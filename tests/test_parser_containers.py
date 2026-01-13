# Copyright (C) 2026 Ronald Rink, d-fens GmbH
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

# pylint: disable=C0116
# type: ignore

"""test_parser_containers"""

from enum import StrEnum
import unittest

from lark import Transformer
from parameterized import parameterized

from biz.dfch.ste100parser import Parser, GrammarType
from biz.dfch.ste100parser.transformer import ContainersTransformer
from biz.dfch.ste100parser.renderer import ContainersRenderer


class Phrase(StrEnum):
    """Test phrases."""

    DQUOTE = """This is "quoted text"."""
    SQUOTE = """This is 'quoted text'."""


class TransformerBase(Transformer):
    """TransformerBase"""

    def __default__(self, data, children, meta):
        # data = the rule name (e.g., "squote", "bold", "emph")
        # children = the list of children
        # meta = metadata (line/column info)

        print(f"__default__ caught: {data}")


class MyTransformer(TransformerBase):
    """MyTransformer"""

    def dquote(self, children):
        print(f"#{len(children)}")
        for i, child in enumerate(children):
            print(f"#{i}: '{child}' [{type(child)}]")


class TestParserContainers(unittest.TestCase):
    """TestParserContainers"""

    sut: Parser

    def setUp(self):
        self.sut = Parser(GrammarType.CONTAINERS)

    def test_and_display(self):

        value = """'I *can* _quote_ *_opening_* `parentheses` "(" and ")".'"""
        self.sut = Parser(GrammarType.CONTAINERS)

        try:
            result = self.sut.invoke(value)
            print(result.pretty())

            result = self.sut.is_valid(value)
            self.assertTrue(result)

        except Exception as ex:  # pylint: disable=W0718
            self.fail(ex)

    def test_dquote_start(self):

        value = '''"This, is a-dquote" at the start of a text.'''
        self.sut = Parser(GrammarType.CONTAINERS)

        try:
            tree0 = self.sut.invoke(value)
            print(tree0.pretty())

            tree1 = ContainersTransformer().transform(tree0)
            print(tree1.pretty())

            tree2 = ContainersRenderer().transform(tree1)
            print(tree2.pretty())

            result = ''.join(tree2.children)
            self.assertEqual(value, result)

            tree0 = self.sut.is_valid(value)
            self.assertTrue(tree0)

        except Exception as ex:  # pylint: disable=W0718
            self.fail(ex)

    def test_dquote_start2(self):

        value = '''"This is a dquote" at the start of a text.'''
        self.sut = Parser(GrammarType.CONTAINERS)

        try:
            result = self.sut.invoke(value)
            print(result.pretty())

            MyTransformer().transform(result)

            result = self.sut.is_valid(value)
            self.assertTrue(result)

        except Exception as ex:  # pylint: disable=W0718
            self.fail(ex)

    @parameterized.expand([
        (Phrase.DQUOTE.name, Phrase.DQUOTE.value, True),
        (Phrase.SQUOTE.name, Phrase.SQUOTE.value, True),

        ("quote_end", 'This is "quoted text".', True),
        ("quote_start", '"Quoted text" is at the start.', True),
        ("quote_mid", 'And here "quoted" text in the middle.', True),

        ("paren_end", 'This is text with parentheses (near the end).', True),
        ("paren_start", '(Unusual) But this can also occur.', True),
        ("paren_mid", 'Not unusual, (when writing) this can happen.', True),

        ("pq_end", 'I can use quoted text in parentheses ("This is quoted text.").', True),
        ("pq_start", '("Quoted text") Sometimes at the start.', True),
        ("pq_mid", 'Quoted text ("in this example") in the middle.', True),

        ("qp_mid_end", 'I can quote opening parentheses "(" and ")".', True),
        ("qp_start_mid", '"(" and ")" at the start.', True),

        ("bold", "This is text in *bold*", True),

        ("paren_nested", 'Nested parentheses (that is parentheses within (another pair of) parentheses).', True),
        ("paren_nested", 'Nested parentheses (that is parentheses within (another "pair" of) parentheses).', True),
    ])
    def test_container(self, rule, value, expected) -> None:

        result = self.sut.is_valid(value)
        self.assertEqual(result, expected, f"{rule}: {value}")
