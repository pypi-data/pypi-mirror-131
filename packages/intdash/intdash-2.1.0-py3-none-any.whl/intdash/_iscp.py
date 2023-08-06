# Copyright 2020 Aptpod, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import asyncio
import functools
import io
import logging
import urllib.parse
from typing import Optional

import tornado.httpclient
import tornado.websocket

import intdash.data
from intdash import _models, _protocol, _utils
from intdash._client import USER_AGENT, TokenSource

logger = logging.getLogger(__name__)


class ResultNGException(Exception):
    pass


class ISCPConnClosedException(Exception):
    pass


__all__ = [
    "ISCPConn",
    "Upstream",
    "Downstream",
    "ISCPConnClosedException",
    "ResultNGException",
]


class ISCPConn(object):
    """WebSocket 接続を表すオブジェクトです。"""

    def __init__(
        self,
        client,
        flush_interval,
        on_close=None,
        token_source: Optional[TokenSource] = None,
    ):
        self._logger = logger
        self._client = client
        self._flush_interval = flush_interval
        self._on_close = on_close

        # counters
        self._next_stream_id = cyclic_counter256(initial=1)
        self._next_req_id = cyclic_counter256(initial=0)

        # send buffer and recv queues
        self._send_buffer = []
        self._recv_stream_queues = {}
        self._recv_req_queues = {}

        # underlying WebSocket conn
        self._wsconn = None

        # child stream objects
        self._upstreams = {}
        self._downstreams = {}

        # done events
        self._flush_loop_done_event = None
        self._read_loop_done_event = None
        self._close_done_event = None

        # closing and closed flags
        self._closing = False
        self._closed = asyncio.Event()

        if token_source is not None and not isinstance(token_source, TokenSource):
            raise TypeError("Must be TokenSource class")
        self._token_source = token_source

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        self._logger.info("ISCPConn:   Exited from with clause.")
        await self.close()

    async def _start(self):
        # auth
        if self._token_source is not None:
            tk = self._token_source.token()
        else:
            self._client._auth()
            tk = self._client.jwt

        url = urllib.parse.urlparse(self._client.url)

        assert (
            url.scheme == "http" or url.scheme == "https"
        ), "shceme must be http or https"

        assert (
            self._client.edge_token or tk
        ), "neither edge_token nor access_token is needed"

        req = create_connect_request(
            url=self._client.url,
            edge_token=self._client.edge_token,
            access_token=tk,
        )

        # connect websocket
        self._wsconn = await tornado.websocket.websocket_connect(url=req)

        # start coroutines
        self._flush_loop_done_event = run_and_get_done_event(self._flush_loop())
        self._read_loop_done_event = run_and_get_done_event(self._read_loop())
        self._close_done_event = run_and_get_done_event(self._wrapped_on_close())

    async def _read_loop(self):
        while True:
            if self._closing:
                self._logger.info(
                    "ISCPConn:   Exited from read loop because closed flag is set."
                )
                return

            # read from WebSocket conn
            msg = await self._wsconn.read_message()
            self._logger.debug(f"ISCPConn:   Read WebSocket msg: {msg}")

            # None means connection close
            if msg is None:
                self._logger.info(
                    "ISCPConn:   WebSocket msg is None on WebSocket reading."
                )
                await self._close(ws_already_closed=True)
                return

            # interpret and dispatch
            await self._interpret_and_dispatch(msg)

    async def _interpret_and_dispatch(self, msg):
        bio = io.BytesIO(msg)
        prd = _protocol.Reader(io.BufferedReader(bio))

        while True:
            try:
                elem = prd.read_elem()

                assert isinstance(
                    elem,
                    (_protocol.RequestElement, _protocol.StreamElement),
                ), "elem's type must be RequestElement or StreamElement"

                if isinstance(elem, _protocol.RequestElement):
                    self._logger.info(
                        f"ISCPConn:   iSCP request element received: {elem.req_id}"
                    )
                    # self._logger.info(f"ISCPConn:   iSCP request element received:\n{elem}")
                    queue = self._recv_req_queues.get(elem.req_id)
                    if queue is not None:
                        await queue.put(elem)

                elif isinstance(elem, _protocol.StreamElement):
                    self._logger.debug(
                        f"ISCPConn:   iSCP stream element received:\n{elem}"
                    )
                    queue = self._recv_stream_queues.get(elem.stream_id)
                    if queue is not None:
                        await queue.put(elem)

            except EOFError:
                return

    async def _flush_loop(self):
        while True:
            if self._closing:
                self._logger.info(
                    "ISCPConn:   Exited from flush loop because closed flag is set."
                )
                return

            # repeat every flush_interval seconds
            nxt = asyncio.sleep(self._flush_interval)
            await self._flush()
            await nxt

    async def _flush(self):
        if len(self._send_buffer) == 0:
            return

        bio = io.BytesIO()
        pwr = _protocol.Writer(io.BufferedWriter(bio))

        # get from buffer and write to BytesIO
        for elem in self._send_buffer:

            assert isinstance(
                elem, (_protocol.RequestElement, _protocol.StreamElement)
            ), "elem's type must be RequestElement or StreamElement"

            if isinstance(elem, _protocol.RequestElement):
                self._logger.info(
                    f"ISCPConn:   Writing iSCP request element: {elem.req_id}"
                )
                # self._logger.info(f"ISCPConn:   Writing iSCP request element:\n{elem}")
                pwr.write_elem(elem)

            elif isinstance(elem, _protocol.StreamElement):
                self._logger.debug(f"ISCPConn:   Writing iSCP stream element:\n{elem}")
                pwr.write_elem(elem)

        self._send_buffer = []

        # get value from BytesIO and write to WebSocket conn
        try:
            msg = bio.getvalue()
            self._logger.debug(f"ISCPConn:   Writing WebSocket msg: {msg}")
            await self._wsconn.write_message(message=msg, binary=True)

        except tornado.websocket.WebSocketClosedError as e:
            self._logger.info(
                f"ISCPConn:   WebSocketCloseError occured on WebSocket writing: {e}"
            )
            await self._close(ws_already_closed=True)

    async def _wrapped_on_close(self):
        await self._closed.wait()
        if self._on_close is not None:
            await self._on_close()

    async def _request(self, req_elem):
        # create queue for response
        req_id, queue = self._next_req_id(), asyncio.Queue()
        assert req_id not in self._recv_req_queues, "req_queue is duplicated"
        self._recv_req_queues[req_id] = queue

        # push to send buffer
        req_elem.req_id = req_id
        self._push_elem_to_send_buffer(req_elem)

        # wait response
        resp_elem = await queue.get()
        assert resp_elem.req_id in self._recv_req_queues, "req_queue is disappeared"
        del self._recv_req_queues[resp_elem.req_id]
        queue.task_done()

        return resp_elem

    def _add_recv_stream_queue(self):
        stream_id, queue = self._next_stream_id(), asyncio.Queue()
        assert stream_id not in self._recv_stream_queues, "stream_queue is duplicated"
        self._recv_stream_queues[stream_id] = queue
        return stream_id, queue

    def _del_recv_stream_queue(self, stream_id):
        assert stream_id in self._recv_stream_queues, "stream_queue is disappeared"
        del self._recv_stream_queues[stream_id]

    def _push_elem_to_send_buffer(self, elem):
        self._send_buffer.append(elem)

    @property
    def is_closed(self):
        """bool: コネクションが閉じているか"""
        return self._closed.is_set()

    async def close(self):
        """intdashサーバーとの接続を切断します。"""
        await self._close(ws_already_closed=False)

    async def _close(self, ws_already_closed=False):
        if self._closing:
            self._logger.info("ISCPConn:   Already closing.")
            return

        if self._closed.is_set():
            self._logger.info("ISCPConn:   Already closed.")
            return

        self._logger.info("ISCPConn:   Closing...")

        # close all child streams
        for stream in list(self._upstreams.values()):
            await stream._close(ws_already_closed=ws_already_closed)
        for stream in list(self._downstreams.values()):
            await stream._close(ws_already_closed=ws_already_closed)

        # force flush
        if not ws_already_closed:
            await self._flush()

        # wait flush loop is done
        self._closing = True
        if self._flush_loop_done_event is not None:
            await self._flush_loop_done_event.wait()

        # wait to complete all recv queue's tasks
        await asyncio.gather(
            *[q.join() for q in self._recv_stream_queues.values()],
            *[q.join() for q in self._recv_req_queues.values()],
        )

        # close websocket connection
        if not ws_already_closed:
            self._wsconn.close()

        # wait read loop is done
        if self._read_loop_done_event is not None:
            await self._read_loop_done_event.wait()

        # wait close
        self._closed.set()
        if self._close_done_event is not None:
            await self._close_done_event.wait()

        self._logger.info(f"ISCPConn:   Closed.")

    async def open_upstream(self, spec, marker_interval=1, on_ack=None):
        """指定した仕様でアップストリームを開きます。

        Args:
            spec (intdash.UpstreamSpec): アップストリームスペック
            marker_interval (int): 秒単位のマーカー間隔
            on_ack (func): SectionAckを受信したときに呼ばれるコールバック
        Returns:
            Upstream: アップストリームを表すオブジェクト
        """
        if self._closing:
            self._logger.info(
                "Raise ISCPConnClosedException by ISCPConn.open_upstream because closing flag is set."
            )
            raise ISCPConnClosedException()

        # create stream object
        stream_id, queue = self._add_recv_stream_queue()
        stream = Upstream(
            iscpconn=self,
            stream_id=stream_id,
            spec=spec,
            marker_interval=marker_interval,
            on_ack=on_ack,
            queue=queue,
        )
        self._upstreams[stream_id] = stream

        # start stream
        await stream._start()
        return stream

    async def _send_upstream_open_request(self, stream_id, spec):
        reqs = _utils._create_req_upstream({stream_id: spec})
        for req in reqs:
            resp = await self._request(req)
            if resp.result_code != _protocol.ResultCode.OK:
                raise ResultNGException()

    async def _send_upstream_close_request(self, stream_id):
        close_spec = _models.UpstreamSpec(
            src_edge_uuid=_models.NULL_UUID, dst_edge_uuids=[]
        )
        reqs = _utils._create_req_upstream({stream_id: close_spec})
        for req in reqs:
            resp = await self._request(req)
            if resp.result_code != _protocol.ResultCode.OK:
                raise ResultNGException()

    def _discard_upstream(self, stream_id):
        del self._upstreams[stream_id]
        self._del_recv_stream_queue(stream_id)

    async def open_downstream(self, spec, on_msg=None):
        """指定した仕様でダウンストリームを開きます。

        Args:
            spec (intdash.DownstreamSpec): ダウンストリームスペック
            on_msg (func): データを受信したときに呼ばれるコールバック
        Returns:
            Downstream: ダウンストリームを表すオブジェクト
        """
        if self._closing:
            self._logger.info(
                "Raise ISCPConnClosedException by ISCPConn.open_downstream because closing flag is set."
            )
            raise ISCPConnClosedException()

        # create stream object
        stream_id, queue = self._add_recv_stream_queue()
        stream = Downstream(
            iscpconn=self, stream_id=stream_id, spec=spec, on_msg=on_msg, queue=queue
        )
        self._downstreams[stream_id] = stream

        # start stream
        await stream._start()
        return stream

    async def _send_downstream_open_request(self, stream_id, spec):
        reqs = _utils._create_req_downstream({stream_id: spec})
        for req in reqs:
            resp = await self._request(req)
            if resp.result_code != _protocol.ResultCode.OK:
                raise ResultNGException()

    async def _send_downstream_close_request(self, stream_id):
        close_spec = _models.DownstreamSpec(src_edge_uuid=_models.NULL_UUID, filters=[])
        reqs = _utils._create_req_downstream({stream_id: close_spec})
        for req in reqs:
            resp = await self._request(req)
            if resp.result_code != _protocol.ResultCode.OK:
                raise ResultNGException()

    def _discard_downstream(self, stream_id):
        del self._downstreams[stream_id]
        self._del_recv_stream_queue(stream_id)


class Upstream(object):
    """アップストリームを表すオブジェクトです。"""

    def __init__(self, iscpconn, stream_id, spec, marker_interval, on_ack, queue):
        self._logger = logger

        # public properties
        self.stream_id = stream_id
        self.spec = spec

        # private properties
        self._iscpconn = iscpconn
        self._marker_interval = marker_interval
        self._on_ack = on_ack
        self._queue = queue

        # counters
        self._count = 0
        self._serial = 0

        # done events
        self._ack_loop_done_event = None
        self._section_loop_done_event = None

        # closing and closed flags
        self._closing = False
        self._closed = False

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        self._logger.info("Upstream:   Exited from with clause.")
        await self.close()

    async def _start(self):
        # send open request
        await self._iscpconn._send_upstream_open_request(
            stream_id=self.stream_id, spec=self.spec
        )

        # push first SOS Marker
        self._push_sos_marker()

        # start coroutines
        self._section_loop_done_event = run_and_get_done_event(self._add_section_loop())
        self._ack_loop_done_event = run_and_get_done_event(self._wait_ack_loop())

    async def _wait_ack_loop(self):
        while True:
            if self._closing and self._queue.qsize() == 0:
                self._logger.info(
                    "Upstream:   Exited from wait_ack loop because closing flag is set and queue is empty."
                )
                return

            ack = await self._queue.get()

            # skip None
            if ack is None:
                self._queue.task_done()
                continue

            # call on_ack callback
            if self._on_ack is not None:
                await self._on_ack(ack.serial_number, ack.result_code)
            self._queue.task_done()

    async def _add_section_loop(self):
        while True:
            if self._closing:
                self._logger.info(
                    "Upstream:   Exited from add_section loop because closing flag is set."
                )
                return

            # repeat every marker_interval seconds
            nxt = asyncio.sleep(self._marker_interval)
            self._add_section()
            await nxt

    def _add_section(self):
        if self._count == 0:
            return

        self._push_eos_marker()
        self._count = 0
        self._serial += 1
        self._push_sos_marker()

    def _push_sos_marker(self):
        sos = _protocol.SOSMarker(stream_id=self.stream_id, serial_number=self._serial)
        self._iscpconn._push_elem_to_send_buffer(sos)

    def _push_eos_marker(self):
        eos = _protocol.EOSMarker(
            stream_id=self.stream_id,
            final=False,
            serial_number=self._serial,
        )
        self._iscpconn._push_elem_to_send_buffer(eos)

    async def write(self, datapoint):
        """データポイントを書き込みます。

        Args:
            datapoint (intdash.DataPoint): データポイント
        Returns:
            int: 送信したデータポイントが所属するセクションのシリアル番号
        """
        if self._closing:
            self._logger.info(
                "Upstream:   Raise ISCPConnClosedException by Upstream.write because closing flag is set."
            )
            raise ISCPConnClosedException()

        self._count += 1
        data = intdash.data.type_to_data_class(datapoint.data_type).from_payload(
            datapoint.data_payload
        )
        unit = _protocol.Unit(
            stream_id=self.stream_id,
            channel=datapoint.channel,
            elapsed_time=datapoint.elapsed_time,
            data=data,
        )
        self._iscpconn._push_elem_to_send_buffer(unit)
        return self._serial

    @property
    def is_closed(self):
        """bool: アップストリームが閉じているか"""
        return self._closed

    async def close(self):
        """アップストリームを閉じます。"""
        await self._close(ws_already_closed=False)

    async def _close(self, ws_already_closed=False):
        if self._closing:
            self._logger.info(
                f"Upstream:   Stream {self.stream_id} is already closing."
            )
            return

        if self._closed:
            self._logger.info(f"Upstream:   Stream {self.stream_id} is already closed.")
            return

        self._logger.info(f"Upstream:   Stream {self.stream_id} is closing...")

        # wait ack loop is done
        self._closing = True
        await self._queue.put(None)  # put None to unlock queue
        if self._ack_loop_done_event is not None:
            await self._ack_loop_done_event.wait()

        # add final section
        if not ws_already_closed:
            self._push_eos_marker()

        # send close request and discard self
        if not ws_already_closed:
            await self._iscpconn._send_upstream_close_request(self.stream_id)
        self._iscpconn._discard_upstream(self.stream_id)

        # wait section loop is done
        if self._section_loop_done_event is not None:
            await self._section_loop_done_event.wait()

        self._closed = True
        self._logger.info(f"Upstream:   Stream {self.stream_id} is closed.")


class Downstream(object):
    """ダウンストリームを表すオブジェクトです。"""

    def __init__(self, iscpconn, stream_id, spec, on_msg, queue):
        self._logger = logger

        # public properties
        self.stream_id = stream_id
        self.spec = spec

        # private properties
        self._iscpconn = iscpconn
        self._on_msg = on_msg
        self._queue = queue

        # done events
        self._read_loop_done_event = None

        # closing and closed flags
        self._closing = False
        self._closed = False

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        self._logger.info("Downstream: Exited from with clause.")
        await self.close()

    async def _start(self):
        # send open request
        await self._iscpconn._send_downstream_open_request(
            stream_id=self.stream_id, spec=self.spec
        )

        # start coroutines
        self._read_loop_done_event = run_and_get_done_event(self._read_loop())

    async def _read_loop(self):
        while True:
            if self._closing and self._queue.qsize() == 0:
                self._logger.info(
                    "Downstream: Exited from wait_ack loop because closing flag is set and queue is empty."
                )
                return

            unit = await self._queue.get()

            # skip None
            if unit is None:
                self._queue.task_done()
                continue

            # call on_msg callback
            if self._on_msg is not None:
                await self._on_msg(
                    _models.DataPoint(
                        elapsed_time=unit.elapsed_time,
                        channel=unit.channel,
                        data_type=unit.data.data_type,
                        data_payload=unit.data.to_payload(),
                    )
                )
            self._queue.task_done()

    @property
    def is_closed(self):
        """bool: ダウンストリームが閉じているか"""
        return self._closed

    async def close(self):
        """ダウンストリームを閉じます。"""
        await self._close(ws_already_closed=False)

    async def _close(self, ws_already_closed=False):
        if self._closing:
            self._logger.info(
                f"Downstream: Stream {self.stream_id} is already closing."
            )
            return

        if self._closed:
            self._logger.info(f"Downstream: Stream {self.stream_id} is already closed.")
            return

        self._logger.info(f"Downstream: Stream {self.stream_id} is closing...")

        # wait read loop is done
        self._closing = True
        await self._queue.put(None)  # put None to unlock queue
        if self._read_loop_done_event is not None:
            await self._read_loop_done_event.wait()

        # send close request and discard self
        if not ws_already_closed:
            await self._iscpconn._send_downstream_close_request(self.stream_id)
        self._iscpconn._discard_downstream(self.stream_id)

        self._closed = True
        self._logger.info(f"Downstream: Stream {self.stream_id} is closed.")


def build_wsurl(httpurl):
    parsedurl = urllib.parse.urlparse(httpurl)
    return urllib.parse.urlunparse(
        [
            "wss" if parsedurl.scheme == "https" else "ws",
            parsedurl.netloc,
            parsedurl.path + "/api/v1/ws/measurements",
            parsedurl.params,
            urllib.parse.urlencode({}),
            parsedurl.fragment,
        ]
    )


def create_connect_request(url, edge_token=None, access_token=None):
    url = build_wsurl(url)
    headers = {
        "Content-Type": "application/json; charset=utf-8",
    }
    if edge_token is not None:
        headers["X-Edge-Token"] = edge_token
    elif access_token is not None:
        headers["Authorization"] = "Bearer " + access_token

    return tornado.httpclient.HTTPRequest(
        url=url,
        headers=headers,
        user_agent=USER_AGENT,
    )


def cyclic_counter256(initial):
    cnt = initial

    def inner():
        nonlocal cnt
        next = cnt
        cnt = (cnt + 1) % 256
        return next

    return inner


def run_and_get_done_event(coro):
    def cb(future, done):
        done.set()

    done = asyncio.Event()
    task = asyncio.ensure_future(coro)
    task.add_done_callback(functools.partial(cb, done=done))
    return done
