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

from intdash import _binaly_utils, _internal, _models, data


class Filter(_internal.Comparable, metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    def _read_from(rd):
        pass

    @abc.abstractmethod
    def _write_to(self, wr):
        pass


class Spec(_internal.Comparable, metaclass=abc.ABCMeta):
    @staticmethod
    @abc.abstractmethod
    def _read_from(rd):
        pass

    @abc.abstractmethod
    def _write_to(self, wr):
        pass


class CAN(Filter):
    data_type = _models.DataType.can

    def __init__(self, specs):
        self.specs = specs

    @staticmethod
    def _read_from(rd):
        spec_num = _binaly_utils.read_uint_from(rd, 1)
        specs = [CANSpec._read_from(rd) for _ in range(spec_num)]
        return CAN(specs=specs)

    def _write_to(self, wr):
        _binaly_utils.write_uint_to(wr, len(self.specs), 1)
        [spec._write_to(wr) for spec in self.specs]

    @staticmethod
    def from_ids(ids):
        return CAN(
            specs=[
                CANSpec(
                    mask=int.from_bytes(b"\xff\xff\xff\xff", "little"),
                    result=int(x, 16),
                    accept=True,
                )
                for x in ids
            ]
        )


class CANSpec(Spec):
    def __init__(self, mask, result, accept):
        self.mask = mask
        self.result = result
        self.accept = accept

    @staticmethod
    def _read_from(rd):
        mask = _binaly_utils.read_uint_from(rd, 4)
        result = _binaly_utils.read_uint_from(rd, 4)
        flags = _binaly_utils.read_uint_from(rd, 1)
        accept = bool((flags & 1) >> 0)
        return CANSpec(mask=mask, result=result, accept=accept)

    def _write_to(self, wr):
        _binaly_utils.write_uint_to(wr, self.mask, 4)
        _binaly_utils.write_uint_to(wr, self.result, 4)
        flags = 1 & (int(self.accept) << 0)
        _binaly_utils.write_uint_to(wr, flags, 1)


class NMEA(Filter):
    data_type = _models.DataType.nmea

    def __init__(self, specs):
        self.specs = specs

    @staticmethod
    def _read_from(rd):
        spec_num = _binaly_utils.read_uint_from(rd, 1)
        specs = [NMEASpec._read_from(rd) for _ in range(spec_num)]
        return NMEA(specs=specs)

    def _write_to(self, wr):
        _binaly_utils.write_uint_to(wr, len(self.specs), 1)
        [spec._write_to(wr) for spec in self.specs]

    @staticmethod
    def from_ids(ids):
        return NMEA(
            specs=[
                NMEASpec(
                    mask=int.from_bytes(b"\xff\xff\xff\xff\xff", "little"),
                    result=int.from_bytes(x.encode("utf-8"), "little"),
                    accept=True,
                )
                for x in ids
            ]
        )


class NMEASpec(Spec):
    def __init__(self, mask, result, accept):
        self.mask = mask
        self.result = result
        self.accept = accept

    @staticmethod
    def _read_from(rd):
        mask = _binaly_utils.read_uint_from(rd, 5)
        result = _binaly_utils.read_uint_from(rd, 5)
        flags = _binaly_utils.read_uint_from(rd, 1)
        accept = bool((flags & 1) >> 0)
        return NMEASpec(mask=mask, result=result, accept=accept)

    def _write_to(self, wr):
        _binaly_utils.write_uint_to(wr, self.mask, 5)
        _binaly_utils.write_uint_to(wr, self.result, 5)
        flags = 1 & (int(self.accept) << 0)
        _binaly_utils.write_uint_to(wr, flags, 1)


class GeneralSensor(Filter):
    data_type = _models.DataType.general_sensor

    def __init__(self, specs):
        self.specs = specs

    @staticmethod
    def _read_from(rd):
        spec_num = _binaly_utils.read_uint_from(rd, 1)
        specs = [GeneralSensorSpec._read_from(rd) for _ in range(spec_num)]
        return GeneralSensor(specs=specs)

    def _write_to(self, wr):
        _binaly_utils.write_uint_to(wr, len(self.specs), 1)
        [spec._write_to(wr) for spec in self.specs]

    @staticmethod
    def from_ids(ids):
        return GeneralSensor(
            specs=[
                GeneralSensorSpec(
                    mask=int.from_bytes(b"\xff\xff", "little"),
                    result=int(x, 16),
                    accept=True,
                )
                for x in ids
            ]
        )


class GeneralSensorSpec(Spec):
    def __init__(self, mask, result, accept):
        self.mask = mask
        self.result = result
        self.accept = accept

    @staticmethod
    def _read_from(rd):
        mask = _binaly_utils.read_uint_from(rd, 2)
        result = _binaly_utils.read_uint_from(rd, 2)
        flags = _binaly_utils.read_uint_from(rd, 1)
        accept = bool((flags & 1) >> 0)
        return GeneralSensorSpec(mask=mask, result=result, accept=accept)

    def _write_to(self, wr):
        _binaly_utils.write_uint_to(wr, self.mask, 2)
        _binaly_utils.write_uint_to(wr, self.result, 2)
        flags = 1 & (int(self.accept) << 0)
        _binaly_utils.write_uint_to(wr, flags, 1)


class Generic(Filter):
    data_type = _models.DataType.generic

    def __init__(self, specs):
        self.specs = specs

    @staticmethod
    def _read_from(rd):
        spec_num = _binaly_utils.read_uint_from(rd, 1)
        specs = [GenericSpec._read_from(rd) for _ in range(spec_num)]
        return Generic(specs=specs)

    def _write_to(self, wr):
        _binaly_utils.write_uint_to(wr, len(self.specs), 1)
        [spec._write_to(wr) for spec in self.specs]

    @staticmethod
    def from_ids(ids):
        return Generic(
            specs=[
                GenericSpec(
                    mask=int.from_bytes(b"\xff\xff\xff\xff", "little"),
                    result=int(x, 16),
                    accept=True,
                )
                for x in ids
            ]
        )


class GenericSpec(Spec):
    def __init__(self, mask, result, accept):
        self.mask = mask
        self.result = result
        self.accept = accept

    @staticmethod
    def _read_from(rd):
        mask = _binaly_utils.read_uint_from(rd, 4)
        result = _binaly_utils.read_uint_from(rd, 4)
        flags = _binaly_utils.read_uint_from(rd, 1)
        accept = bool((flags & 1) >> 0)
        return GenericSpec(mask=mask, result=result, accept=accept)

    def _write_to(self, wr):
        _binaly_utils.write_uint_to(wr, self.mask, 4)
        _binaly_utils.write_uint_to(wr, self.result, 4)
        flags = 1 & (int(self.accept) << 0)
        _binaly_utils.write_uint_to(wr, flags, 1)


class Float(Filter):
    data_type = _models.DataType.float

    def __init__(self, specs):
        self.specs = specs

    @staticmethod
    def _read_from(rd):
        spec_num = _binaly_utils.read_uint_from(rd, 1)
        specs = [PrimitiveSpec._read_from(rd) for _ in range(spec_num)]
        return Float(specs=specs)

    def _write_to(self, wr):
        _binaly_utils.write_uint_to(wr, len(self.specs), 1)
        [spec._write_to(wr) for spec in self.specs]

    @staticmethod
    def from_ids(ids):
        return Float(specs=[PrimitiveSpec(label=x) for x in ids])


class Int(Filter):
    data_type = _models.DataType.int

    def __init__(self, specs):
        self.specs = specs

    @staticmethod
    def _read_from(rd):
        spec_num = _binaly_utils.read_uint_from(rd, 1)
        specs = [PrimitiveSpec._read_from(rd) for _ in range(spec_num)]
        return Int(specs=specs)

    def _write_to(self, wr):
        _binaly_utils.write_uint_to(wr, len(self.specs), 1)
        [spec._write_to(wr) for spec in self.specs]

    @staticmethod
    def from_ids(ids):
        return Int(specs=[PrimitiveSpec(label=x) for x in ids])


class String(Filter):
    data_type = _models.DataType.string

    def __init__(self, specs):
        self.specs = specs

    @staticmethod
    def _read_from(rd):
        spec_num = _binaly_utils.read_uint_from(rd, 1)
        specs = [PrimitiveSpec._read_from(rd) for _ in range(spec_num)]
        return String(specs=specs)

    def _write_to(self, wr):
        _binaly_utils.write_uint_to(wr, len(self.specs), 1)
        [spec._write_to(wr) for spec in self.specs]

    @staticmethod
    def from_ids(ids):
        return String(specs=[PrimitiveSpec(label=x) for x in ids])


class Bytes(Filter):
    data_type = _models.DataType.bytes

    def __init__(self, specs):
        self.specs = specs

    @staticmethod
    def _read_from(rd):
        spec_num = _binaly_utils.read_uint_from(rd, 1)
        specs = [PrimitiveSpec._read_from(rd) for _ in range(spec_num)]
        return Bytes(specs=specs)

    def _write_to(self, wr):
        _binaly_utils.write_uint_to(wr, len(self.specs), 1)
        [spec._write_to(wr) for spec in self.specs]

    @staticmethod
    def from_ids(ids):
        return Bytes(specs=[PrimitiveSpec(label=x) for x in ids])


class PrimitiveSpec(Spec):
    def __init__(self, label):
        self.label = label

    @staticmethod
    def _read_from(rd):
        label_len = _binaly_utils.read_uint_from(rd, 1)
        label = _binaly_utils.read_bytes_from(rd, label_len)
        return PrimitiveSpec(label=label.decode("utf-8"))

    def _write_to(self, wr):
        label = self.label.encode("utf-8")
        _binaly_utils.write_uint_to(wr, len(label), 1)
        _binaly_utils.write_bytes_to(wr, label)


class Any(_internal.Comparable):
    def __init__(self, data_type):
        self.data_type = data_type


def type_to_filter_class(t):
    if t == _models.DataType.can:
        return CAN
    elif t == _models.DataType.nmea:
        return NMEA
    elif t == _models.DataType.general_sensor:
        return GeneralSensor
    elif t == _models.DataType.generic:
        return Generic
    elif t == _models.DataType.float:
        return Float
    elif t == _models.DataType.int:
        return Int
    elif t == _models.DataType.string:
        return String
    elif t == _models.DataType.bytes:
        return Bytes

    raise NotImplementedError
