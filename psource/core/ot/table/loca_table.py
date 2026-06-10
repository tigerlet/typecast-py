#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LocaTable class - Index to Location table
"""

from .table import Table


class LocaTable(Table):
    """
    'loca' table - Index to Location

    Contains offsets to the beginning of each glyph description in the glyf table.
    The format can be short (2 bytes) or long (4 bytes) offsets.
    """

    def __init__(self, directory_entry, data: bytes, num_glyphs: int = 0, index_to_loc_format: int = 0):
        """
        Initialize LocaTable.

        Args:
            directory_entry: DirectoryEntry for this table
            data: Table data
            num_glyphs: Number of glyphs from maxp table
            index_to_loc_format: Format from head table (0=short, 1=long)
        """
        super().__init__(directory_entry)
        self._data = data
        self.num_glyphs = num_glyphs
        self.index_to_loc_format = index_to_loc_format
        self.offsets = []

        self._parse_offsets()

    def _parse_offsets(self):
        """Parse offsets from the table data."""
        data = self._data
        self.offsets = []

        if self.index_to_loc_format == 0:
            for i in range(self.num_glyphs + 1):
                offset = i * 2
                if offset + 2 > len(data):
                    break
                self.offsets.append(int.from_bytes(data[offset:offset+2], byteorder='big', signed=False) * 2)
        else:
            for i in range(self.num_glyphs + 1):
                offset = i * 4
                if offset + 4 > len(data):
                    break
                self.offsets.append(int.from_bytes(data[offset:offset+4], byteorder='big', signed=False))

    def init(self, num_glyphs: int, short_format: bool):
        """
        Initialize loca table with specific parameters.

        Args:
            num_glyphs: Number of glyphs
            short_format: True if using short format (2 bytes), False for long (4 bytes)
        """
        self.num_glyphs = num_glyphs
        self.index_to_loc_format = 0 if short_format else 1
        self._parse_offsets()

    def get_num_glyphs(self) -> int:
        """Get number of glyphs."""
        return self.num_glyphs

    def get_offset(self, index: int) -> int:
        """
        Get offset for glyph index.

        Args:
            index: Glyph index

        Returns:
            Offset to glyph description in glyf table
        """
        if 0 <= index < len(self.offsets):
            return self.offsets[index]
        elif self.offsets:
            return self.offsets[-1]
        return 0

    def get_glyph_length(self, index: int) -> int:
        """
        Get length of glyph at index.

        Args:
            index: Glyph index

        Returns:
            Length of glyph description
        """
        if 0 <= index < len(self.offsets) - 1:
            return self.offsets[index + 1] - self.offsets[index]
        elif index == len(self.offsets) - 1 and self.offsets:
            return 0
        return 0

    def to_string(self) -> str:
        """Get string representation."""
        format_str = "short" if self.index_to_loc_format == 0 else "long"
        return (
            f"loca: Index to Location\n"
            f"  Number of glyphs: {self.num_glyphs}\n"
            f"  Format: {format_str}"
        )
