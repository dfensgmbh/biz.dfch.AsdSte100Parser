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
from biz.dfch.ste100parser import Char

from ...test_case_text_base import TestCaseTextBase
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

    prefix = Char.SPACE * indent

    meta_str = Char.EMPTY
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


class TestTexts(TestCaseTextBase):

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

        value = self.load_test_data(TestData.SINGLE_PARAGRAPH)

        self.assert_tree(value, expected)

    def test_sentence_in_cite(self):

        value = "> Yes, this is a cite block. With two sentences."

        expected = [
            Token.sentence,
            Token.sentence,
        ]

        self.assert_tree(value, expected, Token.cite)

        expected = [
            Token.TEXT,     # Yes
            Token.TEXT,    # ,
            Token.WS,
            Token.TEXT,     # This
            Token.WS,
            Token.TEXT,     # is
            Token.WS,
            Token.TEXT,     # a
            Token.WS,
            Token.TEXT,     # cite
            Token.WS,
            Token.TEXT,     # block
            Token.TEXT,      # .
        ]

        self.assert_tree(value, expected, Token.sentence, level=1)

    def test_sentence_extraction(self):

        value = """Thus, we have no '.' choice."""
        value = """AndX yes, after 1.25 hours, there is a sign: 'Do not enter'."""

        expected = [
            Token.paragraph,
        ]
        self.assert_tree(value, expected)

        expected = [
            Token.sentence,
        ]
        self.assert_tree(value, expected, Token.paragraph, level=1)

        expected = [
            Token.TEXT,     # AndX
            Token.WS,
            Token.TEXT,     # yes
            Token.TEXT,    # ,
            Token.WS,
            Token.TEXT,     # after
            Token.WS,
            Token.TEXT,     # 1.25
            Token.WS,
            Token.TEXT,     # hours
            Token.TEXT,    # ,
            Token.WS,
            Token.TEXT,     # there
            Token.WS,
            Token.TEXT,     # is
            Token.WS,
            Token.TEXT,     # a
            Token.WS,
            Token.TEXT,     # sign
            Token.TEXT,      # :
            Token.WS,
            Token.squote,      # '...'
            Token.TEXT,      # .
        ]
        self.assert_tree(value, expected, Token.sentence, level=2)

    def test_eos_in_dquote(self):

        value = '''This is a sentence, where the end-of-sentence marker (".") is inside a "double quote."'''

        expected = [
            Token.paragraph,
        ]
        self.assert_tree(value, expected)

        expected = [
            Token.sentence,
        ]
        self.assert_tree(value, expected, Token.paragraph, level=1)

        expected = [
            Token.TEXT,    # This
            Token.WS,
            Token.TEXT,    # is
            Token.WS,
            Token.TEXT,    # a
            Token.WS,
            Token.TEXT,    # sentence
            Token.TEXT,
            Token.WS,
            Token.TEXT,    # where
            Token.WS,
            Token.TEXT,    # the
            Token.WS,
            Token.TEXT,    # end-of-sentence
            Token.WS,
            Token.TEXT,    # marker
            Token.WS,
            Token.paren,    # (".")
            Token.WS,
            Token.TEXT,    # is
            Token.WS,
            Token.TEXT,    # inside
            Token.WS,
            Token.TEXT,    # a
            Token.WS,
            Token.dquote,   # "double quote."
        ]
        self.assert_tree(value, expected, Token.sentence, level=2)

    def test_sentence_in_proc_item(self):

        value = '''
1. This is the first work step.
2. This is the second work step (with an error: no EOS)
3. This is the last work step. Here are two sentences.

'''

        expected = [
            Token.proc_item,
            Token.proc_item,
            Token.proc_item,
        ]
        self.assert_tree(value, expected)

        expected = [
            Token.PROC_STEP,
            Token.PROC_DELIMITER,
            Token.sentence,
        ]
        self.assert_tree(value, expected, Token.proc_item, level=1)

    def test_ireb_template(self):

        value = '''When the system recognizes an applicable debit card, 
the system must show this message in less than 0.2 second:
"Type in the PIN."

'''

        expected = [
            Token.paragraph,
        ]
        self.assert_tree(value, expected)

        expected = [
            Token.sentence,
        ]
        self.assert_tree(value, expected, Token.paragraph, level=1)

        expected = [
            Token.TEXT,     # When
            Token.WS,
            Token.TEXT,     # the
            Token.WS,
            Token.TEXT,     # system
            Token.WS,
            Token.TEXT,     # recognizes
            Token.WS,
            Token.TEXT,     # an
            Token.WS,
            Token.TEXT,     # applicable
            Token.WS,
            Token.TEXT,     # debit
            Token.WS,
            Token.TEXT,     # card
            Token.TEXT,     # ,
            Token.WS,
            Token.LINEBREAK,
            Token.TEXT,     # the
            Token.WS,
            Token.TEXT,     # system
            Token.WS,
            Token.TEXT,     # must
            Token.WS,
            Token.TEXT,     # show
            Token.WS,
            Token.TEXT,     # this
            Token.WS,
            Token.TEXT,     # message
            Token.WS,
            Token.TEXT,     # in
            Token.WS,
            Token.TEXT,     # less
            Token.WS,
            Token.TEXT,     # than
            Token.WS,
            Token.TEXT,     # 0.2
            Token.WS,
            Token.TEXT,     # second
            Token.TEXT,     # .
            Token.dquote,   # " ... "
        ]
        self.assert_tree(value, expected, Token.sentence, level=2)

    def test_sentence_in_list_item(self):

        value = self.load_test_data(TestData.TEST_SENTENCE_IN_LIST_ITEM)

        expected = [
            Token.paragraph,
        ]
        self.assert_tree(value, expected)

        expected = [
            Token.sentence,
            Token.list_item,
            Token.list_item,
            Token.list_item,
            Token.sentence,
        ]
        self.assert_tree(value, expected, Token.paragraph, level=1)

        expected = [
            Token.TEXT,     # List
            Token.WS,
            Token.TEXT,     # item
            Token.TEXT,      # :
        ]
        self.assert_tree(value, expected, Token.sentence, level=2)

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
