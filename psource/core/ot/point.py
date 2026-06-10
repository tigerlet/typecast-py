#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Point class - Represents a coordinate point in a glyph contour
"""


class Point:
    """
    Represents a coordinate point in a glyph outline.

    Attributes:
        x (int): X coordinate
        y (int): Y coordinate
        on_curve (bool): True if point is on the curve, False if off-curve (control point)
        end_of_contour (bool): True if this is the last point of a contour
    """

    def __init__(self, x: int, y: int, on_curve: bool = True, end_of_contour: bool = False):
        """
        Initialize a Point.

        Args:
            x: X coordinate
            y: Y coordinate
            on_curve: Whether point is on curve (True) or control point (False)
            end_of_contour: Whether this is the end of a contour
        """
        self.x = x
        self.y = y
        self.on_curve = on_curve
        self.end_of_contour = end_of_contour

    def __repr__(self):
        """String representation of Point."""
        return f"Point(x={self.x}, y={self.y}, on_curve={self.on_curve}, end={self.end_of_contour})"

    def __eq__(self, other):
        """Check equality between points."""
        if not isinstance(other, Point):
            return False
        return (self.x == other.x and
                self.y == other.y and
                self.on_curve == other.on_curve and
                self.end_of_contour == other.end_of_contour)

    def __hash__(self):
        """Hash function for Point."""
        return hash((self.x, self.y, self.on_curve, self.end_of_contour))

    def scale(self, factor: float):
        """
        Scale the point coordinates.

        Args:
            factor: Scale factor
        """
        self.x = int(self.x * factor)
        self.y = int(self.y * factor)

    def translate(self, dx: int, dy: int):
        """
        Translate the point.

        Args:
            dx: Delta X
            dy: Delta Y
        """
        self.x += dx
        self.y += dy
