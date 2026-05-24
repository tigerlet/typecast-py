#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OTFontCollection class - Represents a collection of OpenType fonts
"""

import os
from typing import List
from .otfont import OTFont


class OTFontCollection:
    """
    Represents a collection of one or more fonts.

    Can contain:
    - A single font (TTF/OTF)
    - Multiple fonts (TTC - TrueType Collection)
    - Mac DFont resource
    """

    def __init__(self):
        """Initialize the font collection."""
        self._path_name = None
        self._file_name = None
        self._ttc_header = None
        self._fonts: List[OTFont] = []
        self._tables = []

    @classmethod
    def create(cls, file_path: str) -> 'OTFontCollection':
        """Create a font collection from a file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'Font file not found: {file_path}')

        fc = cls()
        fc._read(file_path)
        return fc

    def _read(self, file_path: str):
        """Read a font file."""
        self._path_name = file_path
        self._file_name = os.path.basename(file_path)

        with open(file_path, 'rb') as f:
            data = f.read()

        if self._is_ttc(data):
            self._read_ttc(data)
        elif self._file_name.endswith('.dfont'):
            self._read_dfont(data)
        else:
            self._read_single_font(data)

    def _is_ttc(self, data: bytes) -> bool:
        """Check if this is a TrueType Collection."""
        if len(data) < 12:
            return False
        tag = data[0:4]
        return tag == b'ttcf'

    def _read_single_font(self, data: bytes):
        """Read a single font."""
        font = OTFont(self)
        font.read(data, 0, 0)
        self._fonts.append(font)

    def _read_ttc(self, data: bytes):
        """Read a TrueType Collection."""
        pass

    def _read_dfont(self, data: bytes):
        """Read a Mac DFont resource."""
        pass

    def get_path_name(self) -> str:
        """Get the full path name."""
        return self._path_name

    def get_file_name(self) -> str:
        """Get the file name."""
        return self._file_name

    def get_font(self, index: int) -> OTFont:
        """Get a font by index."""
        if 0 <= index < len(self._fonts):
            return self._fonts[index]
        return None

    def get_font_count(self) -> int:
        """Get the number of fonts in the collection."""
        return len(self._fonts)

    def get_ttc_header(self):
        """Get the TTC header if this is a collection."""
        return self._ttc_header

    def add_table(self, table):
        """Add a table to the collection."""
        self._tables.append(table)

    def get_table(self, index: int):
        """Get a table by index."""
        if 0 <= index < len(self._tables):
            return self._tables[index]
        return None

    def to_string(self) -> str:
        """Get string representation."""
        return f"OTFontCollection: {self._file_name} ({len(self._fonts)} fonts)"
