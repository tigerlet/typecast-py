#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DirectoryEntry class - Represents an entry in the table directory
"""

from ..fixed import Fixed


class DirectoryEntry:
    """
    Represents an entry in the font's table directory.

    Each table in the font has a DirectoryEntry that contains:
    - Tag: 4-byte identifier
    - Checksum: Data checksum
    - Offset: Offset to table data from start of file
    - Length: Length of table data
    """

    def __init__(self, data: bytes, offset: int = 0):
        """Initialize a DirectoryEntry from binary data."""
        if offset + 16 > len(data):
            raise ValueError(f'Insufficient data for DirectoryEntry at offset {offset}')

        self.tag = int.from_bytes(data[offset:offset+4], byteorder='big')
        self.checksum = int.from_bytes(data[offset+4:offset+8], byteorder='big')
        self.offset = int.from_bytes(data[offset+8:offset+12], byteorder='big')
        self.length = int.from_bytes(data[offset+12:offset+16], byteorder='big')

    def __repr__(self):
        """String representation."""
        from ..fixed import Fixed
        tag_str = Fixed.tag_to_string(self.tag)
        return f"DirectoryEntry(tag='{tag_str}', checksum=0x{self.checksum:08X}, offset={self.offset}, length={self.length})"

    def __eq__(self, other):
        """Check equality."""
        if not isinstance(other, DirectoryEntry):
            return False
        return (self.tag == other.tag and
                self.checksum == other.checksum and
                self.offset == other.offset and
                self.length == other.length)

    def clone(self):
        """Create a copy of this entry."""
        return DirectoryEntry.__new__(DirectoryEntry)
