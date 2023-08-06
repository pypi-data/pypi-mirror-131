from typing import Tuple
from enum import Enum

from .util import probe

class EnumEndian(Enum):
    LITTLE_ENDIAN=0
    BIG_ENDIAN=1

class EnumFieldType(Enum):
    BYTE=1
    ASCII=2
    SHORT=3
    LONG=4

def get_byte_length(field_type: EnumFieldType) -> int:
    if field_type == EnumFieldType.BYTE:
        return 1
    if field_type == EnumFieldType.ASCII:
        return 1
    if field_type == EnumFieldType.SHORT:
        return 2
    if field_type == EnumFieldType.LONG:
        return 4
    raise RuntimeError(f"get_byte_length did not receive a valid field_type")

def read_buf(buf: bytes, offset: int, field_type: EnumFieldType, endianess: EnumEndian):
    byte_length = get_byte_length(field_type)
    if endianess == EnumEndian.LITTLE_ENDIAN:
        _en = 'little'
    if endianess == EnumEndian.BIG_ENDIAN:
        _en = 'big'

    if field_type == EnumFieldType.BYTE:
        return int.from_bytes(buf[offset : offset+byte_length], _en)
    if field_type == EnumFieldType.SHORT:
        return int.from_bytes(buf[offset : offset+byte_length], _en)
    if field_type == EnumFieldType.LONG:
        return int.from_bytes(buf[offset : offset+byte_length], _en)
    raise NotImplementedError(f"not yet implemented? for type {field_type}")

def read_single_entry(buf: bytes, offset: int, endianness: EnumEndian):
    return (
        read_buf(buf, offset, EnumFieldType.SHORT, endianness),
        read_buf(buf, offset+2, EnumFieldType.SHORT, endianness),
        read_buf(buf, offset+4, EnumFieldType.LONG, endianness),
        read_buf(buf, offset+8, EnumFieldType.LONG, endianness),
    )

def read_dir(url: str, offset: int, endianess: EnumEndian, headers=None) -> Tuple[int, int]:
    raw = probe(url, (offset, offset + 2), headers=headers)
    no_fields = read_buf(raw, 0, EnumFieldType.SHORT, endianess)

    raw_dir = probe(url, (offset + 2, offset + 2 + no_fields * 12 + 2), headers=headers)
    dirs = [read_single_entry(raw_dir, idx * 12, endianess) for idx in range(no_fields)]
    width_dir = [dir for dir in dirs if dir[0] == 256]
    height_dir = [dir for dir in dirs if dir[0] == 257]
    if len(width_dir) == 0:
        raise RuntimeError(f"width metadata does not exist")
    if len(height_dir) == 0:
        raise RuntimeError(f"height metadata does not exist")
    return (width_dir[0][3], height_dir[0][3])

def get_tiff_header(url: str, headers=None) -> Tuple[EnumEndian, int]:
    raw = probe(url, (0,7), headers=headers)
    
    byte_order_bytes = raw[:2].decode('utf-8')
    assert byte_order_bytes == 'II' or byte_order_bytes == 'MM'

    if byte_order_bytes == 'II':
        byte_order = EnumEndian.LITTLE_ENDIAN
    if byte_order_bytes == 'MM':
        byte_order = EnumEndian.BIG_ENDIAN
    
    magic_bytes = read_buf(raw, 2, EnumFieldType.SHORT, byte_order)
    assert magic_bytes == 42, f'magic number for tiff should be 42, but is instead {magic_bytes}'

    first_dir = read_buf(raw, 4, EnumFieldType.LONG, byte_order)
    return (byte_order, first_dir)


def try_tiff(url, headers=None) -> Tuple[int, int]:
    byte_order, first_dir = get_tiff_header(url, headers=headers)
    return read_dir(url, first_dir, byte_order, headers=headers)
