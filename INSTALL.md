# Typecast Python Installation and Usage Guide

## Directory Structure

```
typecast.py/
├── README.md                 # Complete design documentation
├── INSTALL.md               # This installation guide
├── PROJECT_SUMMARY.md       # Project summary
├── QUICKSTART.md            # Quick start guide
├── CORRECTIONS.md           # Correction records
├── requirements.txt          # Python dependencies
├── psource/                 # Python source code
│   ├── __init__.py
│   ├── main.py              # Main program entry
│   ├── test.py              # Test script
│   ├── core/                # Core modules
│   │   ├── __init__.py
│   │   └── ot/              # OpenType font parsing
│   │       ├── __init__.py
│   │       ├── point.py          # Point class
│   │       ├── fixed.py          # Fixed-point class
│   │       ├── glyph.py          # Glyph class
│   │       ├── otfont.py         # Font class
│   │       ├── otfont_collection.py  # Font collection
│   │       └── table/            # Table parsing module
│   │           ├── __init__.py
│   │           ├── table.py           # Table base class
│   │           ├── directory_entry.py  # Directory entry
│   │           ├── table_directory.py # Table directory
│   │           ├── table_factory.py   # Table factory
│   │           ├── head_table.py     # Header table
│   │           ├── maxp_table.py     # Maximum profile table
│   │           ├── hhea_table.py     # Horizontal header table
│   │           ├── hmtx_table.py     # Horizontal metrics table
│   │           ├── glyf_table.py      # Glyph table
│   │           ├── glyf_simple_descript.py  # Simple glyph description
│   │           ├── glyph_description.py     # Glyph description base class
│   │           ├── loca_table.py     # Glyph location table
│   │           └── ttc_header.py    # TTC header
│   ├── ui/                  # User interface module
│   │   ├── __init__.py
│   │   ├── main_window.py    # Main window
│   │   └── widgets/          # UI components
│   │       ├── __init__.py
│   │       ├── glyph_editor.py      # Glyph editor
│   │       ├── glyph_panel.py       # Glyph panel
│   │       ├── glyph_toolbar.py     # Edit toolbar
│   │       ├── glyph_statusbar.py   # Status bar
│   │       ├── character_map.py     # Character map
│   │       ├── editor_menu.py       # Menu system
│   │       └── table_tree_builder.py # Tree structure builder
│   ├── export/              # Export module
│   │   ├── __init__.py
│   │   └── svg_exporter.py  # SVG exporter
│   └── resources/           # Resource files
│       └── __init__.py
└── run_typecast.py          # Startup script
```

## System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, Linux
- **Dependencies**: PyQt5

## Installation Steps

### 1. Install Python Dependencies

Open terminal (Command Prompt or PowerShell on Windows), navigate to the project directory:

```bash
cd c:\Users\xqxym\Desktop\typecast.py
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Or:

```bash
pip install PyQt5
```

### 2. Verify Installation

Run the test script:

```bash
python psource/test.py
```

You should see messages indicating all tests passed.

### 3. Run the Application

There are several ways to run the program:

#### Method 1: Direct Run

```bash
python psource/main.py
```

#### Method 2: Use Startup Script

```bash
python run_typecast.py
```

## Feature Description

### Implemented Features

1. **Font File Loading**
   - Supports TTF (TrueType Font)
   - Supports TTC (TrueType Collection)
   - Supports OTF (OpenType Font)
   - Supports DFont (Mac)

2. **Font Parsing**
   - Parse table directory structure
   - Read font header information
   - Parse glyph outline data
   - Extract glyph metrics

3. **User Interface**
   - Tree structure display of font tables
   - Glyph information display
   - Hex dump viewing
   - File open and export

4. **Glyph Editing**
   - Point selection and drag editing
   - Multi-point selection (Ctrl+Click)
   - Select all (Ctrl+A)
   - Real-time coordinate update
   - Grid and axis display
   - Zoom and pan controls

5. **Preview Mode**
   - Fill display mode
   - Outline display mode
   - Toggle shortcut support

6. **Export Functions**
   - SVG format export

### Features to be Implemented

- [ ] Undo/Redo functionality
- [ ] More export formats (PNG, PDF, etc.)
- [ ] Glyph modification and saving
- [ ] Glyph search functionality
- [ ] Batch processing

## Usage Guide

### Open Font File

1. Run the program
2. Click **File → Open** in the menu bar (or press `Ctrl+O`)
3. Select a font file (.ttf, .ttc, .otf, .dfont)
4. The font will be displayed in the tree view on the left

### View Glyph Information

1. Click the font name in the left tree view
2. View glyph statistics in the tabs on the right
3. Click the "Dump" tab to view detailed data

### Export as SVG

1. Select the font to export
2. Click **File → Export** in the menu bar
3. Choose save location and file name
4. Click "Save"

## Troubleshooting

### Problem: PyQt5 Installation Failed

**Solutions**:

Windows:
```bash
pip install PyQt5
```

macOS:
```bash
brew install pyqt5
pip install pyqt5
```

Linux (Ubuntu/Debian):
```bash
sudo apt-get install python3-pyqt5
```

### Problem: Cannot Open Font File

**Possible Causes**:
1. File path contains Chinese characters
2. File is corrupted
3. File format not supported

**Solutions**:
1. Try copying the file to a pure ASCII path
2. Test with other font files
3. Check console error messages

### Problem: Program Unresponsive After Launch

**Possible Causes**:
1. Insufficient system resources
2. Font file is too large

**Solutions**:
1. Close other programs
2. Test with smaller font files

## Development Guide

### Adding New Table Types

1. Create a new table class file in `psource/core/ot/table/` directory
2. Inherit from the `Table` base class
3. Register the new table type in `table_factory.py`
4. Add getter method in `otfont.py`

Example:

```python
# New table class example
from .table import Table

class NewTable(Table):
    def __init__(self, directory_entry, data: bytes):
        super().__init__(directory_entry)
        # Parse table data

    def get_type(self) -> int:
        return Fixed.string_to_tag("newt")
```

### Adding New Export Formats

1. Create a new exporter class in `psource/export/` directory
2. Inherit from the base exporter interface
3. Implement export logic

## License

This project follows the license of the original Typecast project.

## Contact and Feedback

If you encounter any issues or have suggestions, please provide feedback through:

- Submit issues on the project Issue page
- Send email to the project maintainer

## References

- [OpenType Specification](https://docs.microsoft.com/en-us/typography/opentype/spec/)
- [PyQt5 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [TrueType Reference Manual](https://developer.apple.com/fonts/TrueType-Reference-Manual/)

---

**Version**: 1.0.0
**Last Updated**: 2026-05-24