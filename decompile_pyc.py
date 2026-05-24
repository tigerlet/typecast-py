#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Decompile pyc files to extract source code information
"""

import marshal
import dis
import sys
import os

def decompile_pyc(pyc_path):
    """Decompile a pyc file and extract bytecode information."""
    try:
        with open(pyc_path, 'rb') as f:
            # Skip the header (16 bytes for Python 3.6+)
            f.read(16)
            code = marshal.load(f)

        print(f"\n{'='*60}")
        print(f"File: {pyc_path}")
        print(f"{'='*60}")

        # Print code object information
        print(f"\nCode object name: {code.co_name}")
        print(f"First line number: {code.co_firstlineno}")
        print(f"Number of locals: {code.co_nlocals}")
        print(f"Constants: {[c for c in code.co_consts if c is not None]}")
        print(f"Names: {list(code.co_names)}")

        # Disassemble
        print("\nBytecode:")
        dis.dis(code)

        return code
    except Exception as e:
        print(f"Error decompiling {pyc_path}: {e}")
        return None

def main():
    """Main function."""
    if len(sys.argv) > 1:
        decompile_pyc(sys.argv[1])
    else:
        print("Usage: python decompile_pyc.py <pyc_file>")

if __name__ == '__main__':
    main()
