#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HeadTable class - Font header table
"""

from .table import Table


class HeadTable(Table):
    """
    'head' table - Font Header

    Contains global information about the font such as:
    - Font version
    - Units per EM
    - Creation/modification dates
    - Bounding box
    - Magic number
    - Direction settings
    """

    def __init__(self, directory_entry, data: bytes):
        """
        Initialize HeadTable.

        Args:
            directory_entry: DirectoryEntry for this table
            data: Table data
        """
        super().__init__(directory_entry)

        if len(data) < 54:
            raise ValueError("Insufficient data for head table")

        self.version = int.from_bytes(data[0:4], byteorder='big')
        self.font_revision = int.from_bytes(data[4:8], byteorder='big')
        self.checksum_adjustment = int.from_bytes(data[8:12], byteorder='big')
        self.magic_number = int.from_bytes(data[12:16], byteorder='big')

        if self.magic_number != 0x5F0F3CF5:
            raise ValueError(f"Invalid magic number in head table: 0x{self.magic_number:08X}")

        self.flags = int.from_bytes(data[16:18], byteorder='big', signed=False)
        self.units_per_em = int.from_bytes(data[18:20], byteorder='big', signed=False)
        self.created = int.from_bytes(data[20:28], byteorder='big')
        self.modified = int.from_bytes(data[28:36], byteorder='big')
        self.x_min = int.from_bytes(data[36:38], byteorder='big', signed=True)
        self.y_min = int.from_bytes(data[38:40], byteorder='big', signed=True)
        self.x_max = int.from_bytes(data[40:42], byteorder='big', signed=True)
        self.y_max = int.from_bytes(data[42:44], byteorder='big', signed=True)
        self.mac_style = int.from_bytes(data[44:46], byteorder='big', signed=False)
        self.lowest_rec_ppem = int.from_bytes(data[46:48], byteorder='big', signed=False)
        self.font_direction_hint = int.from_bytes(data[48:50], byteorder='big', signed=True)
        self.index_to_loc_format = int.from_bytes(data[50:52], byteorder='big', signed=True)
        self.glyph_data_format = int.from_bytes(data[52:54], byteorder='big', signed=True)

    def get_version(self) -> float:
        """Get font version as float."""
        return self.version / 65536.0

    def get_font_revision(self) -> float:
        """Get font revision as float."""
        return self.font_revision / 65536.0

    def get_units_per_em(self) -> int:
        """Get units per EM square."""
        return self.units_per_em

    def get_x_min(self) -> int:
        """Get minimum x coordinate."""
        return self.x_min

    def get_y_min(self) -> int:
        """Get minimum y coordinate."""
        return self.y_min

    def get_x_max(self) -> int:
        """Get maximum x coordinate."""
        return self.x_max

    def get_y_max(self) -> int:
        """Get maximum y coordinate."""
        return self.y_max

    def get_index_to_loc_format(self) -> int:
        """Get index to loc format (0=short, 1=long)."""
        return self.index_to_loc_format

    def to_string(self) -> str:
        """Get string representation."""
        return (
            f"head: Header Table\n"
            f"  'version'           {self.get_version():.4f}\n"
            f"  'fontRevision'       {self.get_font_revision():.4f}\n"
            f"  'checkSumAdjustment' 0x{self.checksum_adjustment:08X}\n"
            f"  'magicNumber'        0x{self.magic_number:08X}\n"
            f"  'flags'              0x{self.flags:04X}\n"
            f"  'unitsPerEm'         {self.units_per_em}\n"
            f"  'created'            {self.created}\n"
            f"  'modified'           {self.modified}\n"
            f"  'xMin'               {self.x_min}\n"
            f"  'yMin'               {self.y_min}\n"
            f"  'xMax'               {self.x_max}\n"
            f"  'yMax'               {self.y_max}\n"
            f"  'macStyle'           0x{self.mac_style:04X}\n"
            f"  'lowestRecPPEM'      {self.lowest_rec_ppem}\n"
            f"  'fontDirectionHint'   {self.font_direction_hint}\n"
            f"  'indexToLocFormat'    {self.index_to_loc_format}\n"
            f"  'glyphDataFormat'     {self.glyph_data_format}"
        )
