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
import io
import struct

import pandas as pd
import pytz

from intdash import _binaly_utils, _internal, _models, timeutils

__all__ = [
    "CAN",
    "NMEA",
    "GeneralSensor",
    "Controlpad",
    "Generic",
    "JPEG",
    "Float",
    "String",
    "Int",
    "Bytes",
    "Basetime",
    "H264",
    "AAC",
    "PCM",
]

DISPLAY_MAX_LENGTH = 20


class Data(_internal.Comparable, metaclass=abc.ABCMeta):
    """intdash で定義されるデータ型のベースクラスです。"""

    @staticmethod
    @abc.abstractmethod
    def _read_from(rd):
        pass

    @abc.abstractmethod
    def _write_to(self, wr):
        pass

    def to_payload(self):
        """データオブジェクトをデータのペイロードに変換します。"""

        bio = io.BytesIO()
        wr = io.BufferedWriter(bio)

        self._write_to(wr)
        wr.flush()

        return bio.getvalue()


class RawData(Data):
    def __str__(self) -> str:
        data = ["%02X" % b for b in self.data]
        if len(data) < DISPLAY_MAX_LENGTH:
            s = " ".join(data)
        else:
            s = " ".join(data[:DISPLAY_MAX_LENGTH]) + " ..."

        return "data_type: {data_type}\ndata_id: {id}\ndata: {s}".format(
            data_type=self.data_type.name, id=self.data_id, s=s
        )


class ValueData(RawData):
    def __str__(self) -> str:
        return "data_type: {data_type}\ndata_id: {id}\nvalue: {value}".format(
            data_type=self.data_type.name, id=self.data_id, value=self.value
        )


class CAN(RawData):
    """CANのデータを表すオブジェクトです。

    Attributes:
        decimal_id (int): データIDの10進数表記
        data (bytes): 表現されるデータ
    """

    data_type = _models.DataType.can
    """データタイプ
    """

    def __init__(self, decimal_id, data):
        self.decimal_id = decimal_id
        self.data = data

    @staticmethod
    def _read_from(rd):
        decimal_id = _binaly_utils.read_uint_from(rd, 4)
        dlc = _binaly_utils.read_uint_from(rd, 1)
        data = _binaly_utils.read_bytes_from(rd, dlc)
        return CAN(decimal_id=decimal_id, data=data)

    def _write_to(self, wr):
        _binaly_utils.write_uint_to(wr, self.decimal_id, 4)
        _binaly_utils.write_uint_to(wr, len(self.data), 1)
        _binaly_utils.write_bytes_to(wr, self.data)

    @staticmethod
    def from_payload(data_payload):
        """データのペイロードを CAN オブジェクトに変換します。

        Args:
            data_payload(bytes): データのペイロード
        """
        return CAN(
            decimal_id=int.from_bytes(data_payload[:4], byteorder="little"),
            data=data_payload[5:],
        )

    @property
    def data_id(self):
        """データID"""
        return "%08x" % self.decimal_id


class NMEA(RawData):
    """NMEAのデータを表すオブジェクトです。

    Attributes:
        string (str): 表現されるデータ

    .. note::
        `data_id` は NMEAString 内のトーカとメッセージ5文字を UTF-8 エンコード した値が指定されます。
    """

    data_type = _models.DataType.nmea
    """データタイプ
    """

    def __init__(self, string):
        self.string = string

    @staticmethod
    def _read_from(rd):
        bs = _binaly_utils.read_allbytes_from(rd)
        return NMEA(string=bs.decode("utf-8"))

    def _write_to(self, wr):
        bs = self.string.encode("utf-8")
        _binaly_utils.write_bytes_to(wr, bs)

    @staticmethod
    def from_payload(data_payload):
        """データのペイロードを NMEA オブジェクトに変換します。

        Args:
            data_payload(bytes): データのペイロード
        """
        return NMEA(string=data_payload.decode("utf-8"))

    @property
    def data_id(self):
        """データID"""
        return self.string[1:6]

    @property
    def data(self):
        return self.string.encode("utf-8")

    @property
    def value(self):
        return self.string


class GeneralSensor(RawData):
    """汎用センサのデータを表すオブジェクトです。

    Attributes:
        decimal_id (int): データIDの10進数表記
        data (bytes): 表現されるデータ
    """

    data_type = _models.DataType.general_sensor
    """データタイプ
    """

    def __init__(self, decimal_id, data):
        self.decimal_id = decimal_id
        self.data = data

    @staticmethod
    def _read_from(rd):
        decimal_id = _binaly_utils.read_uint_from(rd, 2)
        data = _binaly_utils.read_allbytes_from(rd)
        return GeneralSensor(decimal_id=decimal_id, data=data)

    def _write_to(self, wr):
        _binaly_utils.write_uint_to(wr, self.decimal_id, 2)
        _binaly_utils.write_bytes_to(wr, self.data)

    @staticmethod
    def from_payload(data_payload):
        """データのペイロードを GeneralSensor オブジェクトに変換します。

        Args:
            data_payload(bytes): データのペイロード
        """

        return GeneralSensor(
            decimal_id=int.from_bytes(data_payload[:2], byteorder="little"),
            data=data_payload[2:],
        )

    @property
    def data_id(self):
        """データID"""
        return "%04x" % self.decimal_id


class JPEG(RawData):
    """JPEGのデータを表すオブジェクトです。

    Attributes:
        data (bytes): 表現されるデータ
    """

    data_type = _models.DataType.jpeg
    """データタイプ
    """

    data_id = "jpeg"
    """データID
    """

    def __init__(self, data):
        self.data = data

    @staticmethod
    def _read_from(rd):
        data = _binaly_utils.read_allbytes_from(rd)
        return JPEG(data=data)

    def _write_to(self, wr):
        _binaly_utils.write_bytes_to(wr, self.data)

    @staticmethod
    def from_payload(data_payload):
        """データのペイロードを JPEG オブジェクトに変換します。

        Args:
            data_payload(bytes): データのペイロード
        """
        return JPEG(data=data_payload)


class H264(RawData):
    """H.264のデータを表すオブジェクトです。

    Attributes:
        type_id (int): データ部の種別番号
        data (bytes): 表現されるデータ
    """

    data_type = _models.DataType.h264
    """データタイプ
    """

    def __init__(self, type_id, data):
        self.type_id = type_id
        self.data = data

    @staticmethod
    def _read_from(rd):
        type_id = _binaly_utils.read_uint_from(rd, 1)
        data = _binaly_utils.read_allbytes_from(rd)
        return H264(type_id=type_id, data=data)

    def _write_to(self, wr):
        _binaly_utils.write_uint_to(wr, self.type_id, 1)
        _binaly_utils.write_bytes_to(wr, self.data)

    @staticmethod
    def from_payload(data_payload):
        """データのペイロードを H264 オブジェクトに変換します。

        Args:
            data_payload(bytes): データのペイロード
        """
        return H264(
            type_id=int.from_bytes(data_payload[:1], byteorder="little"),
            data=data_payload[1:],
        )

    @property
    def data_id(self):
        """データID"""
        return "%02x" % self.type_id


class AAC(RawData):
    """AACのデータを表すオブジェクトです。

    Attributes:
        data (bytes): 表現されるデータ
    """

    data_type = _models.DataType.aac
    """データタイプ
    """

    data_id = "aac"
    """データID
    """

    def __init__(self, data):
        self.data = data

    @staticmethod
    def _read_from(rd):
        data = _binaly_utils.read_allbytes_from(rd)
        return AAC(data=data)

    def _write_to(self, wr):
        _binaly_utils.write_bytes_to(wr, self.data)

    @staticmethod
    def from_payload(data_payload):
        """データのペイロードを AAC オブジェクトに変換します。

        Args:
            data_payload(bytes): データのペイロード
        """
        return AAC(data=data_payload)


class PCM(RawData):
    """PCMのデータを表すオブジェクトです。

    Attributes:
        format_id (int): フォーマットID
        channels (int): pcmチャンネル数
        sample_rate (int): サンプルレート
        bit_per_sample (int):  ビットレート
        data (bytes): 表現されるデータ
    """

    data_type = _models.DataType.pcm
    """データタイプ
    """

    data_id = "pcm"
    """データID
    """

    def __init__(self, format_id, channels, sample_rate, bit_per_sample, data):
        self.format_id = format_id
        self.channels = channels
        self.sample_rate = sample_rate
        self.bit_per_sample = bit_per_sample
        self.data = data

    @staticmethod
    def _read_from(rd):
        format_id = _binaly_utils.read_uint_from(rd, 2)
        channels = _binaly_utils.read_uint_from(rd, 2)
        sample_rate = _binaly_utils.read_uint_from(rd, 4)
        bit_per_sample = _binaly_utils.read_uint_from(rd, 2)
        data = _binaly_utils.read_allbytes_from(rd)
        return PCM(
            format_id=format_id,
            channels=channels,
            sample_rate=sample_rate,
            bit_per_sample=bit_per_sample,
            data=data,
        )

    def _write_to(self, wr):
        _binaly_utils.write_uint_to(wr, self.format_id, 2)
        _binaly_utils.write_uint_to(wr, self.channels, 2)
        _binaly_utils.write_uint_to(wr, self.sample_rate, 4)
        _binaly_utils.write_uint_to(wr, self.bit_per_sample, 2)
        _binaly_utils.write_bytes_to(wr, self.data)

    @staticmethod
    def from_payload(data_payload):
        """データのペイロードを PCM オブジェクトに変換します。

        Args:
            data_payload(bytes): データのペイロード
        """
        return PCM(
            format_id=int.from_bytes(data_payload[:2], byteorder="little"),
            channels=int.from_bytes(data_payload[2:4], byteorder="little"),
            sample_rate=int.from_bytes(data_payload[4:8], byteorder="little"),
            bit_per_sample=int.from_bytes(data_payload[8:10], byteorder="little"),
            data=data_payload[10:],
        )


class Controlpad(RawData):
    """コントロールパッドのデータを表すオブジェクトです。

    Attributes:
        decimal_id (int): データIDの10進数表記
        data (bytes): 表現されるデータ
    """

    data_type = _models.DataType.controlpad
    """データタイプ
    """

    def __init__(self, decimal_id, data):
        self.decimal_id = decimal_id
        self.data = data

    @staticmethod
    def _read_from(rd):
        decimal_id = _binaly_utils.read_uint_from(rd, 1)
        data = _binaly_utils.read_allbytes_from(rd)
        return Controlpad(decimal_id=decimal_id, data=data)

    def _write_to(self, wr):
        _binaly_utils.write_uint_to(wr, self.decimal_id, 1)
        _binaly_utils.write_bytes_to(wr, self.data)

    @staticmethod
    def from_payload(data_payload):
        """データのペイロードを Controlpad オブジェクトに変換します。

        Args:
            data_payload(bytes): データのペイロード
        """
        return Controlpad(
            decimal_id=int.from_bytes(data_payload[:1], byteorder="little"),
            data=data_payload[1:],
        )

    @property
    def data_id(self):
        """データID"""
        return "%02x" % self.decimal_id


class Generic(RawData):
    """汎用データのデータを表すオブジェクトです。

    Attributes:
        decimal_id (int): データID
        data (bytes): 表現されるデータ
    """

    data_type = _models.DataType.generic
    """データタイプ
    """

    def __init__(self, decimal_id, data):
        self.decimal_id = decimal_id
        self.data = data

    @staticmethod
    def _read_from(rd):
        decimal_id = _binaly_utils.read_uint_from(rd, 4)
        data = _binaly_utils.read_allbytes_from(rd)
        return Generic(decimal_id=decimal_id, data=data)

    def _write_to(self, wr):
        _binaly_utils.write_uint_to(wr, self.decimal_id, 4)
        _binaly_utils.write_bytes_to(wr, self.data)

    @staticmethod
    def from_payload(data_payload):
        """データのペイロードを Generic オブジェクトに変換します。

        Args:
            data_payload(bytes): データのペイロード
        """
        return Generic(
            decimal_id=int.from_bytes(data_payload[:4], byteorder="little"),
            data=data_payload[4:],
        )

    @property
    def data_id(self):
        """データID"""
        return "%08x" % self.decimal_id


class Float(ValueData):
    """倍精度浮動小数点数のデータを表すオブジェクトです。

    Attributes:
        data_id (str): データID
        value (float): 表現されるデータ
    """

    data_type = _models.DataType.float
    """データタイプ
    """

    def __init__(self, data_id, value):
        self.data_id = data_id
        self.value = value

    @staticmethod
    def _read_from(rd):
        id_length = _binaly_utils.read_uint_from(rd, 1)
        data_id = _binaly_utils.read_bytes_from(rd, id_length)
        value = _binaly_utils.read_float64_from(rd)
        return Float(data_id=data_id.decode("utf-8"), value=value)

    def _write_to(self, wr):
        data_id = self.data_id.encode("utf-8")
        id_length = len(data_id)
        _binaly_utils.write_uint_to(wr, id_length, 1)
        _binaly_utils.write_bytes_to(wr, data_id)
        _binaly_utils.write_float64_to(wr, self.value)

    @staticmethod
    def from_payload(data_payload):
        """データのペイロードを Float オブジェクトに変換します。

        Args:
            data_payload(bytes): データのペイロード
        """
        id_length = int.from_bytes(data_payload[:1], byteorder="little")
        data_id = data_payload[1 : 1 + id_length].decode("utf-8")
        value = struct.unpack("<d", data_payload[1 + id_length :])[0]
        return Float(data_id=data_id, value=value)

    @property
    def data(self):
        bs = struct.pack("<d", self.value)
        return bs


class String(ValueData):
    """文字列のデータを表すオブジェクトです。

    Attributes:
        data_id (str): データID
        value (str): 表現されるデータ
    """

    data_type = _models.DataType.string
    """データタイプ
    """

    def __init__(self, data_id, value):
        self.data_id = data_id
        self.value = value

    @staticmethod
    def _read_from(rd):
        id_length = _binaly_utils.read_uint_from(rd, 1)
        data_id = _binaly_utils.read_bytes_from(rd, id_length)
        value = _binaly_utils.read_allbytes_from(rd)
        return String(data_id=data_id.decode("utf-8"), value=value.decode("utf-8"))

    def _write_to(self, wr):
        data_id = self.data_id.encode("utf-8")
        id_length = len(data_id)
        _binaly_utils.write_uint_to(wr, id_length, 1)
        _binaly_utils.write_bytes_to(wr, data_id)
        _binaly_utils.write_bytes_to(wr, self.value.encode("utf-8"))

    @staticmethod
    def from_payload(data_payload):
        """データのペイロードを String オブジェクトに変換します。

        Args:
            data_payload(bytes): データのペイロード
        """
        id_length = int.from_bytes(data_payload[:1], byteorder="little")
        data_id = data_payload[1 : 1 + id_length].decode("utf-8")
        value = data_payload[1 + id_length :].decode("utf-8")
        return String(data_id=data_id, value=value)

    @property
    def data(self):
        return self.value.encode("utf-8")


class Int(ValueData):
    """64bit符号付き整数のデータを表すオブジェクトです。

    Attributes:
        data_id (str): データID
        value (int): 表現されるデータ
    """

    data_type = _models.DataType.int
    """データタイプ
    """

    def __init__(self, data_id, value):
        self.data_id = data_id
        self.value = value

    @staticmethod
    def _read_from(rd):
        id_length = _binaly_utils.read_uint_from(rd, 1)
        data_id = _binaly_utils.read_bytes_from(rd, id_length)
        value = _binaly_utils.read_int64_from(rd)
        return Int(data_id=data_id.decode("utf-8"), value=value)

    def _write_to(self, wr):
        data_id = self.data_id.encode("utf-8")
        id_length = len(data_id)
        _binaly_utils.write_uint_to(wr, id_length, 1)
        _binaly_utils.write_bytes_to(wr, data_id)
        _binaly_utils.write_int64_to(wr, self.value)

    @staticmethod
    def from_payload(data_payload):
        """データのペイロードを Int オブジェクトに変換します。

        Args:
            data_payload(bytes): データのペイロード
        """
        id_length = int.from_bytes(data_payload[:1], byteorder="little")
        data_id = data_payload[1 : 1 + id_length].decode("utf-8")
        value = int.from_bytes(data_payload[1 + id_length :], byteorder="little")
        return Int(data_id=data_id, value=value)

    @property
    def data(self):
        return self.value


class Bytes(ValueData):
    """バイト列のデータを表すオブジェクトです。

    Attributes:
        data_id (str): データID
        value (bytes): 表現されるデータ
    """

    data_type = _models.DataType.bytes
    """データタイプ
    """

    def __init__(self, data_id, value):
        self.data_id = data_id
        self.value = value

    @staticmethod
    def _read_from(rd):
        id_length = _binaly_utils.read_uint_from(rd, 1)
        data_id = _binaly_utils.read_bytes_from(rd, id_length)
        value = _binaly_utils.read_allbytes_from(rd)
        return Bytes(data_id=data_id.decode("utf-8"), value=value)

    def _write_to(self, wr):
        data_id = self.data_id.encode("utf-8")
        id_length = len(data_id)
        _binaly_utils.write_uint_to(wr, id_length, 1)
        _binaly_utils.write_bytes_to(wr, data_id)
        _binaly_utils.write_bytes_to(wr, self.value)

    @staticmethod
    def from_payload(data_payload):
        """データのペイロードを Bytes オブジェクトに変換します。

        Args:
            data_payload(bytes): データのペイロード
        """
        id_length = int.from_bytes(data_payload[:1], byteorder="little")
        data_id = data_payload[1 : 1 + id_length].decode("utf-8")
        value = data_payload[1 + id_length :]
        return Bytes(data_id=data_id, value=value)

    @property
    def data(self):
        return self.value


class Basetime(Data):
    """基準時刻を表すデータオブジェクトです。

    Attributes:
        type (BasetimeType): 基準時刻種別
        basetime (pandas.Timestamp): 基準時刻
    """

    data_type = _models.DataType.basetime
    """データタイプ
    """

    def __init__(self, type, basetime):
        self.type = type
        self.basetime = basetime

    def __str__(self) -> str:
        return "data_type: {data_type}\ntype: {type}\nbasetime: {basetime}".format(
            data_type=self.data_type.name, type=self.type, basetime=self.basetime
        )

    @staticmethod
    def _read_from(rd):
        basetime_type = _binaly_utils.read_uint_from(rd, 1)
        sec = _binaly_utils.read_uint_from(rd, 4)
        nsec = _binaly_utils.read_uint_from(rd, 4)
        basetime = pd.Timestamp(
            sec * 1_000_000_000 + nsec,
            tzinfo=pytz.utc,
        )
        return Basetime(type=basetime_type, basetime=basetime)

    def _write_to(self, wr):
        _binaly_utils.write_uint_to(wr, self.type, 1)
        sec = self.basetime.value // 1_000_000_000
        nsec = self.basetime.value - sec * 1_000_000_000
        _binaly_utils.write_uint_to(wr, sec, 4)
        _binaly_utils.write_uint_to(wr, nsec, 4)

    @staticmethod
    def from_payload(data_payload):
        """データのペイロードを Basetime オブジェクトに変換します。

        Args:
            data_payload(bytes): データのペイロード
        """
        sec = int.from_bytes(data_payload[1:5], byteorder="little")
        nsec = int.from_bytes(data_payload[5:9], byteorder="little")
        return Basetime(
            type=data_payload[0],
            basetime=pd.Timestamp(sec * 1_000_000_000 + nsec),
        )


def type_to_data_class(t):
    if t == _models.DataType.can:
        return CAN
    elif t == _models.DataType.nmea:
        return NMEA
    elif t == _models.DataType.general_sensor:
        return GeneralSensor
    elif t == _models.DataType.jpeg:
        return JPEG
    elif t == _models.DataType.controlpad:
        return Controlpad
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
    elif t == _models.DataType.basetime:
        return Basetime
    elif t == _models.DataType.h264:
        return H264
    elif t == _models.DataType.aac:
        return AAC
    elif t == _models.DataType.pcm:
        return PCM

    raise NotImplementedError
