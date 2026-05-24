#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
EditorMenu - Menu Bar
"""

from PyQt5.QtWidgets import (QMenuBar, QMenu, QAction, QWidget,
                             QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QKeySequence


class EditorMenu(QMenuBar):
    """
    Editor Menu Bar

    Menus:
    - File: Open, Close, Export, Exit
    - Edit: Undo, Redo, Copy, Paste
    - View: Preview, Control Points, Zoom
    - Help: About
    """

    open_file = pyqtSignal()
    close_file = pyqtSignal()
    export_file = pyqtSignal()
    exit_app = pyqtSignal()

    preview_changed = pyqtSignal(bool)
    show_points_changed = pyqtSignal(bool)

    about_app = pyqtSignal()

    def __init__(self, parent=None):
        """Initialize menu bar"""
        super().__init__(parent)

        self._preview = False
        self._show_points = True
        self._font_collection = None

        self._init_file_menu()
        self._init_edit_menu()
        self._init_view_menu()
        self._init_help_menu()

    def _init_file_menu(self):
        """Initialize file menu"""
        file_menu = self.addMenu("&File")

        self._open_action = QAction("&Open...", self)
        self._open_action.setShortcut(QKeySequence.Open)
        self._open_action.triggered.connect(self._on_open)
        file_menu.addAction(self._open_action)

        file_menu.addSeparator()

        self._close_action = QAction("&Close", self)
        self._close_action.setEnabled(False)
        self._close_action.triggered.connect(self._on_close)
        file_menu.addAction(self._close_action)

        file_menu.addSeparator()

        self._export_action = QAction("&Export...", self)
        self._export_action.setShortcut(QKeySequence.Save)
        self._export_action.setEnabled(False)
        self._export_action.triggered.connect(self._on_export)
        file_menu.addAction(self._export_action)

        file_menu.addSeparator()

        self._exit_action = QAction("E&xit", self)
        self._exit_action.setShortcut(QKeySequence.Quit)
        self._exit_action.triggered.connect(self._on_exit)
        file_menu.addAction(self._exit_action)

    def _init_edit_menu(self):
        """Initialize edit menu"""
        edit_menu = self.addMenu("&Edit")

        undo_action = QAction("&Undo", self)
        undo_action.setShortcut(QKeySequence.Undo)
        undo_action.setEnabled(False)
        edit_menu.addAction(undo_action)

        redo_action = QAction("&Redo", self)
        redo_action.setShortcut(QKeySequence.Redo)
        redo_action.setEnabled(False)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        copy_action = QAction("&Copy", self)
        copy_action.setShortcut(QKeySequence.Copy)
        copy_action.setEnabled(False)
        edit_menu.addAction(copy_action)

        paste_action = QAction("&Paste", self)
        paste_action.setShortcut(QKeySequence.Paste)
        paste_action.setEnabled(False)
        edit_menu.addAction(paste_action)

    def _init_view_menu(self):
        """Initialize view menu"""
        view_menu = self.addMenu("&View")

        self._preview_action = QAction("&Preview", self)
        self._preview_action.setCheckable(True)
        self._preview_action.setChecked(False)
        self._preview_action.triggered.connect(self._on_preview_changed)
        view_menu.addAction(self._preview_action)

        self._show_points_action = QAction("Show &Points", self)
        self._show_points_action.setCheckable(True)
        self._show_points_action.setChecked(True)
        self._show_points_action.triggered.connect(self._on_show_points_changed)
        view_menu.addAction(self._show_points_action)

        view_menu.addSeparator()

        zoom_in_action = QAction("Zoom &In", self)
        zoom_in_action.setShortcut(QKeySequence.ZoomIn)
        view_menu.addAction(zoom_in_action)

        zoom_out_action = QAction("Zoom &Out", self)
        zoom_out_action.setShortcut(QKeySequence.ZoomOut)
        view_menu.addAction(zoom_out_action)

    def _init_help_menu(self):
        """Initialize help menu"""
        help_menu = self.addMenu("&Help")

        about_action = QAction("&About Typecast", self)
        about_action.triggered.connect(self._on_about)
        help_menu.addAction(about_action)

    def _on_open(self):
        """Open file"""
        self.open_file.emit()

    def _on_close(self):
        """Close file"""
        self.close_file.emit()

    def _on_export(self):
        """Export file"""
        self.export_file.emit()

    def _on_exit(self):
        """Exit application"""
        self.exit_app.emit()

    def _on_preview_changed(self, checked: bool):
        """
        Preview mode changed

        Args:
            checked: Whether preview is enabled
        """
        self._preview = checked
        self.preview_changed.emit(checked)

    def _on_show_points_changed(self, checked: bool):
        """
        Show control points changed

        Args:
            checked: Whether to show
        """
        self._show_points = checked
        self.show_points_changed.emit(checked)

    def _on_about(self):
        """Show about dialog"""
        self.about_app.emit()

    def set_font_collection(self, font_collection):
        """
        Set font collection

        Args:
            font_collection: OTFontCollection object
        """
        self._font_collection = font_collection

        if font_collection:
            self._close_action.setText(f"Close \"{font_collection.get_file_name()}\"")
            self._close_action.setEnabled(True)
        else:
            self._close_action.setText("Close")
            self._close_action.setEnabled(False)

    def is_preview(self) -> bool:
        """Check if preview mode is enabled"""
        return self._preview

    def is_show_points(self) -> bool:
        """Check if control points are shown"""
        return self._show_points