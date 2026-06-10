#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Quick launcher script for TypeLens Python version
"""

import os
import sys

psource_dir = os.path.join(os.path.dirname(__file__), 'psource')
sys.path.insert(0, psource_dir)

try:
    from PyQt6.QtWidgets import QApplication

    from ui.main_window import MainWindow

    def main():
        """Main entry point."""
        app = QApplication(sys.argv)
        app.setApplicationName("TypeLens")

        window = MainWindow()
        window.show()

        return app.exec()

    if __name__ == '__main__':
        sys.exit(main())

except ImportError as e:
    print("Error: PyQt6 is not installed.")
    print()
    print("Please install the required dependencies:")
    print("  pip install PyQt6")
    print()
    print(f"Import error: {e}")
    sys.exit(1)