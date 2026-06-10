#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fixed class - Represents 16.16 fixed point numbers used in OpenType fonts
"""

class Fixed:
    """
    Represents 16.16 fixed point numbers.

    OpenType uses 16.16 fixed point format for certain values:
    - High 16 bits: integer part
    - Low 16 bits: fractional part

    Examples:
        0x00010000 = 1.0
        0x00008000 = 0.5
        0x0000C000 = 0.75
    """

    @staticmethod
    def float_value(fixed_int: int) -> float:
        """Convert fixed point integer to float."""
        return fixed_int / 65536.0

    @staticmethod
    def int_value(float_val: float) -> int:
        """Convert float to fixed point integer."""
        return int(float_val * 65536)

    @staticmethod
    def read(data: bytes, offset: int) -> int:
        """Read a 4-byte fixed point value from data at offset."""
        return int.from_bytes(data[offset:offset+4], byteorder='big', signed=True)

    @staticmethod
    def tag_to_string(tag: int) -> str:
        """Convert a 4-byte tag integer to a string."""
        return bytes([
            (tag >> 24) & 0xFF,
            (tag >> 16) & 0xFF,
            (tag >> 8) & 0xFF,
            tag & 0xFF
        ]).decode('latin-1')

    @staticmethod
    def string_to_tag(s: str) -> int:
        """Convert a 4-character string tag to an integer."""
        if len(s) != 4:
            raise ValueError(f"Tag must be exactly 4 characters, got '{s}'")
        return (ord(s[0]) << 24) | (ord(s[1]) << 16) | (ord(s[2]) << 8) | ord(s[3])
