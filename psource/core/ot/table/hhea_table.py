#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HheaTable class - Horizontal Header table
"""

from .table import Table


class HheaTable(Table):
    """
    'hhea' table - Horizontal Header

    Contains information for horizontal layout of text.
    """

    def __init__(self, directory_entry, data: bytes):
        """
        Initialize HheaTable.

        Args:
            directory_entry: DirectoryEntry for this table
            data: Table data
        """
        super().__init__(directory_entry)

        if len(data) < 36:
            raise ValueError("Insufficient data for hhea table")

        self.version = int.from_bytes(data[0:4], byteorder='big')
        self.ascent = int.from_bytes(data[4:6], byteorder='big', signed=True)
        self.descent = int.from_bytes(data[6:8], byteorder='big', signed=True)
        self.line_gap = int.from_bytes(data[8:10], byteorder='big', signed=True)
        self.advance_width_max = int.from_bytes(data[10:12], byteorder='big', signed=False)
        self.min_left_side_bearing = int.from_bytes(data[12:14], byteorder='big', signed=True)
        self.min_right_side_bearing = int.from_bytes(data[14:16], byteorder='big', signed=True)
        self.x_max_extent = int.from_bytes(data[16:18], byteorder='big', signed=True)
        self.caret_slope_rise = int.from_bytes(data[18:20], byteorder='big', signed=True)
        self.caret_slope_run = int.from_bytes(data[20:22], byteorder='big', signed=True)
        self.caret_offset = int.from_bytes(data[22:24], byteorder='big', signed=True)

        self.reserved1 = int.from_bytes(data[24:26], byteorder='big')
        self.reserved2 = int.from_bytes(data[26:28], byteorder='big')
        self.reserved3 = int.from_bytes(data[28:30], byteorder='big')
        self.reserved4 = int.from_bytes(data[30:32], byteorder='big')

        self.metric_data_format = int.from_bytes(data[32:34], byteorder='big', signed=True)
        self.number_of_h_metrics = int.from_bytes(data[34:36], byteorder='big', signed=False)

    def get_version(self) -> float:
        """Get hhea version as float."""
        return self.version / 65536.0

    def get_ascent(self) -> int:
        """Get ascent value."""
        return self.ascent

    def get_descent(self) -> int:
        """Get descent value."""
        return self.descent

    def get_line_gap(self) -> int:
        """Get line gap value."""
        return self.line_gap

    def get_advance_width_max(self) -> int:
        """Get maximum advance width."""
        return self.advance_width_max

    def get_number_of_h_metrics(self) -> int:
        """Get number of horizontal metrics."""
        return self.number_of_h_metrics

    def to_string(self) -> str:
        """Get string representation."""
        return (
            f"hhea: Horizontal Header\n"
            f"  'version'               {self.get_version():.4f}\n"
            f"  'ascent'                 {self.ascent}\n"
            f"  'descent'                {self.descent}\n"
            f"  'lineGap'                {self.line_gap}\n"
            f"  'advanceWidthMax'        {self.advance_width_max}\n"
            f"  'minLeftSideBearing'     {self.min_left_side_bearing}\n"
            f"  'minRightSideBearing'    {self.min_right_side_bearing}\n"
            f"  'xMaxExtent'             {self.x_max_extent}\n"
            f"  'caretSlopeRise'         {self.caret_slope_rise}\n"
            f"  'caretSlopeRun'          {self.caret_slope_run}\n"
            f"  'caretOffset'            {self.caret_offset}\n"
            f"  'metricDataFormat'       {self.metric_data_format}\n"
            f"  'numberOfHMetrics'       {self.number_of_h_metrics}"
        )
