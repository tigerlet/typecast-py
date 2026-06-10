# TypeLens Quick Start Guide

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the program
python psource/main.py

# Or use the startup script
python run_TypeLens.py
```

## 📖 Basic Operations

### Open Font File
1. Click menu **File → Open** (or press `Ctrl+O`)
2. Select font file (.ttf, .ttc, .otf, .dfont)
3. The font will be displayed in the left tree view

### View Glyph Information
1. Click the font name in the left tree
2. View glyph statistics on the right
3. Click the "Dump" tab to view detailed data

### Edit Glyph
1. Click to select points in the glyph editor
2. Drag points to move them
3. Use Ctrl+Click for multi-point selection
4. Use Ctrl+A to select all points

### Export as SVG
1. Select the loaded font
2. Click **File → Export**
3. Choose save location
4. Save as .svg file

## 🎯 Main Features

### ✅ Implemented
- Open multiple font formats (TTF, TTC, OTF, DFont)
- View font tables in tree structure
- Glyph information display
- Glyph editing (point selection, drag, multi-select)
- Preview mode (fill/outline toggle)
- SVG export

### 🔄 To be Enhanced
- Undo/Redo functionality
- More export formats
- Glyph modification saving

## 🛠️ Troubleshooting

### PyQt6 Installation Failed
```bash
pip install PyQt6 --no-cache-dir
```

### Cannot Open Font File
- Check if the file is corrupted
- Try pure ASCII path
- Test with other fonts

### Program Unresponsive
- Close other programs to free memory
- Use smaller font files

## 📂 Project Structure

```
TypeLens/
├── psource/          # Python source code
│   ├── core/         # Core modules (OpenType parsing)
│   │   └── ot/       # OpenType font parsing
│   │       └── table/# Table implementation
│   ├── export/       # Export functions
│   ├── resources/    # Resource files
│   └── ui/           # User interface (main window, widgets)
├── README.md         # Complete design documentation
├── INSTALL.md        # Installation guide
├── QUICKSTART.md     # Quick start guide
├── requirements.txt  # Python dependencies
├── run_typeLens.py   # Startup script
└── simkai.ttf        # Sample font file
```

## 📚 More Resources

- **Complete Documentation**: See [README.md](README.md)
- **Installation Guide**: See [INSTALL.md](INSTALL.md)

## 💡 Tips

- Use `Ctrl+O` to quickly open files
- Use `Ctrl+E` to quickly export
- Use `Ctrl+A` to select all glyph points
- Use mouse wheel to zoom view
- Expand the left tree view to see detailed information
- Click different tabs to view different views

---

**Enjoy font editing!** 🎨