#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GlyphToolbar - Glyph Editing Toolbar
"""

from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QToolBar, QAction,
                             QLabel, QComboBox, QSpinBox, QDoubleSpinBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QImage


class GlyphToolbar(QToolBar):
    """
    Glyph Editing Toolbar

    Tools:
    - Selection tool
    - Zoom control
    - View options
    """

    zoom_changed = pyqtSignal(float)
    tool_changed = pyqtSignal(str)
    show_points_changed = pyqtSignal(bool)
    preview_changed = pyqtSignal(bool)

    def __init__(self, parent=None):
        """Initialize toolbar"""
        super().__init__(parent)

        self._current_tool = "select"
        self._zoom_level = 0.25

        self._init_actions()
        self._init_zoom_control()
        self._init_view_options()

        self.setMovable(False)

    def _init_actions(self):
        """Initialize tool actions"""
        select_action = QAction("Select", self)
        select_action.setToolTip("Select Tool (V)")
        select_action.setCheckable(True)
        select_action.setChecked(True)
        select_action.triggered.connect(lambda: self._on_tool_selected("select"))
        self.addAction(select_action)

        self.addSeparator()

        point_action = QAction("Point", self)
        point_action.setToolTip("Point Tool (P)")
        point_action.setCheckable(True)
        point_action.triggered.connect(lambda: self._on_tool_selected("point"))
        self.addAction(point_action)

        self.addSeparator()

    def _init_zoom_control(self):
        """Initialize zoom control"""
        self.addWidget(QLabel("Zoom:"))

        self._zoom_combo = QComboBox()
        self._zoom_combo.addItems(["25%", "50%", "75%", "100%", "150%", "200%", "400%"])
        self._zoom_combo.setCurrentText("25%")
        self._zoom_combo.currentTextChanged.connect(self._on_zoom_changed)
        self.addWidget(self._zoom_combo)

        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.setToolTip("Zoom In (+)")
        zoom_in_action.triggered.connect(self._zoom_in)
        self.addAction(zoom_in_action)

        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.setToolTip("Zoom Out (-)")
        zoom_out_action.triggered.connect(self._zoom_out)
        self.addAction(zoom_out_action)

        self.addSeparator()

    def _init_view_options(self):
        """Initialize view options"""
        self._preview_action = QAction("Preview", self)
        self._preview_action.setToolTip("Show Preview (F)")
        self._preview_action.setCheckable(True)
        self._preview_action.setChecked(False)
        self._preview_action.triggered.connect(self._on_preview_changed)
        self.addAction(self._preview_action)

        self._show_points_action = QAction("Points", self)
        self._show_points_action.setToolTip("Show Control Points")
        self._show_points_action.setCheckable(True)
        self._show_points_action.setChecked(True)
        self._show_points_action.triggered.connect(self._on_show_points_changed)
        self.addAction(self._show_points_action)

    def _on_tool_selected(self, tool: str):
        """
        Tool selected

        Args:
            tool: Tool name
        """
        self._current_tool = tool
        self.tool_changed.emit(tool)

    def _on_zoom_changed(self, text: str):
        """
        Zoom level changed

        Args:
            text: Zoom text
        """
        if text.endswith('%'):
            zoom = float(text[:-1]) / 100.0
        else:
            zoom = 0.25

        self._zoom_level = zoom
        self.zoom_changed.emit(zoom)

    def _on_preview_changed(self, checked: bool):
        """
        Preview mode changed

        Args:
            checked: Whether preview is enabled
        """
        self.preview_changed.emit(checked)

    def _on_show_points_changed(self, checked: bool):
        """
        Show control points changed

        Args:
            checked: Whether to show
        """
        self.show_points_changed.emit(checked)

    def _zoom_in(self):
        """Zoom in"""
        zoom = self._zoom_level * 1.2
        zoom = min(5.0, zoom)
        self._set_zoom(zoom)

    def _zoom_out(self):
        """Zoom out"""
        zoom = self._zoom_level * 0.8
        zoom = max(0.05, zoom)
        self._set_zoom(zoom)

    def _set_zoom(self, zoom: float):
        """
        Set zoom level

        Args:
            zoom: Zoom value
        """
        self._zoom_level = zoom

        zoom_percent = int(zoom * 100)
        text = f"{zoom_percent}%"

        index = self._zoom_combo.findText(text)
        if index >= 0:
            self._zoom_combo.setCurrentIndex(index)
        else:
            self._zoom_combo.setCurrentText(text)

        self.zoom_changed.emit(zoom)

    def get_current_tool(self) -> str:
        """Get current tool"""
        return self._current_tool

    def get_zoom_level(self) -> float:
        """Get zoom level"""
        return self._zoom_level