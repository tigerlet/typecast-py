#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HmtxTable class - Horizontal Metrics table
"""

from .table import Table


class HmtxTable(Table):
    """
    'hmtx' table - Horizontal Metrics

    Contains horizontal metrics for each glyph.
    """

    def __init__(self, directory_entry, data: bytes, number_of_h_metrics: int = 0):
        """
        Initialize HmtxTable.

        Args:
            directory_entry: DirectoryEntry for this table
            data: Table data
            number_of_h_metrics: Number of horizontal metrics from hhea table
        """
        super().__init__(directory_entry)
        self._data = data
        self.metrics = []
        self._number_of_h_metrics = number_of_h_metrics

        if number_of_h_metrics == 0:
            self._number_of_h_metrics = len(data) // 4

        self._parse_metrics()

    def _parse_metrics(self):
        """Parse metrics data from the table."""
        data = self._data
        self.metrics = []

        offset = 0
        for i in range(self._number_of_h_metrics):
            if offset + 4 > len(data):
                break

            advance_width = int.from_bytes(data[offset:offset+2], byteorder='big', signed=False)
            lsb = int.from_bytes(data[offset+2:offset+4], byteorder='big', signed=True)

            self.metrics.append({
                'advance_width': advance_width,
                'lsb': lsb
            })

            offset += 4

        if len(data) > offset:
            remaining_bytes = len(data) - offset
            remaining_glyphs = remaining_bytes // 2

            for i in range(remaining_glyphs):
                if offset + 2 > len(data):
                    break

                lsb = int.from_bytes(data[offset:offset+2], byteorder='big', signed=True)
                self.metrics.append({
                    'advance_width': self.metrics[-1]['advance_width'] if self.metrics else 0,
                    'lsb': lsb
                })

                offset += 2

    def init(self, number_of_h_metrics: int, num_lsb: int):
        """
        Initialize metrics with specific counts.

        Args:
            number_of_h_metrics: Number of hmetrics entries
            num_lsb: Number of left side bearings
        """
        self._number_of_h_metrics = number_of_h_metrics
        self._parse_metrics()

    def get_number_of_metrics(self) -> int:
        """Get number of metrics entries."""
        return len(self.metrics)

    def get_metric(self, index: int) -> dict:
        """
        Get metric for a specific glyph index.

        Args:
            index: Glyph index

        Returns:
            Dictionary with 'advance_width' and 'lsb' keys
        """
        if 0 <= index < len(self.metrics):
            return self.metrics[index]
        elif self.metrics:
            return self.metrics[-1]
        return {'advance_width': 0, 'lsb': 0}

    def get_advance_width(self, index: int) -> int:
        """Get advance width for glyph index."""
        return self.get_metric(index)['advance_width']

    def get_lsb(self, index: int) -> int:
        """Get left side bearing for glyph index."""
        return self.get_metric(index)['lsb']

    def get_left_side_bearing(self, index: int) -> int:
        """Get left side bearing for glyph index."""
        return self.get_lsb(index)

    def to_string(self) -> str:
        """Get string representation."""
        return (
            f"hmtx: Horizontal Metrics\n"
            f"  Number of metrics: {len(self.metrics)}"
        )
