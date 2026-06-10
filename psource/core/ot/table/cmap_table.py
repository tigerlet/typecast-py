#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CmapTable class - Character Mapping Table
"""

from .table import Table


class CmapIndexEntry:
    """
    Represents an entry in the cmap index table.
    """

    def __init__(self, data: bytes, offset: int):
        """
        Initialize CmapIndexEntry.
        
        Args:
            data: Raw data
            offset: Offset in data
        """
        self._platform_id = int.from_bytes(data[offset:offset+2], byteorder='big')
        self._encoding_id = int.from_bytes(data[offset+2:offset+4], byteorder='big')
        self._offset = int.from_bytes(data[offset+4:offset+8], byteorder='big')
        self._format = None

    def get_platform_id(self) -> int:
        """Get platform ID."""
        return self._platform_id

    def get_encoding_id(self) -> int:
        """Get encoding ID."""
        return self._encoding_id

    def get_offset(self) -> int:
        """Get offset."""
        return self._offset

    def get_format(self):
        """Get CmapFormat."""
        return self._format

    def set_format(self, format):
        """Set CmapFormat."""
        self._format = format

    def get_platform_name(self) -> str:
        """Get platform name."""
        if self._platform_id == 1:
            return "Macintosh"
        elif self._platform_id == 3:
            return "Windows"
        return ""

    def get_encoding_name(self) -> str:
        """Get encoding name."""
        if self._platform_id == 3:
            names = {
                0: "Symbol",
                1: "Unicode",
                2: "ShiftJIS",
                3: "Big5",
                4: "PRC",
                5: "Wansung",
                6: "Johab"
            }
            return names.get(self._encoding_id, "")
        return ""

    def __lt__(self, other):
        """Comparison for sorting."""
        return self._offset < other._offset

    def __eq__(self, other):
        """Equality check."""
        return self._offset == other._offset


class CmapFormat:
    """
    Base class for cmap format implementations.
    """

    def __init__(self, format_type: int, length: int, language: int):
        """
        Initialize CmapFormat.
        
        Args:
            format_type: Format type
            length: Length in bytes
            language: Language code
        """
        self._format_type = format_type
        self._length = length
        self._language = language

    def get_format_type(self) -> int:
        """Get format type."""
        return self._format_type

    def get_length(self) -> int:
        """Get length."""
        return self._length

    def get_language(self) -> int:
        """Get language."""
        return self._language

    def get_glyph_id(self, char_code: int) -> int:
        """Get glyph ID for character code."""
        return 0

    @staticmethod
    def create(format_type: int, data: bytes, offset: int):
        """
        Create appropriate CmapFormat instance.
        
        Args:
            format_type: Format type
            data: Raw data
            offset: Offset in data
        
        Returns:
            CmapFormat instance
        """
        if format_type == 4:
            return CmapFormat4(format_type, data, offset)
        elif format_type == 12:
            return CmapFormat12(format_type, data, offset)
        else:
            return CmapFormat(format_type, 0, 0)


class CmapFormat4(CmapFormat):
    """
    Format 4 cmap subtable - Segmented coverage for Unicode BMP.
    """

    def __init__(self, format_type: int, data: bytes, offset: int):
        """
        Initialize CmapFormat4.
        
        Args:
            format_type: Format type
            data: Raw data
            offset: Offset in data
        """
        length = int.from_bytes(data[offset+2:offset+4], byteorder='big')
        language = int.from_bytes(data[offset+4:offset+6], byteorder='big')
        super().__init__(format_type, length, language)
        
        self._seg_count_x2 = int.from_bytes(data[offset+6:offset+8], byteorder='big')
        seg_count = self._seg_count_x2 // 2
        
        self._end_count = []
        for i in range(seg_count):
            self._end_count.append(int.from_bytes(data[offset+8+i*2:offset+10+i*2], byteorder='big'))
        
        self._start_count = []
        start_offset = offset + 10 + seg_count * 2 + 2
        for i in range(seg_count):
            self._start_count.append(int.from_bytes(data[start_offset+i*2:start_offset+2+i*2], byteorder='big'))
        
        self._id_delta = []
        delta_offset = start_offset + seg_count * 2
        for i in range(seg_count):
            self._id_delta.append(int.from_bytes(data[delta_offset+i*2:delta_offset+2+i*2], byteorder='big', signed=True))
        
        self._id_range_offset = []
        range_offset = delta_offset + seg_count * 2
        for i in range(seg_count):
            self._id_range_offset.append(int.from_bytes(data[range_offset+i*2:range_offset+2+i*2], byteorder='big'))
        
        self._glyph_id_array = []
        glyph_offset = range_offset + seg_count * 2
        remaining = length - (glyph_offset - offset)
        for i in range(remaining // 2):
            self._glyph_id_array.append(int.from_bytes(data[glyph_offset+i*2:glyph_offset+2+i*2], byteorder='big'))

    def get_glyph_id(self, char_code: int) -> int:
        """Get glyph ID for character code."""
        seg_count = self._seg_count_x2 // 2
        
        for i in range(seg_count):
            if char_code <= self._end_count[i]:
                if char_code >= self._start_count[i]:
                    if self._id_range_offset[i] == 0:
                        return (char_code + self._id_delta[i]) & 0xFFFF
                    else:
                        offset = (self._id_range_offset[i] // 2) + (char_code - self._start_count[i])
                        if offset < len(self._glyph_id_array):
                            glyph_id = self._glyph_id_array[offset]
                            if glyph_id == 0:
                                return 0
                            return (glyph_id + self._id_delta[i]) & 0xFFFF
                return 0
        return 0


class CmapFormat12(CmapFormat):
    """
    Format 12 cmap subtable - Segmented coverage for full Unicode.
    """

    def __init__(self, format_type: int, data: bytes, offset: int):
        """
        Initialize CmapFormat12.
        
        Args:
            format_type: Format type
            data: Raw data
            offset: Offset in data
        """
        length = int.from_bytes(data[offset+2:offset+4], byteorder='big')
        language = int.from_bytes(data[offset+4:offset+8], byteorder='big')
        super().__init__(format_type, length, language)
        
        self._num_groups = int.from_bytes(data[offset+8:offset+12], byteorder='big')
        
        self._groups = []
        group_offset = offset + 12
        for i in range(self._num_groups):
            start_char = int.from_bytes(data[group_offset+i*12:group_offset+4+i*12], byteorder='big')
            end_char = int.from_bytes(data[group_offset+4+i*12:group_offset+8+i*12], byteorder='big')
            start_glyph = int.from_bytes(data[group_offset+8+i*12:group_offset+12+i*12], byteorder='big')
            self._groups.append((start_char, end_char, start_glyph))

    def get_glyph_id(self, char_code: int) -> int:
        """Get glyph ID for character code."""
        for start_char, end_char, start_glyph in self._groups:
            if start_char <= char_code <= end_char:
                return start_glyph + (char_code - start_char)
        return 0


class CmapTable(Table):
    """
    'cmap' table - Character Mapping Table
    
    Maps character codes to glyph indices.
    """

    def __init__(self, directory_entry, data: bytes):
        """
        Initialize CmapTable.

        Args:
            directory_entry: DirectoryEntry for this table
            data: Table data
        """
        super().__init__(directory_entry)
        self._data = data
        self._entries = []
        self._parse()

    def _parse(self):
        """Parse the cmap table."""
        self._version = int.from_bytes(self._data[0:2], byteorder='big')
        self._num_tables = int.from_bytes(self._data[2:4], byteorder='big')
        
        bytes_read = 4
        self._entries = []
        for i in range(self._num_tables):
            entry = CmapIndexEntry(self._data, bytes_read)
            self._entries.append(entry)
            bytes_read += 8
        
        self._entries.sort()
        
        last_offset = 0
        last_format = None
        for entry in self._entries:
            if entry.get_offset() == last_offset:
                entry.set_format(last_format)
                continue
            
            if entry.get_offset() > bytes_read:
                bytes_read = entry.get_offset()
            
            if bytes_read + 2 > len(self._data):
                return
            
            format_type = int.from_bytes(self._data[bytes_read:bytes_read+2], byteorder='big')
            last_format = CmapFormat.create(format_type, self._data, bytes_read)
            last_offset = entry.get_offset()
            entry.set_format(last_format)
            bytes_read += last_format.get_length()

    def get_version(self) -> int:
        """Get version."""
        return self._version

    def get_num_tables(self) -> int:
        """Get number of subtables."""
        return self._num_tables

    def get_entries(self):
        """Get all index entries."""
        return self._entries

    def get_subtables(self):
        """Get all subtables (CmapFormat instances)."""
        return [entry.get_format() for entry in self._entries if entry.get_format()]

    def get_cmap_format(self, platform_id: int, encoding_id: int):
        """Get CmapFormat for specified platform and encoding."""
        for entry in self._entries:
            if entry.get_platform_id() == platform_id and entry.get_encoding_id() == encoding_id:
                return entry.get_format()
        return None

    def get_glyph_id(self, char_code: int) -> int:
        """Get glyph ID for character code."""
        for entry in self._entries:
            fmt = entry.get_format()
            if fmt:
                glyph_id = fmt.get_glyph_id(char_code)
                if glyph_id != 0:
                    return glyph_id
        return 0

    def to_string(self) -> str:
        """Get string representation."""
        result = "cmap\n"
        for entry in self._entries:
            platform_name = entry.get_platform_name()
            encoding_name = entry.get_encoding_name()
            result += f"\tplatform id: {entry.get_platform_id()} ({platform_name}), "
            result += f"encoding id: {entry.get_encoding_id()} ({encoding_name}), "
            result += f"offset: {entry.get_offset()}\n"
        return result