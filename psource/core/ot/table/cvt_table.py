#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CvtTable class - Control Value Table
"""

from .table import Table


class CvtTable(Table):
    """
    'cvt ' table - Control Value Table
    
    Contains a list of values used by the TrueType hinting instructions.
    """

    def __init__(self, directory_entry, data: bytes):
        """
        Initialize CvtTable.

        Args:
            directory_entry: DirectoryEntry for this table
            data: Table data
        """
        super().__init__(directory_entry)
        self._data = data
        self._values = []
        self._parse()

    def _parse(self):
        """Parse the control value table."""
        length = len(self._data) // 2
        for i in range(length):
            value = int.from_bytes(
                self._data[i*2:(i+1)*2],
                byteorder='big',
                signed=True
            )
            self._values.append(value)

    def get_values(self):
        """Get the control values."""
        return self._values

    def to_string(self) -> str:
        """Get string representation."""
        result = "'cvt ' Table - Control Value Table\n"
        result += "----------------------------------\n"
        result += f"Size = {len(self._data)} bytes, {len(self._values)} entries\n"
        result += "        Values\n"
        result += "        ------\n"
        for i, value in enumerate(self._values):
            result += f"        {i}: {value}\n"
        return result