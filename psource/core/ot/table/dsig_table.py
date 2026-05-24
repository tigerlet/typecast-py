#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
DsigTable class - Digital Signature Table
"""

from .table import Table


class DsigEntry:
    """
    Represents a DSIG entry.
    """

    def __init__(self, data: bytes, offset: int):
        """
        Initialize DsigEntry.
        
        Args:
            data: Raw data
            offset: Offset in data
        """
        self._format = int.from_bytes(data[offset:offset+2], byteorder='big')
        self._length = int.from_bytes(data[offset+2:offset+6], byteorder='big')
        self._offset = int.from_bytes(data[offset+6:offset+10], byteorder='big')


class SignatureBlock:
    """
    Represents a signature block in DSIG table.
    """

    def __init__(self, data: bytes, offset: int):
        """
        Initialize SignatureBlock.
        
        Args:
            data: Raw data
            offset: Offset in data
        """
        self._reserved1 = int.from_bytes(data[offset:offset+2], byteorder='big')
        self._reserved2 = int.from_bytes(data[offset+2:offset+4], byteorder='big')
        self._signature_len = int.from_bytes(data[offset+4:offset+8], byteorder='big')
        self._signature = data[offset+8:offset+8+self._signature_len]

    def to_string(self) -> str:
        """Get string representation."""
        result = ""
        signature_len = len(self._signature)
        for i in range(0, signature_len, 16):
            end = min(i + 16, signature_len)
            chunk = self._signature[i:end]
            try:
                result += chunk.decode('latin-1', errors='replace') + "\n"
            except:
                result += str(chunk) + "\n"
        return result


class DsigTable(Table):
    """
    'DSIG' table - Digital Signature Table
    
    Contains digital signatures for the font.
    """

    def __init__(self, directory_entry, data: bytes):
        """
        Initialize DsigTable.

        Args:
            directory_entry: DirectoryEntry for this table
            data: Table data
        """
        super().__init__(directory_entry)
        self._data = data
        self._entries = []
        self._sig_blocks = []
        self._parse()

    def _parse(self):
        """Parse the DSIG table."""
        if len(self._data) < 8:
            return
        
        self._version = int.from_bytes(self._data[0:4], byteorder='big')
        self._num_sigs = int.from_bytes(self._data[4:6], byteorder='big')
        self._flag = int.from_bytes(self._data[6:8], byteorder='big')
        
        offset = 8
        self._entries = []
        for i in range(self._num_sigs):
            if offset + 10 <= len(self._data):
                entry = DsigEntry(self._data, offset)
                self._entries.append(entry)
                offset += 10
        
        self._sig_blocks = []
        for i in range(self._num_sigs):
            if offset + 8 <= len(self._data):
                sig_len = int.from_bytes(self._data[offset+4:offset+8], byteorder='big')
                if offset + 8 + sig_len <= len(self._data):
                    block = SignatureBlock(self._data, offset)
                    self._sig_blocks.append(block)
                    offset += 8 + sig_len

    def to_string(self) -> str:
        """Get string representation."""
        result = "DSIG\n"
        for block in self._sig_blocks:
            result += block.to_string()
        return result