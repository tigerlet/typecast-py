#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MainWindow - Main Window (Full Version)
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QSplitter, QTreeView, QTabWidget, QTextEdit,
                             QFileDialog, QMessageBox, QLabel, QStatusBar)
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QKeySequence
import sys

from .widgets.glyph_panel import GlyphPanel
from .widgets.editor_menu import EditorMenu
from .widgets.table_tree_builder import TableTreeBuilder
from core.ot.otfont_collection import OTFontCollection
from core.ot.otfont import OTFont


class MainWindow(QMainWindow):
    """
    Main Window (Full Version)

    Features:
    - Tree view for font table structure
    - Glyph editing panel
    - Hex dump view
    - Menu bar
    - Status bar
    - File operations
    """

    def __init__(self):
        """Initialize main window"""
        super().__init__()

        self._font_collections = []
        self._current_font = None
        self._current_glyph = None
        self._current_font_collection = None
        self._properties = {}
        self._tree_model = None

        self._init_ui()
        self._create_menu()
        self._create_statusbar()
        self._connect_signals()

        self.setWindowTitle("Typecast - OpenType Font Editor")
        self.setGeometry(100, 100, 1200, 800)

    def _init_ui(self):
        """Initialize UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        self._splitter = QSplitter(Qt.Horizontal)

        self._tree_model = TableTreeBuilder.create_tree_model()
        self._tree_view = QTreeView()
        self._tree_view.setModel(self._tree_model)
        self._tree_view.setHeaderHidden(False)
        self._tree_view.setRootIsDecorated(True)
        self._tree_view.clicked.connect(self._on_tree_item_clicked)
        self._tree_view.doubleClicked.connect(self._on_tree_item_double_clicked)

        self._splitter.addWidget(self._tree_view)

        self._tab_widget = QTabWidget()

        self._glyph_panel = GlyphPanel()
        self._tab_widget.addTab(self._glyph_panel, "Outline")

        self._dump_widget = QTextEdit()
        self._dump_widget.setReadOnly(True)
        self._dump_widget.setFontFamily("Monospace")
        self._tab_widget.addTab(self._dump_widget, "Dump")

        self._property_widget = QTextEdit()
        self._property_widget.setReadOnly(True)
        self._property_widget.setFontFamily("Monospace")
        self._tab_widget.addTab(self._property_widget, "Properties")

        self._splitter.addWidget(self._tab_widget)

        layout.addWidget(self._splitter)

        self._splitter.setSizes([300, 900])

    def _create_menu(self):
        """Create menu bar"""
        self._menu = EditorMenu(self)
        self.setMenuBar(self._menu)

    def _create_statusbar(self):
        """Create status bar"""
        self._statusbar = QStatusBar()
        self.setStatusBar(self._statusbar)
        self._statusbar.showMessage("Ready")

    def _connect_signals(self):
        """Connect signals"""
        self._menu.open_file.connect(self._open_font)
        self._menu.close_file.connect(self._close_font)
        self._menu.export_file.connect(self._export_font)
        self._menu.exit_app.connect(self.close)
        self._menu.preview_changed.connect(self._on_preview_changed)
        self._menu.show_points_changed.connect(self._on_show_points_changed)
        self._menu.about_app.connect(self._show_about)

    def _open_font(self):
        """Open font file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Font File",
            "",
            "OpenType Fonts (*.ttf *.ttc *.otf *.dfont);;All Files (*)"
        )

        if file_path:
            self._load_font(file_path)

    def _load_font(self, file_path: str):
        """
        Load font file

        Args:
            file_path: File path
        """
        try:
            fc = OTFontCollection.create(file_path)
            self._font_collections.append(fc)

            TableTreeBuilder.add_font_tree(self._tree_model, fc)

            self._menu.set_font_collection(fc)
            self._current_font_collection = fc

            self._statusbar.showMessage(f"Loaded: {fc.get_file_name()}")

        except Exception as e:
            import traceback
            error_msg = f"Failed to load font:\n{str(e)}\n\n{traceback.format_exc()}"
            print(error_msg)
            QMessageBox.critical(
                self,
                "Error",
                error_msg
            )

    def _close_font(self):
        """Close current font"""
        if not self._current_font_collection:
            return

        try:
            self._font_collections.remove(self._current_font_collection)

            root_item = self._tree_model.item(0)
            for i in range(root_item.rowCount()):
                item = root_item.child(i)
                if item.data() == self._current_font_collection:
                    root_item.removeRow(i)
                    break

            self._current_font_collection = None
            self._current_font = None
            self._current_glyph = None

            self._menu.set_font_collection(None)
            self._glyph_panel.set_glyph(None)
            self._dump_widget.clear()

            self._statusbar.showMessage("Font closed")

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to close font:\n{str(e)}"
            )

    def _export_font(self):
        """Export font"""
        if not self._current_font:
            QMessageBox.warning(self, "Warning", "No font selected")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Font",
            "",
            "SVG Files (*.svg);;All Files (*)"
        )

        if file_path:
            try:
                from ..export.svg_exporter import SVGExporter

                exporter = SVGExporter(self._current_font)
                exporter.export(file_path)

                QMessageBox.information(
                    self,
                    "Success",
                    "Font exported successfully"
                )

                self._statusbar.showMessage(f"Exported to: {file_path}")

            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to export:\n{str(e)}"
                )

    def _on_tree_item_clicked(self, index: QModelIndex):
        """
        Tree item clicked event

        Args:
            index: Clicked index
        """
        item = self._tree_model.itemFromIndex(index)

        if not item:
            return

        data = item.data()

        if isinstance(data, OTFontCollection):
            self._current_font_collection = data
            self._menu.set_font_collection(data)

        elif isinstance(data, OTFont):
            self._current_font = data
            self._glyph_panel.set_font(data)
            self._update_glyph_view(data)

        elif hasattr(data, 'to_string'):
            try:
                self._dump_widget.setText(data.to_string())
            except Exception as e:
                self._dump_widget.setText(f"Error displaying table:\n{str(e)}")

        elif isinstance(data, int):
            self._show_glyph_index(data)
            self._tab_widget.setCurrentIndex(0)

        else:
            item_text = item.text()
            if self._current_font:
                self._dump_widget.setText(f"Item: {item_text}\n\nClick to view details.")

    def _on_tree_item_double_clicked(self, index: QModelIndex):
        """
        Tree item double clicked event

        Args:
            index: Double clicked index
        """
        item = self._tree_model.itemFromIndex(index)

        if not item:
            return

        data = item.data()

        if isinstance(data, int):
            self._show_glyph_index(data)
            self._tab_widget.setCurrentIndex(0)

    def _update_glyph_view(self, font: OTFont):
        """
        Update glyph view

        Args:
            font: OTFont object
        """
        if not font:
            return

        info = f"Glyph Count: {font.get_num_glyphs()}\n"
        info += f"Ascent: {font.get_ascent()}\n"
        info += f"Descent: {font.get_descent()}\n\n"

        if font.get_head_table():
            head = font.get_head_table()
            info += f"Units per EM: {head.get_units_per_em()}\n"
            info += f"Bounding Box: ({head.get_x_min()}, {head.get_y_min()}) - ({head.get_x_max()}, {head.get_y_max()})\n"

        self._property_widget.setText(info)

    def _show_glyph_index(self, index: int):
        """
        Show glyph at index

        Args:
            index: Glyph index
        """
        if not self._current_font:
            if self._current_font_collection:
                self._current_font = self._current_font_collection.get_font(0)
            else:
                return

        try:
            glyph = self._current_font.get_glyph(index)

            if glyph:
                self._current_glyph = glyph
                self._glyph_panel.set_glyph(glyph, index)
                self._dump_widget.setText(glyph.to_string())
            else:
                self._glyph_panel.set_glyph(None)
                self._dump_widget.setText(f"No glyph at index {index}")

        except Exception as e:
            import traceback
            error_msg = f"Error loading glyph:\n{str(e)}\n\n{traceback.format_exc()}"
            print(error_msg)
            self._dump_widget.setText(error_msg)

    def _on_preview_changed(self, preview: bool):
        """
        Preview mode changed

        Args:
            preview: Whether to preview
        """
        self._glyph_panel.get_glyph_editor().set_preview_mode(preview)

    def _on_show_points_changed(self, show: bool):
        """
        Show control points changed

        Args:
            show: Whether to show
        """
        self._glyph_panel.get_glyph_editor().set_show_control_points(show)

    def _show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About Typecast",
            "<h2>Typecast</h2>"
            "<p>OpenType Font Editor</p>"
            "<p>Version 1.0</p>"
            "<p>A professional tool for viewing and editing OpenType fonts.</p>"
            "<p>Supports TTF, TTC, OTF, and DFont formats.</p>"
        )

    def closeEvent(self, event):
        """Close event"""
        self._glyph_panel.set_properties(self._properties)
        event.accept()


def main():
    """Main entry point"""
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    app.setApplicationName("Typecast")

    window = MainWindow()
    window.show()

    return app.exec_()


if __name__ == '__main__':
    sys.exit(main())