#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CharacterMap - Character Map Widget
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTableWidget,
                             QTableWidgetItem, QHeaderView, QScrollArea)
from PyQt5.QtCore import Qt, pyqtSignal
from core.ot.otfont import OTFont


class CharacterMap(QWidget):
    """
    Character Map Widget

    Displays character mapping information for fonts
    """

    character_selected = pyqtSignal(int, int)

    def __init__(self, parent=None):
        """Initialize character map"""
        super().__init__(parent)

        self._font = None
        self._cmap_table = None

        self._init_ui()

    def _init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)

        self._table = QTableWidget()
        self._table.setColumnCount(16)
        self._table.setRowCount(16)

        headers = [f"{i:X}" for i in range(16)]
        self._table.setHorizontalHeaderLabels(headers)
        self._table.setVerticalHeaderLabels(headers)

        header = self._table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self._table.cellClicked.connect(self._on_cell_clicked)

        layout.addWidget(self._table)

    def set_font(self, font: OTFont):
        """
        Set font

        Args:
            font: OTFont object
        """
        self._font = font

        if font:
            self._cmap_table = font.get_cmap_table()
            self._populate_table()
        else:
            self._table.clear()

    def _populate_table(self):
        """Populate table"""
        self._table.clearContents()

        if not self._cmap_table:
            return

        for row in range(16):
            for col in range(16):
                char_code = (row << 8) | col

                item = QTableWidgetItem()
                item.setText(f"{char_code:04X}")
                item.setTextAlignment(Qt.AlignCenter)

                try:
                    glyph_index = self._cmap_table.get_glyph_index(char_code)
                    if glyph_index > 0:
                        item.setText(f"{char_code:04X}\n({glyph_index})")
                except:
                    pass

                self._table.setItem(row, col, item)

    def _on_cell_clicked(self, row: int, column: int):
        """
        Cell clicked event

        Args:
            row: Row index
            column: Column index
        """
        char_code = (row << 8) | column

        if self._cmap_table:
            try:
                glyph_index = self._cmap_table.get_glyph_index(char_code)
                self.character_selected.emit(char_code, glyph_index)
            except:
                self.character_selected.emit(char_code, 0)

    def get_font(self) -> OTFont:
        """Get font"""
        return self._font

    def clear(self):
        """Clear contents"""
        self._table.clearContents()
        self._font = None
        self._cmap_table = None