#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NameTable class - Naming Table
"""

from .table import Table


class NameRecord:
    """
    Represents a name record in the name table.
    """

    def __init__(self, data: bytes, offset: int):
        """
        Initialize NameRecord.
        
        Args:
            data: Raw data
            offset: Offset in data
        """
        self._platform_id = int.from_bytes(data[offset:offset+2], byteorder='big', signed=True)
        self._encoding_id = int.from_bytes(data[offset+2:offset+4], byteorder='big', signed=True)
        self._language_id = int.from_bytes(data[offset+4:offset+6], byteorder='big', signed=True)
        self._name_id = int.from_bytes(data[offset+6:offset+8], byteorder='big', signed=True)
        self._string_length = int.from_bytes(data[offset+8:offset+10], byteorder='big', signed=True)
        self._string_offset = int.from_bytes(data[offset+10:offset+12], byteorder='big', signed=True)
        self._record = ""

    def load_string(self, string_data: bytes):
        """
        Load the string from string storage.
        
        Args:
            string_data: String storage data
        """
        sb = []
        offset = self._string_offset
        
        if self._platform_id == 0:
            for i in range(self._string_length // 2):
                if offset + 2 <= len(string_data):
                    c = int.from_bytes(string_data[offset:offset+2], byteorder='big')
                    sb.append(chr(c))
                    offset += 2
        elif self._platform_id == 1:
            for i in range(self._string_length):
                if offset < len(string_data):
                    sb.append(chr(string_data[offset]))
                    offset += 1
        elif self._platform_id == 2:
            for i in range(self._string_length):
                if offset < len(string_data):
                    sb.append(chr(string_data[offset]))
                    offset += 1
        elif self._platform_id == 3:
            for i in range(self._string_length // 2):
                if offset + 2 <= len(string_data):
                    c = int.from_bytes(string_data[offset:offset+2], byteorder='big')
                    sb.append(chr(c))
                    offset += 2
        
        self._record = ''.join(sb)

    def get_encoding_id(self) -> int:
        """Get encoding ID."""
        return self._encoding_id

    def get_language_id(self) -> int:
        """Get language ID."""
        return self._language_id

    def get_name_id(self) -> int:
        """Get name ID."""
        return self._name_id

    def get_platform_id(self) -> int:
        """Get platform ID."""
        return self._platform_id

    def get_record_string(self) -> str:
        """Get the string value."""
        return self._record

    def __repr__(self) -> str:
        """String representation."""
        return f"NameRecord(platform={self._platform_id}, name={self._name_id}, string={self._record})"


class NameTable(Table):
    """
    'name' table - Naming Table
    
    Contains human-readable names for the font.
    """

    def __init__(self, directory_entry, data: bytes):
        """
        Initialize NameTable.

        Args:
            directory_entry: DirectoryEntry for this table
            data: Table data
        """
        super().__init__(directory_entry)
        self._data = data
        self._records = []
        self._parse()

    def _parse(self):
        """Parse the name table."""
        if len(self._data) < 6:
            return
        
        self._format_selector = int.from_bytes(self._data[0:2], byteorder='big', signed=True)
        self._number_of_name_records = int.from_bytes(self._data[2:4], byteorder='big', signed=True)
        self._string_storage_offset = int.from_bytes(self._data[4:6], byteorder='big', signed=True)
        
        self._records = []
        record_offset = 6
        for i in range(self._number_of_name_records):
            if record_offset + 12 <= len(self._data):
                record = NameRecord(self._data, record_offset)
                self._records.append(record)
                record_offset += 12
        
        if self._string_storage_offset < len(self._data):
            string_data = self._data[self._string_storage_offset:]
            for record in self._records:
                record.load_string(string_data)

    def get_number_of_name_records(self) -> int:
        """Get number of name records."""
        return self._number_of_name_records

    def get_record(self, index: int):
        """Get name record at index."""
        if 0 <= index < len(self._records):
            return self._records[index]
        return None

    def get_name_records(self):
        """Get all name records."""
        result = []
        for record in self._records:
            result.append({
                'platform_id': record.get_platform_id(),
                'encoding_id': record.get_encoding_id(),
                'language_id': record.get_language_id(),
                'name_id': record.get_name_id(),
                'name': self._get_name_id_name(record.get_name_id()),
                'value': record.get_record_string()
            })
        return result

    def _get_name_id_name(self, name_id: int) -> str:
        """Get the name for a name ID."""
        names = {
            0: "Copyright",
            1: "Font Family",
            2: "Font Subfamily",
            3: "Unique ID",
            4: "Full Name",
            5: "Version",
            6: "PostScript Name",
            7: "Trademark",
            8: "Manufacturer",
            9: "Designer",
            10: "Description",
            11: "URL Vendor",
            12: "URL Designer",
            13: "License",
            14: "License URL",
            15: "Preferred Family",
            16: "Preferred Subfamily",
            17: "Compatible Full",
            18: "Sample Text",
            19: "PostScript CID",
            20: "WWS Family",
            21: "WWS Subfamily",
            22: "Light Background Palette",
            23: "Dark Background Palette",
            24: "Variations PostScript Name Prefix"
        }
        return names.get(name_id, f"Name ID {name_id}")

    def get_record_string(self, name_id: int) -> str:
        """Get the string for a specific name ID."""
        for record in self._records:
            if record.get_name_id() == name_id:
                return record.get_record_string()
        return ""

    def to_string(self) -> str:
        """Get string representation."""
        result = "name\n"
        for record in self._records:
            result += f"\tName ID {record.get_name_id()} ({self._get_name_id_name(record.get_name_id())}): "
            result += f"{record.get_record_string()}\n"
        return result