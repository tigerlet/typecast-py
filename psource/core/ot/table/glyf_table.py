#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GlyfTable class - Glyph table
"""

from .table import Table


class GlyfTable(Table):
    """
    'glyf' table - Glyph

    Contains the actual glyph data for each character in the font.
    Glyphs can be simple (made up of outlines) or composite (made up of other glyphs).
    """

    def __init__(self, directory_entry, data: bytes):
        """
        Initialize GlyfTable.

        Args:
            directory_entry: DirectoryEntry for this table
            data: Table data
        """
        super().__init__(directory_entry)
        self._buf = data
        self._descript = []
        self._loca_table = None

    def init(self, num_glyphs: int, loca_table):
        """
        Initialize glyph data using loca table.

        Args:
            num_glyphs: Number of glyphs
            loca_table: LocaTable instance
        """
        self._loca_table = loca_table
        
        if self._buf is None:
            return
        
        self._descript = [None] * num_glyphs
        
        for i in range(num_glyphs):
            length = loca_table.get_offset(i + 1) - loca_table.get_offset(i)
            if length > 0:
                offset = loca_table.get_offset(i)
                glyph_data = self._buf[offset:offset + length]
                
                if len(glyph_data) >= 2:
                    number_of_contours = int.from_bytes(glyph_data[0:2], byteorder='big', signed=True)
                    
                    if number_of_contours >= 0:
                        from .glyf_simple_descript import GlyfSimpleDescript
                        try:
                            self._descript[i] = GlyfSimpleDescript(self, number_of_contours, glyph_data[2:])
                        except Exception:
                            self._descript[i] = None
        
        for i in range(num_glyphs):
            length = loca_table.get_offset(i + 1) - loca_table.get_offset(i)
            if length <= 0:
                continue
            
            offset = loca_table.get_offset(i)
            glyph_data = self._buf[offset:offset + length]
            
            if len(glyph_data) >= 2:
                number_of_contours = int.from_bytes(glyph_data[0:2], byteorder='big', signed=True)
                
                if number_of_contours < 0:
                    from .glyf_composite_descript import GlyfCompositeDescript
                    try:
                        self._descript[i] = GlyfCompositeDescript(self, glyph_data[2:])
                    except Exception:
                        pass
        
        self._buf = None

    def get_description(self, index: int):
        """
        Get glyph description at index.

        Args:
            index: Glyph index

        Returns:
            Glyph description or None
        """
        if 0 <= index < len(self._descript):
            return self._descript[index]
        return None

    def get_glyph(self, index: int):
        """
        Get glyph at index (alias for get_description).

        Args:
            index: Glyph index

        Returns:
            Glyph description or None
        """
        return self.get_description(index)

    def get_glyph_count(self) -> int:
        """Get number of glyphs."""
        return len(self._descript)

    def get_glyph_data(self, index: int) -> bytes:
        """
        Get raw glyph data at index.

        Args:
            index: Glyph index

        Returns:
            Raw glyph data
        """
        if not self._loca_table or self._buf is None:
            return b''

        offset = self._loca_table.get_offset(index)
        length = self._loca_table.get_glyph_length(index)

        if length > 0 and offset + length <= len(self._buf):
            return self._buf[offset:offset + length]

        return b''

    def to_string(self) -> str:
        """Get string representation."""
        return (
            f"glyf: Glyph Table\n"
            f"  Number of glyphs: {len(self._descript)}"
        )