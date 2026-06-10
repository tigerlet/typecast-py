#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Table base class - Base class for all OpenType tables
"""


class Table:
    """
    Base class for all OpenType table types.

    Each table in an OpenType font extends this base class.
    """

    def __init__(self, directory_entry):
        """Initialize a Table."""
        self._directory_entry = directory_entry

    def get_type(self) -> int:
        """Get the table type tag."""
        return self._directory_entry.tag

    def get_directory_entry(self):
        """Get the directory entry for this table."""
        return self._directory_entry

    def to_string(self) -> str:
        """Get string representation."""
        return str(self._directory_entry)
