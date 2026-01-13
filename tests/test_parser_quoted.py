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

# pylint: disable=C0116
# type: ignore

"""test_parser_quoted"""

from enum import auto, Enum
import unittest

from lark import Transformer
from lark import Tree

from parameterized import parameterized

from biz.dfch.ste100parser import Parser, GrammarType


class WordType(Enum):
    """WordType"""
    DEFAULT = auto()
    CAP = auto()
    LOWER = auto()
    UPPER = auto()
    MULTI = auto()


class MyTransformer(Transformer):
    """MyTransformer"""

    def __init__(self):
        super().__init__()
        self.errors = []

    def WORD(self, children):  # pylint: disable=C0103
        print(f"word #{len(children)}: '{children}'")

        token = str(children)

        return Tree(WordType.MULTI, [token])


class TestParserQuoted(unittest.TestCase):
    """TestParserQuoted"""

    sut: Parser

    def setUp(self):
        self.sut = Parser(GrammarType.CONTAINER)

    def test_and_display(self):

        value = "abc-def-123"
        self.sut = Parser(GrammarType.CONTAINER)

        try:
            result = self.sut.invoke(value)
            print(result.pretty())

            result = self.sut.is_valid(value)
            self.assertTrue(result)

        except Exception as ex:  # pylint: disable=W0718
            self.fail(ex)

    def test_sth(self):
        value = "abc-def-123"
        tree = self.sut.invoke(value)

        transformer = MyTransformer()
        result = transformer.transform(tree)

        print(f"result: {result}")

    @parameterized.expand([
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

        ("paren_nested", 'Nested parentheses (that is parentheses within (another pair of) parentheses).', True),
        ("paren_nested", 'Nested parentheses (that is parentheses within (another "pair" of) parentheses).', True),
    ])
    def test_quoted(self, rule, value, expected) -> None:

        result = self.sut.is_valid(value)
        self.assertEqual(result, expected, f"{rule}: {value}")
