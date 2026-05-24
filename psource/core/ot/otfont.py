#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OTFont class - Represents a single OpenType font
"""

from typing import List, Dict
from .table.table import Table
from .table.table_directory import TableDirectory
from .glyph import Glyph


class OTFont:
    """
    Represents a single OpenType font within a collection.

    A font contains multiple tables that store different
    aspects of the font data.
    """

    def __init__(self, font_collection):
        """Initialize the font."""
        self._font_collection = font_collection
        self._table_directory = None
        self._tables: Dict[int, Table] = {}
        self._os2 = None
        self._cmap = None
        self._glyf = None
        self._head = None
        self._hhea = None
        self._hmtx = None
        self._loca = None
        self._maxp = None
        self._name = None
        self._post = None

    def read(self, data: bytes, directory_offset: int, tables_origin: int):
        """Read font data from binary data."""
        self._table_directory = TableDirectory(data[directory_offset:])

        for i in range(self._table_directory.get_num_tables()):
            entry = self._table_directory.get_entry(i)
            offset = tables_origin + entry.offset
            table_data = data[offset:offset + entry.length]
            table = self._create_table(entry, table_data)
            if table:
                self._tables[entry.tag] = table

        self._os2 = self._tables.get(1330851634)
        self._cmap = self._tables.get(1668112752)
        self._glyf = self._tables.get(1735162214)
        self._head = self._tables.get(1751474532)
        self._hhea = self._tables.get(1751672161)
        self._hmtx = self._tables.get(1752003704)
        self._loca = self._tables.get(1819239265)
        self._maxp = self._tables.get(1835104368)
        self._name = self._tables.get(1851878757)
        self._post = self._tables.get(1886352244)

        if self._hmtx and self._hhea and self._maxp:
            self._hmtx.init(self._hhea.get_number_of_h_metrics(), self._maxp.get_num_glyphs() - self._hhea.get_number_of_h_metrics())

        if self._loca and self._head and self._maxp:
            self._loca.init(self._maxp.get_num_glyphs(), self._head.get_index_to_loc_format() == 0)

        if self._glyf and self._maxp and self._loca:
            self._glyf.init(self._maxp.get_num_glyphs(), self._loca)

    def _create_table(self, entry, data: bytes) -> Table:
        """Create a table from directory entry and data."""
        from .table import table_factory
        return table_factory.TableFactory.create(entry, data)

    def get_table(self, table_type: int) -> Table:
        """Get a table by type."""
        return self._tables.get(table_type)

    def get_os2_table(self):
        """Get the OS/2 table."""
        return self._os2

    def get_cmap_table(self):
        """Get the cmap table."""
        return self._cmap

    def get_head_table(self):
        """Get the head table."""
        return self._head

    def get_hhea_table(self):
        """Get the hhea table."""
        return self._hhea

    def get_hmtx_table(self):
        """Get the hmtx table."""
        return self._hmtx

    def get_loca_table(self):
        """Get the loca table."""
        return self._loca

    def get_maxp_table(self):
        """Get the maxp table."""
        return self._maxp

    def get_name_table(self):
        """Get the name table."""
        return self._name

    def get_post_table(self):
        """Get the post table."""
        return self._post

    def get_glyf_table(self):
        """Get the glyf table."""
        return self._glyf

    def get_ascent(self) -> int:
        """Get the font ascent."""
        if self._hhea:
            return self._hhea.get_ascent()
        return 0

    def get_descent(self) -> int:
        """Get the font descent."""
        if self._hhea:
            return self._hhea.get_descent()
        return 0

    def get_num_glyphs(self) -> int:
        """Get the number of glyphs in the font."""
        if self._maxp:
            return self._maxp.get_num_glyphs()
        return 0

    def get_glyph(self, index: int) -> Glyph:
        """Get a glyph by index."""
        if not self._glyf or not self._hmtx:
            return None

        description = self._glyf.get_glyph(index)
        if not description:
            return None

        lsb = self._hmtx.get_left_side_bearing(index)
        advance = self._hmtx.get_advance_width(index)
        return Glyph(description, lsb, advance)

    def get_table_directory(self) -> TableDirectory:
        """Get the table directory."""
        return self._table_directory

    def to_string(self) -> str:
        """Get string representation."""
        if self._table_directory:
            return self._table_directory.to_string()
        return "Empty font"
