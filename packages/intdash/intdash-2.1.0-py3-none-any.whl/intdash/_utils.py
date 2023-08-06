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
import io
from distutils.version import LooseVersion

from intdash import _filter, _models, _protocol, data
from intdash.pb import data_response_pb2, store_request_pb2


def _create_elems_storedata(units, final, serial_number):
    elems = []

    #
    # specs
    #

    elems.append(_protocol.SOSMarker(stream_id=1, serial_number=serial_number))

    for unit in units:
        elems.append(
            _protocol.Unit(
                stream_id=1,
                channel=unit.channel,
                elapsed_time=unit.elapsed_time,
                data=unit.data,
                time_precision="ns",
            )
        )

    elems.append(
        _protocol.EOSMarker(stream_id=1, serial_number=serial_number, final=final)
    )

    return elems


def _create_req_store_protobuf(data_points, final, serial_number, measurement_uuid):
    store_request = store_request_pb2.StoreProto()
    store_request.meas_uuid = measurement_uuid
    store_request.serial_number = serial_number
    store_request.meas_end = final
    store_request.section_end = True  # section status is always True
    store_request.section_total_count.value = 1  # section length is always one

    for dps in data_points:
        data_point = store_request.data_points.add()
        data_point.elapsed_time = dps.elapsed_time.value
        data_point.channel = dps.channel
        data_point.data_type = dps.data_type
        data_point.data_payload = dps.data_payload

    return store_request.SerializeToString()


def _write_req_body(elems):

    bio = io.BytesIO()
    bwr = io.BufferedWriter(bio)
    wr = _protocol.Writer(bwr)

    for e in elems:
        wr.write_elem(e)

    return bio.getvalue()


def _read_resp_body(body):
    bio = io.BytesIO(body)
    brd = io.BufferedReader(bio)
    rd = _protocol.Reader(brd)

    elems = []
    while True:
        try:
            e = rd.read_elem()
        except EOFError:
            break

        elems.append(e)

    return elems


def _read_resp_body_protobuf(body):

    n = 0
    data_points = []
    while n < len(body):
        len_data = int.from_bytes(body[n : n + 8], byteorder="little")
        n += 8

        data_payload = body[n : n + len_data]
        data_response = data_response_pb2.DataResponseProto()
        data_response.ParseFromString(data_payload)
        data_points.append(data_response)
        n += len_data

    return data_points


def _check_supported(api_version, minimum_version):
    if LooseVersion(api_version) < LooseVersion(minimum_version):
        return False
    else:
        return True


def _create_req_upstream(specs):
    reqs = []

    #
    # specs
    #

    uspecs = []
    for i, spec in specs.items():
        uspecs.append(
            _protocol.UpstreamSpec(
                stream_id=i,
                store=spec.store,
                resend=spec.resend,
                measurement_uuid=spec.measurement_uuid,
                src_edge_uuid=spec.src_edge_uuid,
                dst_edge_uuids=spec.dst_edge_uuids,
            )
        )

    reqs.append(_protocol.UpstreamSpecRequest(req_id=0, specs=uspecs))

    return reqs


def _create_req_downstream(specs):
    reqs = []

    #
    # specs
    #

    dspecs = []
    for i, spec in specs.items():
        dspecs.append(
            _protocol.DownstreamSpec(
                stream_id=i,
                src_edge_uuid=spec.src_edge_uuid,
                dst_edge_uuid=spec.dst_edge_uuid,
            )
        )

    reqs.append(_protocol.DownstreamSpecRequest(req_id=0, specs=dspecs))

    #
    # filts
    #

    sfilts = []
    for i, spec in specs.items():

        dfilts = []

        specs_map = {}
        for df in spec.filters:

            key = (df.data_type, df.channel)
            if key not in specs_map:
                specs_map[key] = []

            spec.accept = True
            specs_map[key].append(df.data_id)

        dfilts = []
        for (data_type, channel), ids in specs_map.items():
            try:
                filter_cls = _filter.type_to_filter_class(data_type)

                dfilts.append(
                    _protocol.DownstreamDataFilter(
                        channel=channel, filter=filter_cls.from_ids(ids)
                    )
                )
            except NotImplementedError:

                dfilts.append(
                    _protocol.DownstreamDataFilter(
                        channel=channel, filter=_filter.Any(data_type)
                    )
                )

        sfilts.append(
            _protocol.DownstreamFilter(stream_id=i, downstream_data_filters=dfilts)
        )

    reqs.append(_protocol.DownstreamFilterRequest(req_id=1, filters=sfilts))

    return reqs
