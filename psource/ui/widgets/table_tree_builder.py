#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TableTreeBuilder - Tree Structure Builder
"""

from PyQt6.QtGui import QStandardItemModel, QStandardItem
from core.ot.otfont_collection import OTFontCollection
from core.ot.otfont import OTFont
from core.ot.fixed import Fixed


class TableTreeBuilder:
    """
    Tree Structure Builder

    Builds font table structure into Qt tree model
    """

    @staticmethod
    def create_tree_model():
        """
        Create tree model

        Returns:
            QStandardItemModel
        """
        root_item = QStandardItem("Fonts")
        model = QStandardItemModel()
        model.appendRow(root_item)
        return model

    @staticmethod
    def add_font_tree(model: QStandardItemModel, font_collection: OTFontCollection):
        """
        Add font to tree model

        Args:
            model: QStandardItemModel
            font_collection: OTFontCollection object
        """
        collection_node = QStandardItem(font_collection.get_file_name())
        collection_node.setData(font_collection)
        collection_node.setEditable(False)

        for i in range(font_collection.get_font_count()):
            font = font_collection.get_font(i)
            font_node = TableTreeBuilder._create_font_node(font, i)
            collection_node.appendRow(font_node)

        root_item = model.item(0)
        root_item.appendRow(collection_node)

    @staticmethod
    def _create_font_node(font: OTFont, index: int) -> QStandardItem:
        """
        Create font node

        Args:
            font: OTFont object
            index: Font index

        Returns:
            QStandardItem
        """
        name = f"Font {index + 1}"

        if font.get_name_table():
            try:
                name = font.get_name_table().get_record_string(4)
            except:
                pass

        font_node = QStandardItem(name)
        font_node.setData(font)
        font_node.setEditable(False)

        td = font.get_table_directory()
        if td:
            for i in range(td.get_num_tables()):
                entry = td.get_entry(i)
                table_node = TableTreeBuilder._create_table_node(font, entry)
                font_node.appendRow(table_node)

        return font_node

    @staticmethod
    def _create_table_node(font: OTFont, entry) -> QStandardItem:
        """
        Create table node

        Args:
            font: OTFont object
            entry: DirectoryEntry object

        Returns:
            QStandardItem
        """
        tag_str = Fixed.tag_to_string(entry.tag)
        table = font.get_table(entry.tag)

        node = QStandardItem(tag_str)
        node.setData(table)
        node.setEditable(False)

        if entry.tag == 0x6e616d65:  # 'name'
            TableTreeBuilder._add_name_table(font, node)
        elif entry.tag == 0x636d6170:  # 'cmap'
            TableTreeBuilder._add_cmap_table(font, node)
        elif entry.tag == 0x676c7966:  # 'glyf'
            TableTreeBuilder._add_glyf_table(font, node)

        return node

    @staticmethod
    def _add_name_table(font: OTFont, parent: QStandardItem):
        """Add name table"""
        name_table = font.get_name_table()
        if name_table:
            records = name_table.get_name_records()
            for record in records[:20]:
                lang = record.get('language_id', 0)
                platform = record['platform_id']
                name = record.get('name', f"Record {platform}:{lang}")
                value = record.get('value', '')
                display_name = f"{name}: {value}" if value else name
                node = QStandardItem(display_name)
                node.setData(record)
                node.setEditable(False)
                parent.appendRow(node)

    @staticmethod
    def _add_cmap_table(font: OTFont, parent: QStandardItem):
        """Add character map table"""
        cmap_table = font.get_cmap_table()
        if cmap_table:
            entries = cmap_table.get_entries()
            for entry in entries:
                platform_id = entry.get_platform_id()
                platform_name = TableTreeBuilder._get_platform_name(platform_id)
                encoding_id = entry.get_encoding_id()
                node = QStandardItem(f"Platform ID: {platform_id} ({platform_name})")
                node.setData(entry.get_format())
                node.setEditable(False)
                parent.appendRow(node)

    @staticmethod
    def _get_platform_name(platform_id: int) -> str:
        """Get platform name"""
        names = {
            0: "Unicode",
            1: "Mac",
            2: "ISO",
            3: "Microsoft",
            4: "Custom"
        }
        return names.get(platform_id, f"Unknown {platform_id}")

    @staticmethod
    def _add_glyf_table(font: OTFont, parent: QStandardItem):
        """Add glyph table"""
        glyf_table = font.get_glyf_table()
        if not glyf_table:
            return

        post_table = font.get_post_table()
        num_glyphs = font.get_num_glyphs()

        for i in range(num_glyphs):
            glyph_name = f"{i}"

            if post_table:
                try:
                    name = post_table.get_glyph_name(i)
                    if name:
                        glyph_name = f"{i} {name}"
                except:
                    pass

            glyph_node = QStandardItem(glyph_name)
            glyph_node.setData(i)
            glyph_node.setEditable(False)
            parent.appendRow(glyph_node)