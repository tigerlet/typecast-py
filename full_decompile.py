#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Comprehensive decompiler for Python bytecode files
"""

import marshal
import dis
import sys
import os
import types

def decompile_all_pyc_files(pyc_dir, output_dir=None):
    """Decompile all pyc files in a directory."""
    if output_dir is None:
        output_dir = pyc_dir.replace('__pycache__', 'decompiled')

    os.makedirs(output_dir, exist_ok=True)

    pyc_files = [f for f in os.listdir(pyc_dir) if f.endswith('.pyc')]

    for pyc_file in sorted(pyc_files):
        pyc_path = os.path.join(pyc_dir, pyc_file)
        output_file = os.path.join(output_dir, pyc_file.replace('.cpython-314.pyc', '.txt'))

        print(f"\n{'='*80}")
        print(f"Decompiling: {pyc_file}")
        print(f"Output: {output_file}")
        print('='*80)

        try:
            with open(pyc_path, 'rb') as f:
                # Skip header
                f.read(16)
                code = marshal.load(f)

            # Write to file
            with open(output_file, 'w', encoding='utf-8') as out:
                out.write(f"File: {pyc_file}\n")
                out.write(f"Module code: {code.co_name}\n\n")

                out.write("Disassembly:\n")
                out.write("-" * 80 + "\n")

                dis.dis(code, file=out)

            print(f"Successfully decompiled to {output_file}")

        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python full_decompile.py <pycache_dir> [output_dir]")
        print("Example: python full_decompile.py psource/core/ot/__pycache__")
        sys.exit(1)

    pyc_dir = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.isdir(pyc_dir):
        print(f"Error: {pyc_dir} is not a directory")
        sys.exit(1)

    decompile_all_pyc_files(pyc_dir, output_dir)
    print("\nDecompilation complete!")

if __name__ == '__main__':
    main()
