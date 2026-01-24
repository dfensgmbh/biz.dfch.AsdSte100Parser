# Copyright (C) 2026 Ronald Rink, d-fens GmbH, http://d-fens.ch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# pylint: disable=C0115
# pylint: disable=C0116
# type: ignore

"""test_texts"""

from lark import Tree

from biz.dfch.ste100parser import Token

from ...test_case_container_base import TestCaseContainerBase
from ...test_data.test_data import TestData


def pretty_with_meta1(tree, indent=0):
    """Print a Lark Tree with metadata."""
    prefix = "  " * indent

    if isinstance(tree, Tree):
        # It's a Tree node (non-terminal)
        meta_str = ""
        if hasattr(tree, 'meta'):
            meta = tree.meta
            parts = []
            if hasattr(meta, 'line'):
                parts.append(f"L{meta.line}:C{meta.column}")
            if hasattr(meta, 'start_pos'):
                parts.append(f"pos:{meta.start_pos}-{meta.end_pos}")
            meta_str = f" [{', '.join(parts)}]" if parts else ""

        print(f"{prefix}{tree.data}{meta_str}")

        # Recursively print children
        for child in tree.children:
            pretty_with_meta(child, indent + 1)

    elif isinstance(tree, Token):
        # It's a Token (terminal)
        token_meta = ""
        if hasattr(tree, 'line'):
            token_meta = f" [L{tree.line}:C{tree.column}]"
        print(f"{prefix}{tree.type}: {repr(str(tree))}{token_meta}")

    else:
        # It's a plain string or other primitive value
        print(f"{prefix}{type(tree).__name__}: {repr(tree)}")


def pretty_with_meta2(node, indent=0):
    prefix = "  " * indent

    if isinstance(node, Tree):
        # 1. Handle Tree Nodes (Non-terminals)
        meta_str = ""
        if hasattr(node, 'meta'):
            m = node.meta
            # Earley with propagate_positions=True provides these:
            meta_str = f" [L{m.line}:C{m.column} -> L{m.end_line}:C{m.end_column}]"

        print(f"{prefix}{node.data}{meta_str}")

        for child in node.children:
            pretty_with_meta(child, indent + 1)

    elif isinstance(node, Token):
        # 2. Handle Tokens (Terminals)
        # Tokens store line/column/pos directly on themselves
        loc = f" [L{node.line}:C{node.column}, pos:{node.start_pos}]"
        print(f"{prefix}{node.type}: {repr(str(node))}{loc}")

    else:
        # 3. Handle anything else (Strings, None, etc.)
        print(f"{prefix}{type(node).__name__}: {repr(node)}")


def pretty_with_meta(node, indent=0):
    prefix = "  " * indent

    # 1. Check if it's a Tree (has 'data' and 'children')
    if hasattr(node, 'data') and hasattr(node, 'children'):
        meta_str = ""
        if hasattr(node, 'meta') and hasattr(node.meta, 'line'):
            m = node.meta
            meta_str = f" [L{m.line}:C{m.column} @ {m.start_pos}:{m.end_pos}]"

        print(f"{prefix}{node.data}{meta_str}")
        for child in node.children:
            pretty_with_meta(child, indent + 1)

    # 2. Check if it's a Token (has 'type' attribute)
    elif hasattr(node, 'type'):
        # Extract location info safely
        line = getattr(node, 'line', '?')
        col = getattr(node, 'column', '?')
        pos = getattr(node, 'start_pos', getattr(node, 'pos_in_stream', '?'))

        loc = f" [L{line}:C{col}, pos:{pos}]"
        print(f"{prefix}{node.type}: {repr(str(node))}{loc}")

    # 3. Fallback for plain strings or unexpected objects
    else:
        print(f"{prefix}{type(node).__name__}: {repr(node)}")


class TestTexts(TestCaseContainerBase):

    def assert_tree(
        self,
        value: str,
        expected,
        start_token: Token = Token.start,
        level: int = 0,
    ):

        initial = self.invoke(value)
        # pretty_with_meta(initial)
        transformed = self.transform(initial)

        print(transformed.pretty())
        pretty_with_meta(transformed)

        token_tree = self.get_token_tree(transformed)
        token, children = token_tree
        for _ in range(level):
            token, children = children[0]
        self.assertEqual(start_token, token)

        result = self.get_tokens(children)
        self.assertEqual(expected, result)

    def test_proc_newline_para_at_end(self):

        expected = [
            Token.proc_item,
            Token.paragraph,
            Token.paragraph,
        ]

        value = """
1. This is work step 1.

This is a paragraph.

This is another paragraph.

"""

        self.assert_tree(value, expected)

    def test_proc_with_warning_at_end(self):

        expected = [
            Token.proc_item,
        ]

        value = """
1. This is work step 1.
WARNING: This is a safety instruction.

"""

        self.assert_tree(value, expected)

    def test_proc_with_caution_at_end(self):

        expected = [
            Token.proc_item,
        ]

        value = """
1. This is work step 1.
CAUTION: This is a safety instruction.

"""

        self.assert_tree(value, expected)

    def test_proc_with_note_at_end(self):

        expected = [
            Token.proc_item,
        ]

        value = """
1. This is work step 1.
NOTE: This is a note.

"""
        self.assert_tree(value, expected)

    def test_para_with_note_at_end(self):

        expected = [
            Token.paragraph,
            Token.NOTE,
        ]

        value = """This is a paragraph.
NOTE: This is a note.

"""

        self.assert_tree(value, expected)

    def test_para_with_cite_at_end(self):

        expected = [
            Token.paragraph,
            Token.cite,
        ]

        value = """This is a paragraph.
> This is a citation.

"""

        self.assert_tree(value, expected)

    def test_single_paragraph(self):

        expected = [
            Token.paragraph,
        ]

        value = self.load_test_file(TestData.SINGLE_PARAGRAPH)

        self.assert_tree(value, expected)

    def test_single_paragraph_with_linebreak(self):

        expected = [
            Token.paragraph,
        ]

        value = self.load_test_file(TestData.SINGLE_PARAGRAPH_WITH_LINEBREAK)
        self.assert_tree(value, expected)

    def test_complex_headings_para_proc_list(self):

        expected = [
            Token.heading,
            Token.cite,
            Token.cite,
            Token.cite,
            Token.NOTE,
            Token.paragraph,
            Token.paragraph,
            Token.heading,
            Token.proc_item,
            Token.proc_item,
            Token.proc_item,
            Token.proc_item,
            Token.NOTE,
            Token.paragraph,
        ]

        value = self.load_test_file(TestData.COMPLEX_HEADINGS_PARA_PROC_LIST)
        self.assert_tree(value, expected)

    def test_complex_headings_proc_cite_para_list(self):

        expected = [
            Token.heading,
            Token.paragraph,
            Token.paragraph,
            Token.heading,
            Token.proc_item,
            Token.proc_item,
            Token.proc_item,
            Token.paragraph,
            Token.paragraph,
            Token.paragraph,
            Token.proc_item,
            Token.proc_item,
            Token.cite,
            Token.cite,
            Token.paragraph,
            Token.cite,
            Token.cite,
        ]

        value = self.load_test_file(
            TestData.COMPLEX_HEADINGS_PROC_CITE_PARA_LIST)
        self.assert_tree(value, expected)
