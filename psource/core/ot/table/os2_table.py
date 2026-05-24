#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Os2Table class - OS/2 and Windows Metrics table
"""

from .table import Table


class Os2Table(Table):
    """
    'OS/2' table - OS/2 and Windows Metrics

    Contains metadata about the font including:
    - Version
    - Average character width
    - Weight and width classes
    - Font type flags
    - Subscript/superscript sizes
    - Strikeout information
    - Family class
    - PANOSE classification
    - Unicode ranges
    - Vendor ID
    - Selection flags
    - Character indexes
    - Typographic metrics
    - Windows metrics
    - Code page ranges
    """

    def __init__(self, directory_entry, data: bytes):
        """
        Initialize Os2Table.

        Args:
            directory_entry: DirectoryEntry for this table
            data: Table data
        """
        super().__init__(directory_entry)
        self._data = data
        self._parse(data)

    def _parse(self, data: bytes):
        """Parse OS/2 table data."""
        if len(data) < 78:
            return

        self.version = int.from_bytes(data[0:2], byteorder='big', signed=False)
        self.x_avg_char_width = int.from_bytes(data[2:4], byteorder='big', signed=True)
        self.us_weight_class = int.from_bytes(data[4:6], byteorder='big', signed=False)
        self.us_width_class = int.from_bytes(data[6:8], byteorder='big', signed=False)
        self.fs_type = int.from_bytes(data[8:10], byteorder='big', signed=False)

        if len(data) >= 10:
            self.y_subscript_x_size = int.from_bytes(data[10:12], byteorder='big', signed=True)
            self.y_subscript_y_size = int.from_bytes(data[12:14], byteorder='big', signed=True)
            self.y_subscript_x_offset = int.from_bytes(data[14:16], byteorder='big', signed=True)
            self.y_subscript_y_offset = int.from_bytes(data[16:18], byteorder='big', signed=True)
            self.y_superscript_x_size = int.from_bytes(data[18:20], byteorder='big', signed=True)
            self.y_superscript_y_size = int.from_bytes(data[20:22], byteorder='big', signed=True)
            self.y_superscript_x_offset = int.from_bytes(data[22:24], byteorder='big', signed=True)
            self.y_superscript_y_offset = int.from_bytes(data[24:26], byteorder='big', signed=True)
            self.y_strikeout_size = int.from_bytes(data[26:28], byteorder='big', signed=True)
            self.y_strikeout_position = int.from_bytes(data[28:30], byteorder='big', signed=True)
            self.s_family_class = int.from_bytes(data[30:32], byteorder='big', signed=True)

        if len(data) >= 42:
            self.panose = []
            for i in range(10):
                self.panose.append(data[32 + i])

        if len(data) >= 54:
            self.unicode_range_1 = int.from_bytes(data[42:46], byteorder='big', signed=False)
            self.unicode_range_2 = int.from_bytes(data[46:50], byteorder='big', signed=False)
            self.unicode_range_3 = int.from_bytes(data[50:54], byteorder='big', signed=False)

        if len(data) >= 58:
            self.unicode_range_4 = int.from_bytes(data[54:58], byteorder='big', signed=False)

        if len(data) >= 62:
            self.ach_vend_id = data[58:62].decode('ascii', errors='replace').strip('\x00')

        if len(data) >= 64:
            self.fs_selection = int.from_bytes(data[62:64], byteorder='big', signed=False)

        if len(data) >= 72:
            self.us_first_char_index = int.from_bytes(data[64:66], byteorder='big', signed=False)
            self.us_last_char_index = int.from_bytes(data[66:68], byteorder='big', signed=False)
            self.s_typo_ascender = int.from_bytes(data[68:70], byteorder='big', signed=True)
            self.s_typo_descender = int.from_bytes(data[70:72], byteorder='big', signed=True)
            self.s_typo_line_gap = int.from_bytes(data[72:74], byteorder='big', signed=True)
            self.us_win_ascent = int.from_bytes(data[74:76], byteorder='big', signed=False)
            self.us_win_descent = int.from_bytes(data[76:78], byteorder='big', signed=False)

        if len(data) >= 86:
            self.code_page_range_1 = int.from_bytes(data[78:82], byteorder='big', signed=False)
            self.code_page_range_2 = int.from_bytes(data[82:86], byteorder='big', signed=False)

    def to_string(self) -> str:
        """Get string representation."""
        result = "'OS/2' Table - OS/2 and Windows Metrics\n"
        result += "----------------------------------------\n\n"
        
        result += "'OS/2' version:\t\t{:d}\n".format(self.version)
        result += "xAvgCharWidth:\t\t{:d}\n".format(self.x_avg_char_width)
        result += "usWeightClass:\t\t{:d}\n".format(self.us_weight_class)
        result += "usWidthClass:\t\t{:d}\n".format(self.us_width_class)
        result += "fsType:\t\t\t0x{:04X}\n".format(self.fs_type)
        
        if hasattr(self, 'y_subscript_x_size'):
            result += "ySubscriptXSize:\t{:d}\n".format(self.y_subscript_x_size)
            result += "ySubscriptYSize:\t{:d}\n".format(self.y_subscript_y_size)
            result += "ySubscriptXOffset:\t{:d}\n".format(self.y_subscript_x_offset)
            result += "ySubscriptYOffset:\t{:d}\n".format(self.y_subscript_y_offset)
            result += "ySuperscriptXSize:\t{:d}\n".format(self.y_superscript_x_size)
            result += "ySuperscriptYSize:\t{:d}\n".format(self.y_superscript_y_size)
            result += "ySuperscriptXOffset:\t{:d}\n".format(self.y_superscript_x_offset)
            result += "ySuperscriptYOffset:\t{:d}\n".format(self.y_superscript_y_offset)
            result += "yStrikeoutSize:\t\t{:d}\n".format(self.y_strikeout_size)
            result += "yStrikeoutPosition:\t{:d}\n".format(self.y_strikeout_position)
            
            subclass = (self.s_family_class >> 8) & 0xFF
            result += "sFamilyClass:\t\t{:d}\tsubclass = {:d}\n".format(self.s_family_class, subclass)

        if hasattr(self, 'panose'):
            result += "PANOSE:\t\t\t"
            result += ' '.join(str(p) for p in self.panose) + "\n"

        if hasattr(self, 'unicode_range_1'):
            result += "Unicode Range 1( Bits 0 - 31 ):\t0x{:08X}\n".format(self.unicode_range_1)
            result += "Unicode Range 2( Bits 32- 63 ):\t0x{:08X}\n".format(self.unicode_range_2)
            result += "Unicode Range 3( Bits 64- 95 ):\t0x{:08X}\n".format(self.unicode_range_3)

        if hasattr(self, 'unicode_range_4'):
            result += "Unicode Range 4( Bits 96-127 ):\t0x{:08X}\n".format(self.unicode_range_4)

        if hasattr(self, 'ach_vend_id'):
            result += "achVendID:\t\t'{:s}'\n".format(self.ach_vend_id)

        if hasattr(self, 'fs_selection'):
            result += "fsSelection:\t\t0x{:04X}\n".format(self.fs_selection)

        if hasattr(self, 'us_first_char_index'):
            result += "usFirstCharIndex:\t0x{:04X}\n".format(self.us_first_char_index)
            result += "usLastCharIndex:\t0x{:04X}\n".format(self.us_last_char_index)
            result += "sTypoAscender:\t\t{:d}\n".format(self.s_typo_ascender)
            result += "sTypoDescender:\t\t{:d}\n".format(self.s_typo_descender)
            result += "sTypoLineGap:\t\t{:d}\n".format(self.s_typo_line_gap)
            result += "usWinAscent:\t\t{:d}\n".format(self.us_win_ascent)
            result += "usWinDescent:\t\t{:d}\n".format(self.us_win_descent)

        if hasattr(self, 'code_page_range_1'):
            result += "CodePage Range 1( Bits 0 - 31 ):\t0x{:08X}\n".format(self.code_page_range_1)
            result += "CodePage Range 2( Bits 32- 63 ):\t0x{:08X}\n".format(self.code_page_range_2)

        return result