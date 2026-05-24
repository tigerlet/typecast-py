#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MaxpTable class - Maximum Profile table
"""

from .table import Table


class MaxpTable(Table):
    """
    'maxp' table - Maximum Profile

    Contains the maximum values for various font metrics and limits.
    The format varies depending on the font type (TrueType vs CFF).
    """

    def __init__(self, directory_entry, data: bytes):
        """
        Initialize MaxpTable.

        Args:
            directory_entry: DirectoryEntry for this table
            data: Table data
        """
        super().__init__(directory_entry)

        if len(data) < 6:
            raise ValueError("Insufficient data for maxp table")

        self.version = int.from_bytes(data[0:4], byteorder='big')
        self.num_glyphs = int.from_bytes(data[4:6], byteorder='big', signed=False)

    def get_version(self) -> float:
        """Get maxp version as float."""
        return self.version / 65536.0

    def get_num_glyphs(self) -> int:
        """Get number of glyphs in font."""
        return self.num_glyphs

    def to_string(self) -> str:
        """Get string representation."""
        return (
            f"maxp: Maximum Profile\n"
            f"  'version'      {self.get_version():.4f}\n"
            f"  'numGlyphs'     {self.num_glyphs}"
        )
