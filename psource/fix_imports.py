#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fix imports in UI modules
"""

import os
import re


def fix_imports(file_path):
    """Fix relative imports in a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        content = re.sub(r'from \.\.\.core\.ot', 'from core.ot', content)
        content = re.sub(r'from \.\.core\.ot', 'from core.ot', content)
        content = re.sub(r'from \.\.\.core', 'from core', content)
        content = re.sub(r'from \.\.core', 'from core', content)
        content = re.sub(r'from \.\.', 'from .', content)

        if content != original:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {file_path}")
            return True

    except Exception as e:
        print(f"Error fixing {file_path}: {e}")

    return False


def main():
    """Main function."""
    base_dir = os.path.dirname(os.path.abspath(__file__))

    for root, dirs, files in os.walk(base_dir):
        if '__pycache__' in root:
            continue

        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                fix_imports(file_path)

    print("\nAll imports fixed!")


if __name__ == '__main__':
    main()
