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
import abc
import enum
import io
import struct
import uuid

import pandas as pd

from intdash import _binaly_utils, _filter, _internal, data

VERSION = "v1.5.0"
PREAMBLE = int.from_bytes(b"\xaa", "little")


class ResultCode(int, enum.Enum):
    OK = int.from_bytes(b"\x00", "little")
    NG = int.from_bytes(b"\x01", "little")


class Reader(object):
    def __init__(self, rd: io.BufferedReader):
        rd.seek(0)
        self.rd = rd

    def read_elem(self):
        preamble = _binaly_utils.read_uint_from(self.rd, 1)
        if preamble != PREAMBLE:
            raise ValueError

        elem_type = _binaly_utils.read_uint_from(self.rd, 1)
        elem_class = ElemType(elem_type).to_corresponding_class()

        return elem_class._read_from(self.rd)


class Writer(object):
    def __init__(self, wr: io.BufferedWriter):
        self.wr = wr

    def write_elem(self, elem):
        _binaly_utils.write_uint_to(self.wr, PREAMBLE, 1)
        _binaly_utils.write_uint_to(self.wr, elem.elem_type, 1)

        elem._write_to(self.wr)
        self.wr.flush()


class ElemType(int, enum.Enum):
    UPSTREAM_SPEC_REQUEST = int.from_bytes(b"\x90", "little")
    UPSTREAM_SPEC_RESPONSE = int.from_bytes(b"\x81", "little")
    DOWNSTREAM_SPEC_REQUEST = int.from_bytes(b"\x91", "little")
    DOWNSTREAM_SPEC_RESPONSE = int.from_bytes(b"\x83", "little")
    DOWNSTREAM_FILTER_REQUEST = int.from_bytes(b"\x86", "little")
    DOWNSTREAM_FILTER_RESPONSE = int.from_bytes(b"\x87", "little")
    MEASUREMENT_ID_REQUEST = int.from_bytes(b"\x92", "little")
    MEASUREMENT_ID_RESPONSE = int.from_bytes(b"\x85", "little")
    SOS_MARKER = int.from_bytes(b"\xf9", "little")
    EOS_MARKER = int.from_bytes(b"\xf8", "little")
    SECTION_ACK = int.from_bytes(b"\xfa", "little")
    UNIT = int.from_bytes(b"\x03", "little")

    def to_corresponding_class(self):
        if self == self.UPSTREAM_SPEC_REQUEST:
            return UpstreamSpecRequest
        elif self == self.UPSTREAM_SPEC_RESPONSE:
            return UpstreamSpecResponse
        elif self == self.DOWNSTREAM_SPEC_REQUEST:
            return DownstreamSpecRequest
        elif self == self.DOWNSTREAM_SPEC_RESPONSE:
            return DownstreamSpecResponse
        elif self == self.DOWNSTREAM_FILTER_REQUEST:
            return DownstreamFilterRequest
        elif self == self.DOWNSTREAM_FILTER_RESPONSE:
            return DownstreamFilterResponse
        elif self == self.MEASUREMENT_ID_REQUEST:
            return MeasurementIDRequest
        elif self == self.MEASUREMENT_ID_RESPONSE:
            return MeasurementIDResponse
        elif self == self.SOS_MARKER:
            return SOSMarker
        elif self == self.EOS_MARKER:
            return EOSMarker
        elif self == self.SECTION_ACK:
            return SectionAck
        elif self == self.UNIT:
            return Unit

        raise NotImplementedError


class Element(_internal.Comparable, metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    def _read_from(rd):
        pass

    @abc.abstractmethod
    def _write_to(self, wr):
        pass


class StreamElement(Element):
    pass


class RequestElement(Element):
    pass


class UpstreamSpecRequest(RequestElement):
    elem_type = ElemType.UPSTREAM_SPEC_REQUEST

    def __init__(self, req_id, specs):
        self.req_id = req_id
        self.specs = specs

    @staticmethod
    def _read_from(rd):
        req_id = _binaly_utils.read_uint_from(rd, 1)
        stream_num = _binaly_utils.read_uint_from(rd, 1)
        specs = [UpstreamSpec._read_from(rd) for _ in range(stream_num)]
        return UpstreamSpecRequest(req_id=req_id, specs=specs)

    def _write_to(self, wr):
        _binaly_utils.write_uint_to(wr, self.req_id, 1)
        _binaly_utils.write_uint_to(wr, len(self.specs), 1)
        [spec._write_to(wr) for spec in self.specs]


class UpstreamSpec(_internal.Comparable):
    def __init__(
        self, stream_id, store, resend, measurement_uuid, src_edge_uuid, dst_edge_uuids
    ):
        self.stream_id = stream_id
        self.store = store
        self.resend = resend
        self.measurement_uuid = measurement_uuid
        self.src_edge_uuid = src_edge_uuid
        self.dst_edge_uuids = dst_edge_uuids

    @staticmethod
    def _read_from(rd):
        stream_id = _binaly_utils.read_uint_from(rd, 1)
        dst_num = _binaly_utils.read_uint_from(rd, 1)
        flags = _binaly_utils.read_uint_from(rd, 1)
        store = bool((flags & 2) >> 1)
        resend = bool((flags & 1) >> 0)
        measurement_uuid = _binaly_utils.read_uuid_from(rd)
        src_edge_uuid = _binaly_utils.read_uuid_from(rd)
        dst_edge_uuids = [_binaly_utils.read_uuid_from(rd) for _ in range(dst_num)]

        return UpstreamSpec(
            stream_id=stream_id,
            store=store,
            resend=resend,
            measurement_uuid=measurement_uuid,
            src_edge_uuid=src_edge_uuid,
            dst_edge_uuids=dst_edge_uuids,
        )

    def _write_to(self, wr):
        _binaly_utils.write_uint_to(wr, self.stream_id, 1)
        _binaly_utils.write_uint_to(wr, len(self.dst_edge_uuids), 1)
        flags = 1 & (int(self.resend) << 0) | 2 & (int(self.store) << 1)
        _binaly_utils.write_uint_to(wr, flags, 1)
        _binaly_utils.write_uuid_to(wr, self.measurement_uuid)
        _binaly_utils.write_uuid_to(wr, self.src_edge_uuid)
        [_binaly_utils.write_uuid_to(wr, uuid) for uuid in self.dst_edge_uuids]


class UpstreamSpecResponse(RequestElement):
    elem_type = ElemType.UPSTREAM_SPEC_RESPONSE

    def __init__(self, req_id, result_code):
        self.req_id = req_id
        self.result_code = result_code

    @staticmethod
    def _read_from(rd):
        req_id = _binaly_utils.read_uint_from(rd, 1)
        result_code = _binaly_utils.read_uint_from(rd, 1)
        return UpstreamSpecResponse(req_id=req_id, result_code=result_code)

    def _write_to(self, wr):
        _binaly_utils.write_uint_to(wr, self.req_id, 1)
        _binaly_utils.write_uint_to(wr, self.result_code, 1)


class DownstreamSpecRequest(RequestElement):
    elem_type = ElemType.DOWNSTREAM_SPEC_REQUEST

    def __init__(self, req_id, specs):
        self.req_id = req_id
        self.specs = specs

    @staticmethod
    def _read_from(rd):
        req_id = _binaly_utils.read_uint_from(rd, 1)
        stream_num = _binaly_utils.read_uint_from(rd, 1)
        specs = [DownstreamSpec._read_from(rd) for _ in range(stream_num)]
        return DownstreamSpecRequest(req_id=req_id, specs=specs)

    def _write_to(self, wr):
        _binaly_utils.write_uint_to(wr, self.req_id, 1)
        _binaly_utils.write_uint_to(wr, len(self.specs), 1)
        [spec._write_to(wr) for spec in self.specs]


class DownstreamSpec(_internal.Comparable):
    def __init__(self, stream_id, src_edge_uuid, dst_edge_uuid):
        self.stream_id = stream_id
        self.src_edge_uuid = src_edge_uuid
        self.dst_edge_uuid = dst_edge_uuid

    @staticmethod
    def _read_from(rd):
        stream_id = _binaly_utils.read_uint_from(rd, 1)
        src_edge_uuid = _binaly_utils.read_uuid_from(rd)
        dst_edge_uuid = _binaly_utils.read_uuid_from(rd)

        return DownstreamSpec(
            stream_id=stream_id,
            src_edge_uuid=src_edge_uuid,
            dst_edge_uuid=dst_edge_uuid,
        )

    def _write_to(self, wr):
        _binaly_utils.write_uint_to(wr, self.stream_id, 1)
        _binaly_utils.write_uuid_to(wr, self.src_edge_uuid)
        _binaly_utils.write_uuid_to(wr, self.dst_edge_uuid)


class DownstreamSpecResponse(RequestElement):
    elem_type = ElemType.DOWNSTREAM_SPEC_RESPONSE

    def __init__(self, req_id, result_code):
        self.req_id = req_id
        self.result_code = result_code

    @staticmethod
    def _read_from(rd):
        req_id = _binaly_utils.read_uint_from(rd, 1)
        result_code = _binaly_utils.read_uint_from(rd, 1)
        return DownstreamSpecResponse(req_id=req_id, result_code=result_code)

    def _write_to(self, wr):
        _binaly_utils.write_uint_to(wr, self.req_id, 1)
        _binaly_utils.write_uint_to(wr, self.result_code, 1)


class DownstreamFilterRequest(RequestElement):
    elem_type = ElemType.DOWNSTREAM_FILTER_REQUEST

    def __init__(self, req_id, filters):
        self.req_id = req_id
        self.filters = filters

    @staticmethod
    def _read_from(rd):
        req_id = _binaly_utils.read_uint_from(rd, 1)
        filt_num = _binaly_utils.read_uint_from(rd, 1)
        filters = [DownstreamFilter._read_from(rd) for _ in range(filt_num)]
        return DownstreamFilterRequest(req_id=req_id, filters=filters)

    def _write_to(self, wr):
        _binaly_utils.write_uint_to(wr, self.req_id, 1)
        _binaly_utils.write_uint_to(wr, len(self.filters), 1)
        [filt._write_to(wr) for filt in self.filters]


class DownstreamFilter(_internal.Comparable):
    def __init__(self, stream_id, downstream_data_filters):
        self.stream_id = stream_id
        self.downstream_data_filters = downstream_data_filters

    @staticmethod
    def _read_from(rd):
        stream_id = _binaly_utils.read_uint_from(rd, 1)
        filt_num = _binaly_utils.read_uint_from(rd, 2)
        filters = [DownstreamDataFilter._read_from(rd) for _ in range(filt_num)]
        return DownstreamFilter(stream_id=stream_id, downstream_data_filters=filters)

    def _write_to(self, wr):
        _binaly_utils.write_uint_to(wr, self.stream_id, 1)
        _binaly_utils.write_uint_to(wr, len(self.downstream_data_filters), 2)
        [filt._write_to(wr) for filt in self.downstream_data_filters]


class DownstreamDataFilter(_internal.Comparable):
    def __init__(self, channel, filter):
        self.channel = channel
        self.filter = filter

    @staticmethod
    def _read_from(rd):
        channel = _binaly_utils.read_uint_from(rd, 1)
        data_type = _binaly_utils.read_uint_from(rd, 1)
        length = _binaly_utils.read_uint_from(rd, 2)
        if 0 < length:
            payload = _binaly_utils.read_bytes_from(rd, length)

            filter_class = _filter.type_to_filter_class(data_type)
            bio = io.BytesIO(payload)
            payload_rd = io.BufferedReader(bio)
            filt = filter_class._read_from(payload_rd)
        else:
            filt = _filter.Any(data_type=data_type)

        return DownstreamDataFilter(channel=channel, filter=filt)

    def _write_to(self, wr):
        bio = io.BytesIO()
        if type(self.filter) != _filter.Any:
            payload_wr = io.BufferedWriter(bio)
            self.filter._write_to(payload_wr)
            payload_wr.flush()
        payload = bio.getvalue()

        _binaly_utils.write_uint_to(wr, self.channel, 1)
        _binaly_utils.write_uint_to(wr, self.filter.data_type, 1)
        _binaly_utils.write_uint_to(wr, len(payload), 2)
        _binaly_utils.write_bytes_to(wr, payload)


class DownstreamFilterResponse(RequestElement):
    elem_type = ElemType.DOWNSTREAM_FILTER_RESPONSE

    def __init__(self, req_id, result_code):
        self.req_id = req_id
        self.result_code = result_code

    @staticmethod
    def _read_from(rd):
        req_id = _binaly_utils.read_uint_from(rd, 1)
        result_code = _binaly_utils.read_uint_from(rd, 1)
        return DownstreamFilterResponse(req_id=req_id, result_code=result_code)

    def _write_to(self, wr):
        _binaly_utils.write_uint_to(wr, self.req_id, 1)
        _binaly_utils.write_uint_to(wr, self.result_code, 1)


class MeasurementIDRequest(RequestElement):
    elem_type = ElemType.MEASUREMENT_ID_REQUEST

    def __init__(self, req_id, edge_uuid):
        self.req_id = req_id
        self.edge_uuid = edge_uuid

    @staticmethod
    def _read_from(rd):
        req_id = _binaly_utils.read_uint_from(rd, 1)
        edge_uuid = _binaly_utils.read_uuid_from(rd)
        return MeasurementIDRequest(req_id=req_id, edge_uuid=edge_uuid)

    def _write_to(self, wr):
        _binaly_utils.write_uint_to(wr, self.req_id, 1)
        _binaly_utils.write_uuid_to(wr, self.edge_uuid)


class MeasurementIDResponse(RequestElement):
    elem_type = ElemType.MEASUREMENT_ID_RESPONSE

    def __init__(self, req_id, result_code, measurement_uuid):
        self.req_id = req_id
        self.result_code = result_code
        self.measurement_uuid = measurement_uuid

    @staticmethod
    def _read_from(rd):
        req_id = _binaly_utils.read_uint_from(rd, 1)
        result_code = _binaly_utils.read_uint_from(rd, 1)
        measurement_uuid = _binaly_utils.read_uuid_from(rd)
        return MeasurementIDResponse(
            req_id=req_id, result_code=result_code, measurement_uuid=measurement_uuid
        )

    def _write_to(self, wr):
        _binaly_utils.write_uint_to(wr, self.req_id, 1)
        _binaly_utils.write_uint_to(wr, self.result_code, 1)
        _binaly_utils.write_uuid_to(wr, self.measurement_uuid)


class SOSMarker(StreamElement):
    elem_type = ElemType.SOS_MARKER

    def __init__(self, stream_id, serial_number):
        self.stream_id = stream_id
        self.serial_number = serial_number

    @staticmethod
    def _read_from(rd):
        stream_id = _binaly_utils.read_uint_from(rd, 1)
        serial_number = _binaly_utils.read_uint_from(rd, 4)
        return SOSMarker(stream_id=stream_id, serial_number=serial_number)

    def _write_to(self, wr):
        _binaly_utils.write_uint_to(wr, self.stream_id, 1)
        _binaly_utils.write_uint_to(wr, self.serial_number, 4)


class EOSMarker(StreamElement):
    elem_type = ElemType.EOS_MARKER

    def __init__(self, stream_id, final, serial_number):
        self.stream_id = stream_id
        self.final = final
        self.serial_number = serial_number

    @staticmethod
    def _read_from(rd):
        stream_id = _binaly_utils.read_uint_from(rd, 1)
        flags = _binaly_utils.read_uint_from(rd, 1)
        final = bool((flags & 1) >> 0)
        serial_number = _binaly_utils.read_uint_from(rd, 4)
        return EOSMarker(stream_id=stream_id, final=final, serial_number=serial_number)

    def _write_to(self, wr):
        _binaly_utils.write_uint_to(wr, self.stream_id, 1)
        flags = 1 & (int(self.final) << 0)
        _binaly_utils.write_uint_to(wr, flags, 1)
        _binaly_utils.write_uint_to(wr, self.serial_number, 4)


class SectionAck(StreamElement):
    elem_type = ElemType.SECTION_ACK

    def __init__(self, stream_id, result_code, serial_number):
        self.stream_id = stream_id
        self.result_code = result_code
        self.serial_number = serial_number

    @staticmethod
    def _read_from(rd):
        stream_id = _binaly_utils.read_uint_from(rd, 1)
        result_code = _binaly_utils.read_uint_from(rd, 1)
        serial_number = _binaly_utils.read_uint_from(rd, 4)
        return SectionAck(
            stream_id=stream_id, result_code=result_code, serial_number=serial_number
        )

    def _write_to(self, wr):
        _binaly_utils.write_uint_to(wr, self.stream_id, 1)
        _binaly_utils.write_uint_to(wr, self.result_code, 1)
        _binaly_utils.write_uint_to(wr, self.serial_number, 4)


class Unit(StreamElement):
    elem_type = ElemType.UNIT

    def __init__(self, stream_id, channel, elapsed_time, data, time_precision=None):
        self.stream_id = stream_id
        self.channel = channel
        self.elapsed_time = elapsed_time
        self.time_precision = time_precision
        self.data = data

    @staticmethod
    def _read_from(rd):
        stream_id = _binaly_utils.read_uint_from(rd, 1)
        channel = _binaly_utils.read_uint_from(rd, 1)
        data_type = _binaly_utils.read_uint_from(rd, 1)
        elapsed_time_sec, _ = _binaly_utils.read_variable_uint16to24_from(rd)
        elapsed_time_frac, frac_len = _binaly_utils.read_variable_uint16to32_from(rd)

        if frac_len == 2:
            time_precision = "ms"
            elapsed_time = pd.Timedelta(
                elapsed_time_sec * 1_000_000_000 + elapsed_time_frac * 1_000_000,
                unit="ns",
            )
        elif frac_len == 3:
            time_precision = "us"
            elapsed_time = pd.Timedelta(
                elapsed_time_sec * 1_000_000_000 + elapsed_time_frac * 1_000,
                unit="ns",
            )
        elif frac_len == 4:
            time_precision = "ns"
            elapsed_time = pd.Timedelta(
                elapsed_time_sec * 1_000_000_000 + elapsed_time_frac,
                unit="ns",
            )

        length, _ = _binaly_utils.read_variable_uint8to32_from(rd)
        payload = _binaly_utils.read_bytes_from(rd, length)

        bio = io.BytesIO(payload)
        payload_rd = io.BufferedReader(bio)

        data_class = data.type_to_data_class(data_type)
        d = data_class._read_from(payload_rd)

        return Unit(
            stream_id=stream_id,
            channel=channel,
            elapsed_time=elapsed_time,
            data=d,
            time_precision=time_precision,
        )

    def _write_to(self, wr):
        bio = io.BytesIO()
        payload_wr = io.BufferedWriter(bio)
        self.data._write_to(payload_wr)
        payload_wr.flush()
        payload = bio.getvalue()

        _binaly_utils.write_uint_to(wr, self.stream_id, 1)
        _binaly_utils.write_uint_to(wr, self.channel, 1)
        _binaly_utils.write_uint_to(wr, self.data.data_type, 1)

        sec = self.elapsed_time.value // 1_000_000_000
        nsec = self.elapsed_time.value - sec * 1_000_000_000
        if sec < 32_768:  # 2^(16-1)
            _binaly_utils.write_variable_uint16to24_to(wr, sec, 2)
        else:
            _binaly_utils.write_variable_uint16to24_to(wr, sec, 3)

        if self.time_precision == "ns":
            _binaly_utils.write_variable_uint16to32_to(wr, nsec, 4)
        elif self.time_precision == "us" or self.time_precision is None:
            _binaly_utils.write_variable_uint16to32_to(wr, nsec // 1_000, 3)
        elif self.time_precision == "ms":
            _binaly_utils.write_variable_uint16to32_to(wr, nsec // 1_000_000, 2)

        payload_len = len(payload)
        if payload_len < 64:  # 2^(8-2)
            _binaly_utils.write_variable_uint8to32_to(wr, payload_len, 1)
        elif payload_len < 16_384:  # 2^(16-2)
            _binaly_utils.write_variable_uint8to32_to(wr, payload_len, 2)
        elif payload_len < 4_194_304:  # 2^(24-2)
            _binaly_utils.write_variable_uint8to32_to(wr, payload_len, 3)
        else:
            _binaly_utils.write_variable_uint8to32_to(wr, payload_len, 4)

        _binaly_utils.write_bytes_to(wr, payload)
