#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GlyfSimpleDescript class - Simple glyph description
"""

from .glyph_description import GlyphDescription


class GlyfSimpleDescript(GlyphDescription):
    """
    Represents a simple glyph description (made up of outlines).
    
    A simple glyph consists of:
    - A bounding box (xMin, yMin, xMax, yMax)
    - A number of contours
    - Flags arrays
    - Coordinates arrays
    """

    def __init__(self, parent_table, number_of_contours, data):
        """
        Initialize a simple glyph description.
        
        Args:
            parent_table: GlyfTable instance
            number_of_contours: Number of contours (short)
            data: Data input (bytes or file-like object)
        """
        super().__init__()
        
        self._parent_table = parent_table
        self._number_of_contours = number_of_contours
        
        if isinstance(data, bytes):
            self._data = data
            self._offset = 0
        else:
            self._data = None
            self._stream = data
        
        self._read_bounding_box()
        self._read_end_points_of_contours()
        self._read_instructions()
        self._read_flags()
        self._read_coords()

    def _read_short(self):
        """Read a signed short (2 bytes) from data."""
        if self._data is not None:
            if self._offset + 2 > len(self._data):
                return 0
            value = int.from_bytes(self._data[self._offset:self._offset+2], byteorder='big', signed=True)
            self._offset += 2
            return value
        else:
            return self._stream.readShort()

    def _read_byte(self):
        """Read a byte from data."""
        if self._data is not None:
            if self._offset >= len(self._data):
                return 0
            value = self._data[self._offset]
            self._offset += 1
            return value
        else:
            return self._stream.readByte()

    def _read_unsigned_byte(self):
        """Read an unsigned byte from data."""
        return self._read_byte() & 0xFF

    def _read_bytes(self, length):
        """Read bytes from data."""
        if self._data is not None:
            if self._offset + length > len(self._data):
                return b''
            value = self._data[self._offset:self._offset+length]
            self._offset += length
            return value
        else:
            buf = bytearray(length)
            self._stream.readFully(buf)
            return bytes(buf)

    def _read_bounding_box(self):
        """Read bounding box values."""
        self._x_min = self._read_short()
        self._y_min = self._read_short()
        self._x_max = self._read_short()
        self._y_max = self._read_short()

    def _read_end_points_of_contours(self):
        """Read end points of contours."""
        self._end_pts_of_contours = []
        for i in range(self._number_of_contours):
            self._end_pts_of_contours.append(self._read_short())
        
        if self._number_of_contours > 0:
            self._count = self._end_pts_of_contours[-1] + 1
        else:
            self._count = 0
        
        self._flags = bytearray(self._count)
        self._x_coordinates = [0] * self._count
        self._y_coordinates = [0] * self._count

    def _read_instructions(self):
        """Read glyph instructions."""
        instruction_count = self._read_short()
        self._instructions = self._read_bytes(instruction_count)

    def _read_flags(self):
        """Read flags array."""
        try:
            index = 0
            while index < self._count:
                flag = self._read_byte()
                self._flags[index] = flag
                
                if (flag & 0x08) != 0:
                    repeats = self._read_unsigned_byte()
                    for i in range(1, repeats + 1):
                        if index + i < self._count:
                            self._flags[index + i] = flag
                    index += repeats
                
                index += 1
        except IndexError:
            pass

    def _read_coords(self):
        """Read x and y coordinates."""
        x = 0
        for i in range(self._count):
            if (self._flags[i] & 0x10) != 0:
                if (self._flags[i] & 0x02) != 0:
                    x += self._read_unsigned_byte()
            else:
                if (self._flags[i] & 0x02) != 0:
                    x += -self._read_unsigned_byte()
                else:
                    x += self._read_short()
            self._x_coordinates[i] = x
        
        y = 0
        for i in range(self._count):
            if (self._flags[i] & 0x20) != 0:
                if (self._flags[i] & 0x04) != 0:
                    y += self._read_unsigned_byte()
            else:
                if (self._flags[i] & 0x04) != 0:
                    y += -self._read_unsigned_byte()
                else:
                    y += self._read_short()
            self._y_coordinates[i] = y

    def get_point_count(self) -> int:
        """Get number of points."""
        return self._count

    def get_contour_count(self) -> int:
        """Get number of contours."""
        return self._number_of_contours

    def get_end_pt_of_contours(self, contour_index: int) -> int:
        """Get end point of contour."""
        if 0 <= contour_index < len(self._end_pts_of_contours):
            return self._end_pts_of_contours[contour_index]
        return -1

    def get_flags(self, point_index: int) -> int:
        """Get flags for point."""
        if 0 <= point_index < len(self._flags):
            return self._flags[point_index]
        return 0

    def get_x_coordinate(self, point_index: int) -> int:
        """Get X coordinate."""
        if 0 <= point_index < len(self._x_coordinates):
            return self._x_coordinates[point_index]
        return 0

    def get_y_coordinate(self, point_index: int) -> int:
        """Get Y coordinate."""
        if 0 <= point_index < len(self._y_coordinates):
            return self._y_coordinates[point_index]
        return 0

    def is_composite(self) -> bool:
        """Check if this is a composite glyph."""
        return False

    def get_instructions(self) -> bytes:
        """Get instructions."""
        return self._instructions

    def get_x_min(self) -> int:
        """Get xMin."""
        return self._x_min

    def get_y_min(self) -> int:
        """Get yMin."""
        return self._y_min

    def get_x_max(self) -> int:
        """Get xMax."""
        return self._x_max

    def get_y_max(self) -> int:
        """Get yMax."""
        return self._y_max

    def to_string(self) -> str:
        """Get string representation."""
        result = f"GlyfSimpleDescript\n"
        result += f"  numberOfContours: {self._number_of_contours}\n"
        result += f"  xMin:             {self._x_min}\n"
        result += f"  yMin:             {self._y_min}\n"
        result += f"  xMax:             {self._x_max}\n"
        result += f"  yMax:             {self._y_max}\n"
        result += f"\n  EndPoints\n  ---------"
        for i, pt in enumerate(self._end_pts_of_contours):
            result += f"\n    {i}: {pt}"
        result += f"\n\n  Length of Instructions: {len(self._instructions)}"
        
        result += "\n\n  Coordinates\n  -----------"
        old_x = 0
        old_y = 0
        for i in range(len(self._x_coordinates)):
            rel_x = self._x_coordinates[i] - old_x
            rel_y = self._y_coordinates[i] - old_y
            abs_x = self._x_coordinates[i]
            abs_y = self._y_coordinates[i]
            result += f"\n    {i}: Rel ({rel_x}, {rel_y})  ->  Abs ({abs_x}, {abs_y})"
            old_x = abs_x
            old_y = abs_y
        
        return result