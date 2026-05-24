#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TableFactory class - Factory for creating table instances
"""

from .table import Table
from .head_table import HeadTable
from .maxp_table import MaxpTable
from .glyf_table import GlyfTable
from .loca_table import LocaTable
from .hhea_table import HheaTable
from .hmtx_table import HmtxTable
from .os2_table import Os2Table
from .cvt_table import CvtTable
from .cmap_table import CmapTable
from .nam_table import NameTable
from .dsig_table import DsigTable


class TableFactory:
    """
    Factory class for creating OpenType table instances.

    Maps table type tags to their corresponding classes.
    """

    TABLE_TYPES = {
        0x68656164: HeadTable,    # 'head'
        0x6D617870: MaxpTable,   # 'maxp'
        0x676C7966: GlyfTable,   # 'glyf'
        0x6C6F6361: LocaTable,   # 'loca'
        0x68686561: HheaTable,    # 'hhea'
        0x686D7478: HmtxTable,    # 'hmtx'
        0x4F532F32: Os2Table,     # 'OS/2'
        0x63767420: CvtTable,     # 'cvt '
        0x636D6170: CmapTable,    # 'cmap'
        0x6E616D65: NameTable,    # 'name'
        0x44534947: DsigTable,    # 'DSIG'
    }

    @staticmethod
    def create(directory_entry, data: bytes) -> Table:
        """
        Create a table instance based on directory entry.

        Args:
            directory_entry: DirectoryEntry with tag
            data: Table data

        Returns:
            Table instance
        """
        tag = directory_entry.tag
        table_class = TableFactory.TABLE_TYPES.get(tag)

        if table_class:
            return table_class(directory_entry, data)

        return GenericTable(directory_entry, data)


class GenericTable(Table):
    """
    Generic table implementation for unsupported table types.
    """

    def __init__(self, directory_entry, data: bytes):
        """
        Initialize generic table.

        Args:
            directory_entry: DirectoryEntry for this table
            data: Table data
        """
        super().__init__(directory_entry)
        self._data = data

    def get_data(self) -> bytes:
        """Get raw table data."""
        return self._data

    def get_type(self) -> int:
        """Get table type tag."""
        return self._directory_entry.tag
