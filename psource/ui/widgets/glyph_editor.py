#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GlyphEditor - Glyph Editor Widget (Enhanced Version)
"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPoint, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QMouseEvent, QWheelEvent, QPainterPath
from core.ot.glyph import Glyph
from core.ot.otfont import OTFont


class GlyphEditor(QWidget):
    """
    Glyph Editor Widget (Enhanced Version)

    Features:
    - Display glyph outlines
    - Zoom and pan
    - Show control points
    - Point selection and drag editing
    - Preview mode (fill display)
    - Real-time updates
    """

    glyph_changed = pyqtSignal(int)
    point_selected = pyqtSignal(int)

    def __init__(self, parent=None):
        """Initialize glyph editor"""
        super().__init__(parent)

        self._glyph = None
        self._font = None
        self._units_per_em = 1000
        self._scale_factor = 0.25
        self._translate_x = 0
        self._translate_y = 0

        self._show_control_points = True
        self._preview_mode = False
        self._show_grid = True

        self._selected_points = set()
        self._drag_start = None
        self._drag_offset = {}
        self._current_tool = "select"

        self.setMinimumSize(800, 800)
        self.setMaximumSize(2000, 2000)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setMouseTracking(True)

    def set_font(self, font: OTFont):
        """Set font"""
        self._font = font
        if font and font.get_head_table():
            self._units_per_em = font.get_head_table().get_units_per_em()

    def set_glyph(self, glyph: Glyph, index: int = 0):
        """Set glyph"""
        self._glyph = glyph
        self._glyph_index = index
        self._selected_points.clear()
        self.update()
        self.glyph_changed.emit(index)

    def get_glyph(self) -> Glyph:
        """Get current glyph"""
        return self._glyph

    def get_font(self) -> OTFont:
        """Get font"""
        return self._font

    def set_scale_factor(self, scale: float):
        """Set scale factor"""
        self._scale_factor = max(0.05, min(5.0, scale))
        self.update()

    def get_scale_factor(self) -> float:
        """Get scale factor"""
        return self._scale_factor

    def set_show_control_points(self, show: bool):
        """Set whether to show control points"""
        self._show_control_points = show
        self.update()

    def set_preview_mode(self, preview: bool):
        """Set preview mode"""
        self._preview_mode = preview
        self.update()

    def set_show_grid(self, show: bool):
        """Set whether to show grid"""
        self._show_grid = show
        self.update()

    def set_current_tool(self, tool: str):
        """Set current tool"""
        self._current_tool = tool

    def paintEvent(self, event):
        """Draw glyph"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width = self.width()
        height = self.height()

        self._translate_x = width // 2
        self._translate_y = height // 2

        if self._show_grid:
            self._draw_grid(painter)
        self._draw_axes(painter)
        self._draw_glyph(painter)
        if self._show_control_points:
            self._draw_control_points(painter)

    def _draw_grid(self, painter: QPainter):
        """Draw grid"""
        painter.setPen(QPen(QColor(240, 240, 240), 1))

        grid_size = int(self._units_per_em * self._scale_factor / 10)

        for x in range(0, self.width(), max(1, grid_size)):
            painter.drawLine(x, 0, x, self.height())

        for y in range(0, self.height(), max(1, grid_size)):
            painter.drawLine(0, y, self.width(), y)

    def _draw_axes(self, painter: QPainter):
        """Draw axes"""
        pen = QPen(QColor(200, 200, 200), 1)
        painter.setPen(pen)

        units = int(self._units_per_em * self._scale_factor)
        x1 = self._translate_x - units
        x2 = self._translate_x + units
        y = self._translate_y

        painter.drawLine(x1, y, x2, y)

        y1 = self._translate_y - units
        y2 = self._translate_y + units
        x = self._translate_x

        painter.drawLine(x, y1, x, y2)

        if self._font:
            ascent = self._font.get_ascent()
            descent = self._font.get_descent()

            pen.setColor(QColor(180, 180, 180))
            painter.setPen(pen)

            y_ascent = self._translate_y - int(ascent * self._scale_factor)
            painter.drawLine(x1, y_ascent, x2, y_ascent)

            y_descent = self._translate_y - int(descent * self._scale_factor)
            painter.drawLine(x1, y_descent, x2, y_descent)

    def _draw_glyph(self, painter: QPainter):
        """Draw glyph outline"""
        if not self._glyph:
            return

        if self._preview_mode:
            pen = QPen(QColor(100, 100, 100), 2)
            painter.setPen(pen)
            brush_color = QColor(100, 100, 100, 50)
            painter.setBrush(brush_color)
        else:
            pen = QPen(QColor(0, 0, 0), 2)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)

        point_count = self._glyph.get_point_count()

        if point_count == 0:
            return

        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)

        contour_start = 0
        i = 0

        while i < point_count:
            point = self._glyph.get_point(i)

            if point.end_of_contour:
                contour_end = i
                self._add_contour_to_path(path, contour_start, contour_end)
                contour_start = i + 1

            i += 1

        painter.drawPath(path)

    def _add_contour_to_path(self, path: QPainterPath, start: int, end: int):
        """Add single contour to path (following Java PathFactory implementation)"""
        points = []
        count = end - start + 1

        for i in range(start, end + 1):
            p = self._glyph.get_point(i)
            x = self._translate_x + int(p.x * self._scale_factor)
            y = self._translate_y - int(p.y * self._scale_factor)
            points.append((x, y, p.on_curve))

        if not points:
            return

        offset = 0
        connect = False

        while offset < count:
            x_minus1, y_minus1, on_minus1 = points[(offset - 1) % count]
            x, y, on_curve = points[offset % count]
            x_plus1, y_plus1, on_plus1 = points[(offset + 1) % count]
            x_plus2, y_plus2, on_plus2 = points[(offset + 2) % count]

            if on_curve and on_plus1:
                if connect:
                    path.lineTo(x_plus1, y_plus1)
                else:
                    path.moveTo(x, y)
                    path.lineTo(x_plus1, y_plus1)
                    connect = True
                offset += 1
            elif on_curve and not on_plus1 and on_plus2:
                if connect:
                    path.quadTo(x_plus1, y_plus1, x_plus2, y_plus2)
                else:
                    path.moveTo(x, y)
                    path.quadTo(x_plus1, y_plus1, x_plus2, y_plus2)
                    connect = True
                offset += 2
            elif on_curve and not on_plus1 and not on_plus2:
                mid_x = (x_plus1 + x_plus2) // 2
                mid_y = (y_plus1 + y_plus2) // 2
                if connect:
                    path.quadTo(x_plus1, y_plus1, mid_x, mid_y)
                else:
                    path.moveTo(x, y)
                    path.quadTo(x_plus1, y_plus1, mid_x, mid_y)
                    connect = True
                offset += 2
            elif not on_curve and not on_plus1:
                mid_x0 = (x_minus1 + x) // 2
                mid_y0 = (y_minus1 + y) // 2
                mid_x1 = (x + x_plus1) // 2
                mid_y1 = (y + y_plus1) // 2
                if connect:
                    path.quadTo(x, y, mid_x1, mid_y1)
                else:
                    path.moveTo(mid_x0, mid_y0)
                    path.quadTo(x, y, mid_x1, mid_y1)
                    connect = True
                offset += 1
            elif not on_curve and on_plus1:
                mid_x = (x_minus1 + x) // 2
                mid_y = (y_minus1 + y) // 2
                if connect:
                    path.quadTo(x, y, x_plus1, y_plus1)
                else:
                    path.moveTo(mid_x, mid_y)
                    path.quadTo(x, y, x_plus1, y_plus1)
                    connect = True
                offset += 1
            else:
                offset += 1

        path.closeSubpath()

    def _draw_single_contour(self, painter: QPainter, start: int, end: int):
        """Draw single contour (following Java PathFactory implementation)"""
        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        self._add_contour_to_path(path, start, end)
        painter.drawPath(path)

    def _draw_control_points(self, painter: QPainter):
        """Draw control points"""
        if not self._glyph:
            return

        point_count = self._glyph.get_point_count()

        for i in range(point_count):
            point = self._glyph.get_point(i)

            x = self._translate_x + int(point.x * self._scale_factor)
            y = self._translate_y - int(point.y * self._scale_factor)

            is_selected = i in self._selected_points

            if point.on_curve:
                if is_selected:
                    painter.setBrush(QColor(0, 120, 215))
                    painter.setPen(QPen(QColor(0, 0, 255), 2))
                else:
                    painter.setBrush(QColor(0, 0, 0))
                    painter.setPen(QPen(QColor(0, 0, 0), 2))
                painter.drawRect(x - 2, y - 2, 5, 5)
            else:
                if is_selected:
                    painter.setPen(QPen(QColor(0, 120, 215), 2))
                    painter.setBrush(QColor(0, 120, 215, 100))
                else:
                    painter.setPen(QPen(QColor(0, 0, 0), 2))
                    painter.setBrush(Qt.NoBrush)
                painter.drawRect(x - 2, y - 2, 5, 5)

            font = QFont()
            font.setPointSize(7)
            painter.setFont(font)
            painter.setPen(QPen(QColor(80, 80, 80), 1))
            painter.drawText(x + 5, y - 5, str(i))

    def mousePressEvent(self, event: QMouseEvent):
        """Mouse press event"""
        if event.button() == Qt.LeftButton:
            if self._show_control_points and self._glyph:
                index = self._find_point_at(event.pos())

                if index >= 0:
                    if event.modifiers() & Qt.ControlModifier:
                        point = self._glyph.get_point(index)
                        point.on_curve = not point.on_curve
                        self.update()
                    else:
                        if index not in self._selected_points:
                            self._selected_points.clear()
                            self._selected_points.add(index)

                        self._drag_start = event.pos()
                        self._drag_offset = {}

                        for idx in self._selected_points:
                            p = self._glyph.get_point(idx)
                            self._drag_offset[idx] = (p.x, p.y)

                        self.update()
                        self.point_selected.emit(index)
                else:
                    self._selected_points.clear()
                    self.update()

    def mouseMoveEvent(self, event: QMouseEvent):
        """Mouse move event"""
        if event.buttons() & Qt.LeftButton and self._drag_start and self._glyph:
            pos = event.pos()

            dx = int((pos.x() - self._drag_start.x()) / self._scale_factor)
            dy = int(-(pos.y() - self._drag_start.y()) / self._scale_factor)

            for idx in self._selected_points:
                if idx in self._drag_offset:
                    orig_x, orig_y = self._drag_offset[idx]
                    p = self._glyph.get_point(idx)
                    p.x = orig_x + dx
                    p.y = orig_y + dy

            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        """Mouse release event"""
        self._drag_start = None
        self._drag_offset = {}

    def wheelEvent(self, event: QWheelEvent):
        """Mouse wheel zoom"""
        delta = event.angleDelta().y()

        if event.modifiers() & Qt.ControlModifier:
            if delta > 0:
                self._scale_factor *= 1.1
            else:
                self._scale_factor *= 0.9
        else:
            if delta > 0:
                self._scale_factor *= 1.05
            else:
                self._scale_factor *= 0.95

        self._scale_factor = max(0.05, min(5.0, self._scale_factor))
        self.update()

    def _find_point_at(self, pos: QPoint) -> int:
        """Find point at position"""
        if not self._glyph:
            return -1

        tolerance = max(8, int(10 / self._scale_factor))
        point_count = self._glyph.get_point_count()

        for i in range(point_count):
            point = self._glyph.get_point(i)

            x = self._translate_x + int(point.x * self._scale_factor)
            y = self._translate_y - int(point.y * self._scale_factor)

            if abs(pos.x() - x) <= tolerance and abs(pos.y() - y) <= tolerance:
                return i

        return -1

    def keyPressEvent(self, event):
        """Key press event"""
        if event.key() == Qt.Key_Delete or event.key() == Qt.Key_Backspace:
            pass

        elif event.key() == Qt.Key_A and event.modifiers() & Qt.ControlModifier:
            self._select_all_points()

        elif event.key() == Qt.Key_Escape:
            self._selected_points.clear()
            self.update()

        elif event.key() == Qt.Key_V:
            self._current_tool = "select"

        elif event.key() == Qt.Key_P:
            self._current_tool = "point"

        elif event.key() == Qt.Key_G:
            self._show_grid = not self._show_grid
            self.update()

    def _select_all_points(self):
        """Select all points"""
        if self._glyph:
            self._selected_points = set(range(self._glyph.get_point_count()))
            self.update()

    def get_selected_points(self) -> set:
        """Get selected points"""
        return self._selected_points.copy()

    def clear_selection(self):
        """Clear selection"""
        self._selected_points.clear()
        self.update()