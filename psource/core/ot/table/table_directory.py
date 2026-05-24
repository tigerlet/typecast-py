#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TableDirectory class - Represents the table directory in an OpenType font
"""

from .directory_entry import DirectoryEntry
from ..fixed import Fixed


class TableDirectory:
    """
    Represents the table directory section of an OpenType font.

    The table directory contains metadata about all tables in the font,
    followed by individual directory entries for each table.
    """

    def __init__(self, data: bytes):
        """
        Initialize a TableDirectory from binary data.

        Args:
            data: Binary data starting at the table directory
        """
        if len(data) < 12:
            raise ValueError("Insufficient data for TableDirectory header")

        self.version = int.from_bytes(data[0:4], byteorder='big')
        self.num_tables = int.from_bytes(data[4:6], byteorder='big', signed=False)
        self.search_range = int.from_bytes(data[6:8], byteorder='big', signed=False)
        self.entry_selector = int.from_bytes(data[8:10], byteorder='big', signed=False)
        self.range_shift = int.from_bytes(data[10:12], byteorder='big', signed=False)

        self.entries = []
        for i in range(self.num_tables):
            entry_offset = 12 + i * 16
            self.entries.append(DirectoryEntry(data, entry_offset))

    def get_entry(self, index: int) -> DirectoryEntry:
        """
        Get entry by index.

        Args:
            index: Entry index

        Returns:
            DirectoryEntry object
        """
        return self.entries[index]

    def get_entry_by_tag(self, tag: int) -> DirectoryEntry:
        """
        Get entry by tag.

        Args:
            tag: Tag value to search for

        Returns:
            DirectoryEntry if found, None otherwise
        """
        for entry in self.entries:
            if entry.tag == tag:
                return entry
        return None

    def get_num_tables(self) -> int:
        """Get number of tables."""
        return self.num_tables

    def get_version(self) -> int:
        """Get version."""
        return self.version

    def get_search_range(self) -> int:
        """Get search range."""
        return self.search_range

    def get_entry_selector(self) -> int:
        """Get entry selector."""
        return self.entry_selector

    def get_range_shift(self) -> int:
        """Get range shift."""
        return self.range_shift

    def to_string(self) -> str:
        """Get string representation."""
        lines = [
            "Offset Table",
            "------ -----",
            f"  sfnt version:     {Fixed.float_value(self.version)}",
            f"  numTables =       {self.num_tables}",
            f"  searchRange =     {self.search_range}",
            f"  entrySelector =   {self.entry_selector}",
            f"  rangeShift =      {self.range_shift}",
            "",
        ]

        for i, entry in enumerate(self.entries):
            lines.append(f"{i}. {entry.to_string()}")

        return "\n".join(lines)
