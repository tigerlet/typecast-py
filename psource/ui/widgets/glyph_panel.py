#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GlyphPanel - Glyph Editing Panel Widget
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QToolBar,
                             QScrollArea, QLabel)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QPalette
from .glyph_editor import GlyphEditor
from .glyph_toolbar import GlyphToolbar
from .glyph_statusbar import GlyphStatusBar


class GlyphPanel(QWidget):
    """
    Glyph Editing Panel

    Contains:
    - Toolbar (GlyphToolbar)
    - Glyph Editor (GlyphEditor)
    - Status Bar (GlyphStatusBar)
    """

    def __init__(self, parent=None):
        """Initialize glyph editing panel"""
        super().__init__(parent)

        self._font = None
        self._glyph = None
        self._properties = {}

        self._init_ui()
        self._init_toolbar()
        self._init_statusbar()

    def _init_ui(self):
        """Initialize UI layout"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._toolbar = GlyphToolbar(self)
        layout.addWidget(self._toolbar)

        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setBackgroundRole(QPalette.Window)
        self._scroll_area.setStyleSheet("QScrollArea { background-color: white; }")

        self._glyph_editor = GlyphEditor()
        self._scroll_area.setWidget(self._glyph_editor)

        layout.addWidget(self._scroll_area)

        self._statusbar = GlyphStatusBar(self)
        layout.addWidget(self._statusbar)

        self._statusbar.setGlyphEditor(self._glyph_editor)

    def _init_toolbar(self):
        """Initialize toolbar"""
        pass

    def _init_statusbar(self):
        """Initialize status bar"""
        pass

    def get_glyph_editor(self) -> GlyphEditor:
        """Get glyph editor"""
        return self._glyph_editor

    def get_toolbar(self) -> GlyphToolbar:
        """Get toolbar"""
        return self._toolbar

    def get_statusbar(self) -> GlyphStatusBar:
        """Get status bar"""
        return self._statusbar

    def set_font(self, font):
        """
        Set font

        Args:
            font: OTFont object
        """
        self._font = font
        self._glyph_editor.set_font(font)

    def set_glyph(self, glyph, index: int = 0):
        """
        Set current glyph

        Args:
            glyph: Glyph object
            index: Glyph index
        """
        self._glyph = glyph
        self._glyph_editor.set_glyph(glyph, index)

        if glyph:
            self._glyph_editor.set_font(self._font)
            self._statusbar.update_glyph_info(glyph, index)

    def get_font(self):
        """Get font"""
        return self._font

    def get_glyph(self):
        """Get current glyph"""
        return self._glyph

    def set_properties(self, props: dict):
        """
        Set properties

        Args:
            props: Properties dictionary
        """
        self._properties = props

        zoom = float(props.get('Zoom', '0.25'))
        self._glyph_editor.set_scale_factor(zoom)

    def get_properties(self) -> dict:
        """Get properties"""
        self._properties['Zoom'] = str(self._glyph_editor.get_scale_factor())
        return self._properties