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

from biz.dfch.ste100parser import Token

from ...test_case_container_base import TestCaseContainerBase
from ...test_data.test_data import TestData


def pretty_with_meta(node, indent=0):

    assert not hasattr(node, 'type'), repr(node)
    assert hasattr(node, 'data'), repr(node)
    assert hasattr(node, 'children'), repr(node)
    assert hasattr(node, 'meta'), repr(node)
    assert hasattr(node.meta, 'line'), repr(node.meta)
    assert hasattr(node.meta, 'column'), repr(node.meta)
    assert hasattr(node.meta, 'start_pos'), repr(node.meta)
    assert hasattr(node.meta, 'end_pos'), repr(node.meta)

    prefix = "  " * indent

    meta_str = ""
    m = node.meta
    meta_str = f"L{m.line}:C{m.column} @ {m.start_pos}:{m.end_pos}"

    if (
        isinstance(node.children, list) and
        1 == len(node.children) and
        not hasattr(node.children[0], 'data') and
        isinstance(node.children[0], str)
    ):
        child = node.children[0]
        print(f"{prefix}{node.data}: '{child}' [{meta_str}]")
    else:
        print(f"{prefix}{node.data}: [{meta_str}]")

        for child in node.children:
            pretty_with_meta(child, indent + 1)


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

    def test_paragraph_continues_after_list_item(self):

        value = self.load_test_data(TestData.TEST_SENTENCE_IN_LIST_ITEM)

        expected = [
            Token.paragraph,
        ]
        self.assert_tree(value, expected)

        expected = [
            Token.TEXT,
            Token.WS,
            Token.TEXT,
            Token.list_item,
            Token.list_item,
            Token.list_item,
            Token.TEXT,
            Token.WS,
            Token.TEXT,
            Token.WS,
            Token.TEXT,
            Token.WS,
            Token.TEXT,
            Token.WS,
            Token.TEXT,
        ]
        self.assert_tree(value, expected, Token.paragraph, level=1)

    def test_single_paragraph(self):

        expected = [
            Token.paragraph,
        ]

        value = self.load_test_data(TestData.SINGLE_PARAGRAPH)

        self.assert_tree(value, expected)

    def test_single_paragraph_with_linebreak(self):

        expected = [
            Token.paragraph,
        ]

        value = self.load_test_data(TestData.SINGLE_PARAGRAPH_WITH_LINEBREAK)
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

        value = self.load_test_data(TestData.COMPLEX_HEADINGS_PARA_PROC_LIST)
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

        value = self.load_test_data(
            TestData.COMPLEX_HEADINGS_PROC_CITE_PARA_LIST)
        self.assert_tree(value, expected)
