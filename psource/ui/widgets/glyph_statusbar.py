#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GlyphStatusBar - Glyph Status Bar
"""

from PyQt5.QtWidgets import QStatusBar, QLabel, QFrame
from PyQt5.QtCore import Qt
from core.ot.glyph import Glyph


class GlyphStatusBar(QStatusBar):
    """
    Glyph Status Bar

    Displays:
    - Glyph index
    - Point count
    - Contour count
    - Current tool information
    """

    def __init__(self, parent=None):
        """Initialize status bar"""
        super().__init__(parent)

        self._glyph_editor = None
        self._glyph_index = 0
        self._glyph = None

        self._init_widgets()

    def _init_widgets(self):
        """Initialize widgets"""
        self._glyph_label = QLabel("Glyph: -")
        self._glyph_label.setFrameStyle(QFrame.Sunken | QFrame.Panel)
        self.addPermanentWidget(self._glyph_label)

        self._points_label = QLabel("Points: -")
        self._points_label.setFrameStyle(QFrame.Sunken | QFrame.Panel)
        self.addPermanentWidget(self._points_label)

        self._contours_label = QLabel("Contours: -")
        self._contours_label.setFrameStyle(QFrame.Sunken | QFrame.Panel)
        self.addPermanentWidget(self._contours_label)

        self._advance_label = QLabel("Advance: -")
        self._advance_label.setFrameStyle(QFrame.Sunken | QFrame.Panel)
        self.addPermanentWidget(self._advance_label)

        self._lsb_label = QLabel("LSB: -")
        self._lsb_label.setFrameStyle(QFrame.Sunken | QFrame.Panel)
        self.addPermanentWidget(self._lsb_label)

        self.showMessage("Ready")

    def setGlyphEditor(self, editor):
        """
        Set glyph editor

        Args:
            editor: GlyphEditor object
        """
        self._glyph_editor = editor

    def update_glyph_info(self, glyph: Glyph, index: int):
        """
        Update glyph information

        Args:
            glyph: Glyph object
            index: Glyph index
        """
        self._glyph = glyph
        self._glyph_index = index

        if glyph:
            self._glyph_label.setText(f"Glyph: {index}")

            point_count = glyph.get_point_count()
            self._points_label.setText(f"Points: {point_count}")

            contour_count = self._count_contours(glyph)
            self._contours_label.setText(f"Contours: {contour_count}")

            advance = glyph.get_advance_width()
            self._advance_label.setText(f"Advance: {advance}")

            lsb = glyph.get_left_side_bearing()
            self._lsb_label.setText(f"LSB: {lsb}")

        else:
            self._glyph_label.setText("Glyph: -")
            self._points_label.setText("Points: -")
            self._contours_label.setText("Contours: -")
            self._advance_label.setText("Advance: -")
            self._lsb_label.setText("LSB: -")

    def _count_contours(self, glyph: Glyph) -> int:
        """
        Count contours

        Args:
            glyph: Glyph object

        Returns:
            Contour count
        """
        if not glyph:
            return 0

        count = 0
        point_count = glyph.get_point_count()

        for i in range(point_count):
            point = glyph.get_point(i)
            if point.end_of_contour:
                count += 1

        return count

    def show_message(self, message: str):
        """
        Show message

        Args:
            message: Message text
        """
        self.showMessage(message)

    def clear(self):
        """Clear status bar"""
        self._glyph_label.setText("Glyph: -")
        self._points_label.setText("Points: -")
        self._contours_label.setText("Contours: -")
        self._advance_label.setText("Advance: -")
        self._lsb_label.setText("LSB: -")