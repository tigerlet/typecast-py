#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script for Typecast Python port
Tests basic functionality of the OpenType font parser
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def test_point():
    """Test Point class."""
    print("Testing Point class...")

    from core.ot.point import Point

    p = Point(100, 200, True, False)
    assert p.x == 100, f"Expected x=100, got {p.x}"
    assert p.y == 200, f"Expected y=200, got {p.y}"
    assert p.on_curve == True, f"Expected on_curve=True, got {p.on_curve}"
    assert p.end_of_contour == False, f"Expected end_of_contour=False, got {p.end_of_contour}"

    p.scale(0.5)
    assert p.x == 50, f"Expected scaled x=50, got {p.x}"
    assert p.y == 100, f"Expected scaled y=100, got {p.y}"

    print("  ✓ Point class tests passed")


def test_fixed():
    """Test Fixed class."""
    print("Testing Fixed class...")

    from core.ot.fixed import Fixed

    value = Fixed.int_value(1.5)
    assert value == int(1.5 * 65536), f"Expected {int(1.5 * 65536)}, got {value}"

    float_val = Fixed.float_value(value)
    assert abs(float_val - 1.5) < 0.001, f"Expected ~1.5, got {float_val}"

    tag = Fixed.string_to_tag("glyf")
    assert tag == 0x676C7966, f"Expected 0x676C7966, got {tag:#x}"

    tag_str = Fixed.tag_to_string(tag)
    assert tag_str == "glyf", f"Expected 'glyf', got '{tag_str}'"

    print("  ✓ Fixed class tests passed")


def test_directory_entry():
    """Test DirectoryEntry class."""
    print("Testing DirectoryEntry class...")

    from core.ot.table.directory_entry import DirectoryEntry

    data = b'glyf' + b'\x00\x00\x00\x00' + b'\x00\x00\x00\x64' + b'\x00\x00\x00\x32'

    entry = DirectoryEntry(data)
    assert entry.tag == 0x676C7966, f"Expected tag 0x676C7966, got {entry.tag:#x}"
    assert entry.offset == 100, f"Expected offset 100, got {entry.offset}"
    assert entry.length == 50, f"Expected length 50, got {entry.length}"

    print("  ✓ DirectoryEntry class tests passed")


def test_imports():
    """Test module imports."""
    print("Testing module imports...")

    try:
        from core.ot import OTFontCollection, OTFont, Glyph, Point, Fixed
        from ui.main_window import MainWindow
        from export.svg_exporter import SVGExporter
        from ui.widgets import GlyphPanel, GlyphEditor, GlyphToolbar, GlyphStatusBar

        print("  ✓ All imports successful")
        return True

    except ImportError as e:
        print(f"  ✗ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_glyph():
    """Test Glyph class."""
    print("Testing Glyph class...")

    from core.ot.glyph import Glyph

    glyph = Glyph(None, 100, 500)
    assert glyph.get_advance_width() == 500, f"Expected advance_width=500, got {glyph.get_advance_width()}"
    assert glyph.get_left_side_bearing() == 100, f"Expected lsb=100, got {glyph.get_left_side_bearing()}"
    assert glyph.get_point_count() == 2, f"Expected 2 points, got {glyph.get_point_count()}"

    print("  ✓ Glyph class tests passed")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Typecast Python Port - Test Suite")
    print("=" * 60)
    print()

    tests_passed = 0
    tests_failed = 0

    try:
        test_point()
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Point class tests failed: {e}")
        tests_failed += 1

    try:
        test_fixed()
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Fixed class tests failed: {e}")
        tests_failed += 1

    try:
        test_directory_entry()
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ DirectoryEntry class tests failed: {e}")
        tests_failed += 1

    try:
        test_glyph()
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Glyph class tests failed: {e}")
        tests_failed += 1

    try:
        if test_imports():
            tests_passed += 1
        else:
            tests_failed += 1
    except Exception as e:
        print(f"  ✗ Import tests failed: {e}")
        tests_failed += 1

    print()
    print("=" * 60)
    print(f"Test Results: {tests_passed} passed, {tests_failed} failed")
    print("=" * 60)

    if tests_failed == 0:
        print()
        print("✓ All tests passed successfully!")
        print()
        print("To run the application:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Run: python run_typecast.py")
        print()
        return 0
    else:
        print()
        print("✗ Some tests failed. Please check the errors above.")
        print()
        return 1


if __name__ == '__main__':
    sys.exit(main())
