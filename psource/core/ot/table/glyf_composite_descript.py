#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GlyfCompositeDescript class - Composite glyph description
"""

from .glyph_description import GlyphDescription


class GlyfCompositeDescript(GlyphDescription):
    """
    Represents a composite glyph description (made up of other glyphs).
    
    A composite glyph consists of:
    - A bounding box (xMin, yMin, xMax, yMax)
    - A number of components (references to other glyphs)
    - Transformation matrices for each component
    """

    def __init__(self, data: bytes):
        """
        Initialize a composite glyph description.
        
        Args:
            data: Glyph data
        """
        super().__init__()

        if len(data) < 10:
            raise ValueError("Insufficient data for composite glyph description")

        self.x_min = int.from_bytes(data[0:2], byteorder='big', signed=True)
        self.y_min = int.from_bytes(data[2:4], byteorder='big', signed=True)
        self.x_max = int.from_bytes(data[4:6], byteorder='big', signed=True)
        self.y_max = int.from_bytes(data[6:8], byteorder='big', signed=True)

        self.number_of_contours = int.from_bytes(data[8:10], byteorder='big', signed=True)
        
        if self.number_of_contours >= 0:
            raise ValueError("Not a composite glyph")

        self.components = []
        self._parse_components(data[10:])

    def _parse_components(self, data: bytes):
        """
        Parse composite glyph components.
        
        Args:
            data: Component data
        """
        offset = 0
        more_components = True
        
        while more_components and offset < len(data):
            flags = int.from_bytes(data[offset:offset+2], byteorder='big')
            offset += 2
            
            glyph_index = int.from_bytes(data[offset:offset+2], byteorder='big')
            offset += 2
            
            arg_1_and_2_are_words = (flags & 0x0001) != 0
            args_are_xy_values = (flags & 0x0002) != 0
            round_xy_to_grid = (flags & 0x0004) != 0
            we_have_a_scale = (flags & 0x0008) != 0
            reserved = (flags & 0x0010) != 0
            more_components = (flags & 0x0020) != 0
            we_have_an_x_and_y_scale = (flags & 0x0040) != 0
            we_have_a_two_by_two = (flags & 0x0080) != 0
            we_have_instructions = (flags & 0x0100) != 0
            use_my_metrics = (flags & 0x0200) != 0
            overlap_compound = (flags & 0x0400) != 0
            scalable_component_offset = (flags & 0x0800) != 0
            unscaled_component_offset = (flags & 0x1000) != 0
            
            transformation = [1, 0, 0, 1, 0, 0]
            
            if we_have_a_two_by_two:
                a = int.from_bytes(data[offset:offset+2], byteorder='big', signed=True) / 65536.0
                b = int.from_bytes(data[offset+2:offset+4], byteorder='big', signed=True) / 65536.0
                c = int.from_bytes(data[offset+4:offset+6], byteorder='big', signed=True) / 65536.0
                d = int.from_bytes(data[offset+6:offset+8], byteorder='big', signed=True) / 65536.0
                transformation = [a, b, c, d, 0, 0]
                offset += 8
            elif we_have_an_x_and_y_scale:
                scale_x = int.from_bytes(data[offset:offset+2], byteorder='big', signed=True) / 65536.0
                scale_y = int.from_bytes(data[offset+2:offset+4], byteorder='big', signed=True) / 65536.0
                transformation = [scale_x, 0, 0, scale_y, 0, 0]
                offset += 4
            elif we_have_a_scale:
                scale = int.from_bytes(data[offset:offset+2], byteorder='big', signed=True) / 65536.0
                transformation = [scale, 0, 0, scale, 0, 0]
                offset += 2
            
            if arg_1_and_2_are_words:
                if args_are_xy_values:
                    x = int.from_bytes(data[offset:offset+2], byteorder='big', signed=True)
                    y = int.from_bytes(data[offset+2:offset+4], byteorder='big', signed=True)
                else:
                    x = int.from_bytes(data[offset:offset+2], byteorder='big', signed=True)
                    y = int.from_bytes(data[offset+2:offset+4], byteorder='big', signed=True)
                offset += 4
            else:
                if args_are_xy_values:
                    x = data[offset] if (data[offset] & 0x80) == 0 else data[offset] - 256
                    y = data[offset + 1] if (data[offset + 1] & 0x80) == 0 else data[offset + 1] - 256
                else:
                    x = data[offset] if (data[offset] & 0x80) == 0 else data[offset] - 256
                    y = data[offset + 1] if (data[offset + 1] & 0x80) == 0 else data[offset + 1] - 256
                offset += 2
            
            transformation[4] = x
            transformation[5] = y
            
            self.components.append({
                'glyph_index': glyph_index,
                'transformation': transformation,
                'flags': flags
            })

    def get_component_count(self) -> int:
        """Get number of components."""
        return len(self.components)

    def get_component(self, index: int):
        """Get component at index."""
        if 0 <= index < len(self.components):
            return self.components[index]
        return None

    def get_point_count(self) -> int:
        """Get number of points (returns 0 for composite glyphs)."""
        return 0

    def get_contour_count(self) -> int:
        """Get number of contours (returns negative value for composite)."""
        return self.number_of_contours

    def get_end_pt_of_contours(self, contour_index: int) -> int:
        """Get end point of contour."""
        return -1

    def get_flags(self, point_index: int) -> int:
        """Get flags for point."""
        return 0

    def get_x_coordinate(self, point_index: int) -> int:
        """Get X coordinate."""
        return 0

    def get_y_coordinate(self, point_index: int) -> int:
        """Get Y coordinate."""
        return 0

    def to_string(self) -> str:
        """Get string representation."""
        result = f"GlyfCompositeDescript\n"
        result += f"  Number of components: {len(self.components)}\n"
        result += f"  xMin: {self.x_min}, yMin: {self.y_min}\n"
        result += f"  xMax: {self.x_max}, yMax: {self.y_max}\n"
        for i, comp in enumerate(self.components):
            result += f"  Component {i}: glyph={comp['glyph_index']}, "
            result += f"transform=[{comp['transformation'][0]:.4f}, {comp['transformation'][1]:.4f}, "
            result += f"{comp['transformation'][2]:.4f}, {comp['transformation'][3]:.4f}, "
            result += f"{comp['transformation'][4]}, {comp['transformation'][5]}]\n"
        return result