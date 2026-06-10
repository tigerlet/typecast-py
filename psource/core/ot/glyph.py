#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Glyph class - Represents a single glyph (character outline)
"""

from typing import List
from .point import Point


class Glyph:
    """
    Represents a single glyph in a font.

    A glyph contains:
    - Points: List of Point objects making up the outline
    - advance_width: Distance to move for the next character
    - left_side_bearing: Distance from origin to left edge
    """

    def __init__(self, description, left_side_bearing: int, advance_width: int):
        """
        Initialize a Glyph.

        Args:
            description: GlyphDescription containing the outline
            left_side_bearing: Left side bearing value
            advance_width: Advance width value
        """
        self._left_side_bearing = left_side_bearing
        self._advance_width = advance_width
        self._points = []

        if description:
            self._describe(description)
        else:
            # Add two anchor points even without description
            self._points.append(Point(0, 0, True, True))
            self._points.append(Point(advance_width, 0, True, True))

    def _describe(self, description):
        """
        Extract points from glyph description.

        Args:
            description: GlyphDescription object
        """
        end_pt_index = 0
        point_count = description.get_point_count()

        for i in range(point_count):
            is_end_pt = description.get_end_pt_of_contours(end_pt_index) == i

            if is_end_pt:
                end_pt_index += 1

            on_curve = (description.get_flags(i) & 0x01) != 0
            x = description.get_x_coordinate(i)
            y = description.get_y_coordinate(i)

            self._points.append(Point(x, y, on_curve, is_end_pt))

    def get_advance_width(self) -> int:
        """Get advance width."""
        return self._advance_width

    def get_left_side_bearing(self) -> int:
        """Get left side bearing."""
        return self._left_side_bearing

    def get_point(self, index: int) -> Point:
        """
        Get point at index.

        Args:
            index: Point index

        Returns:
            Point object
        """
        if 0 <= index < len(self._points):
            return self._points[index]
        return None

    def get_point_count(self) -> int:
        """Get number of points."""
        return len(self._points)

    def reset(self):
        """Reset glyph state."""
        pass

    def scale(self, factor: float):
        """
        Scale the glyph.

        Args:
            factor: Scale factor
        """
        for point in self._points:
            point.scale(factor)

        self._left_side_bearing = int(self._left_side_bearing * factor)
        self._advance_width = int(self._advance_width * factor)

    def to_string(self) -> str:
        """Get string representation."""
        result = f"Glyph:\n"
        result += f"  Advance Width: {self._advance_width}\n"
        result += f"  Left Side Bearing: {self._left_side_bearing}\n"
        result += f"  Points: {len(self._points)}\n"
        
        result += "\n  Coordinates\n  -----------"
        old_x = 0
        old_y = 0
        for i, point in enumerate(self._points):
            rel_x = point.x - old_x
            rel_y = point.y - old_y
            abs_x = point.x
            abs_y = point.y
            result += f"\n    {i}: Rel ({rel_x}, {rel_y})  ->  Abs ({abs_x}, {abs_y})"
            old_x = abs_x
            old_y = abs_y
        
        return result
