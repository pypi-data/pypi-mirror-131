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
import struct
import uuid


def read_bytes_from(rd, nbytes) -> bytes:
    if nbytes == 0:
        return b""

    bs = rd.read(nbytes)
    if len(bs) == 0:
        raise EOFError

    if len(bs) < nbytes:
        raise ValueError

    return bs


def read_allbytes_from(rd) -> bytes:
    bs = rd.read()
    if len(bs) == 0:
        raise EOFError

    return bs


def read_uuid_from(rd) -> str:
    bs = read_bytes_from(rd, 16)
    return str(uuid.UUID(bytes=bs))


def read_uint_from(rd, nbytes) -> int:
    bs = read_bytes_from(rd, nbytes)
    return int.from_bytes(bs, "little")


def read_float64_from(rd) -> float:
    bs = read_bytes_from(rd, 8)
    return struct.unpack("<d", bs)[0]


def read_int64_from(rd) -> int:
    bs = read_bytes_from(rd, 8)
    return struct.unpack("<q", bs)[0]


def read_variable_uint8to32_from(rd) -> (int, int):
    bs = read_bytes_from(rd, 1)

    remain = bs[0] & 0b11
    length = remain + 1

    if 0 < remain:
        bs += read_bytes_from(rd, remain)

    return int.from_bytes(bs, "little") >> 2, length


def read_variable_uint16to24_from(rd) -> (int, int):
    bs = read_bytes_from(rd, 2)

    remain = bs[0] & 0b01
    length = remain + 2

    if 0 < remain:
        bs += read_bytes_from(rd, remain)

    return int.from_bytes(bs, "little") >> 1, length


def read_variable_uint16to32_from(rd) -> (int, int):
    bs = read_bytes_from(rd, 2)

    remain = bs[0] & 0b11
    length = remain + 2

    if 0 < remain:
        bs += read_bytes_from(rd, remain)

    return int.from_bytes(bs, "little") >> 2, length


def write_bytes_to(wr, bs):
    wr.write(bs)


def write_uuid_to(wr, u):
    bs = uuid.UUID(f"{{{u}}}").bytes
    wr.write(bs)


def write_uint_to(wr, u, nbytes):
    bs = u.to_bytes(nbytes, "little")
    wr.write(bs)


def write_float64_to(wr, f):
    bs = struct.pack("<d", f)
    wr.write(bs)


def write_int64_to(wr, i):
    bs = struct.pack("<q", i)
    wr.write(bs)


def write_variable_uint8to32_to(wr, u, length):
    if length < 1 or 4 < length:
        raise ValueError

    remain = length - 1
    bs = ((u << 2) | remain).to_bytes(length, "little")
    wr.write(bs)


def write_variable_uint16to24_to(wr, u, length):
    if length < 2 or 3 < length:
        raise ValueError

    remain = length - 2
    bs = ((u << 1) | remain).to_bytes(length, "little")
    wr.write(bs)


def write_variable_uint16to32_to(wr, u, length):
    if length < 2 or 4 < length:
        raise ValueError

    remain = length - 2
    bs = ((u << 2) | remain).to_bytes(length, "little")
    wr.write(bs)
