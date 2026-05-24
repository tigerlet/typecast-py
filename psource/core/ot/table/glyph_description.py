#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GlyphDescription base class - Base class for glyph descriptions
"""


class GlyphDescription:
    """
    Base class for glyph descriptions in the 'glyf' table.

    Subclasses handle simple glyphs and composite glyphs.
    """

    def __init__(self):
        """Initialize a GlyphDescription."""
        self.x_min = 0
        self.y_min = 0
        self.x_max = 0
        self.y_max = 0

    def get_point_count(self) -> int:
        """
        Get the number of points in the glyph.

        Returns:
            Number of points
        """
        return 0

    def get_contour_count(self) -> int:
        """
        Get the number of contours in the glyph.

        Returns:
            Number of contours
        """
        return 0

    def get_bounds(self) -> tuple:
        """
        Get the bounding box of the glyph.

        Returns:
            Tuple of (x_min, y_min, x_max, y_max)
        """
        return (self.x_min, self.y_min, self.x_max, self.y_max)

    def to_string(self) -> str:
        """Get string representation."""
        return (
            f"GlyphDescription\n"
            f"  xMin: {self.x_min}\n"
            f"  yMin: {self.y_min}\n"
            f"  xMax: {self.x_max}\n"
            f"  yMax: {self.y_max}"
        )
