#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TTCHeader class - TrueType Collection header
"""


class TTCHeader:
    """
    TTC (TrueType Collection) header.

    Contains version and offset table for each font in the collection.
    """

    def __init__(self, data: bytes):
        """
        Initialize TTCHeader.

        Args:
            data: Binary data starting at TTC header
        """
        if len(data) < 12:
            raise ValueError("Insufficient data for TTC header")

        self.tag = int.from_bytes(data[0:4], byteorder='big')
        if self.tag != 0x74746366:
            raise ValueError(f"Not a TTC file: tag=0x{self.tag:08X}")

        self.version = int.from_bytes(data[4:8], byteorder='big')
        self.num_directories = int.from_bytes(data[8:12], byteorder='big', signed=False)

        self.table_directory_offsets = []
        for i in range(self.num_directories):
            offset = int.from_bytes(data[12 + i * 4:16 + i * 4], byteorder='big', signed=False)
            self.table_directory_offsets.append(offset)

    def get_tag(self) -> int:
        """Get TTC tag."""
        return self.tag

    def get_version(self) -> float:
        """Get TTC version as float."""
        return self.version / 65536.0

    def get_directory_count(self) -> int:
        """Get number of directories."""
        return self.num_directories

    def get_table_directory_offset(self, index: int) -> int:
        """
        Get offset to table directory for given font index.

        Args:
            index: Font index

        Returns:
            Offset from start of file
        """
        if 0 <= index < len(self.table_directory_offsets):
            return self.table_directory_offsets[index]
        return 0

    @staticmethod
    def is_ttc(data: bytes) -> bool:
        """
        Check if data is a TTC file.

        Args:
            data: Binary data

        Returns:
            True if TTC
        """
        if len(data) < 4:
            return False
        tag = int.from_bytes(data[0:4], byteorder='big')
        return tag == 0x74746366
