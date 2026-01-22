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

"""test_parser_word"""

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

    def WORD(self, children):
        print(f"word #{len(children)}: '{children}'")

        token = str(children)

        return Tree(WordType.MULTI, [token])


class TestParserWord(unittest.TestCase):
    """TestParserWord"""

    sut: Parser

    def setUp(self):
        self.sut = Parser(GrammarType.WORD)

    def test_and_display(self):

        value = "abc-def-123"
        self.sut = Parser(GrammarType.WORD)

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
        ("empty", "", False),

        ("single_char_lower", "a", True),
        ("single_char_lower", "b", True),

        ("lower", "ab", True),
        ("lower", "abc", True),

        ("single_char_upper", "A", True),
        ("single_char_upper", "B", True),

        ("upper", "AB", True),
        ("upper", "ABC", True),

        ("digit", "1", True),
        ("digit", "12", True),
        ("digit", "123", True),
        ("digit", "12a", True),
        ("digit", "12B", True),

        ("alpha", "1abc", True),
        ("alpha", "a1bc", True),
        ("alpha", "a1b2c", True),
        ("alpha", "a1b2c3", True),

        ("cap", "Abc", True),

        ("multi", "Abc-Def", True),
        ("multi", "Abc-Def-Ghi", True),
        ("multi", "1bc-D2f-G3i", True),
        ("multi", "1bc-d2f-g3i", True),
        ("multi", "123-456-789", True),

        ("single-hyphen", "-", False),
        ("leading-hyphen", "-Abc", False),
        ("leading-hyphen", "-abc", False),
        ("trailing-hyphen", "Abc-", False),
        ("trailing-hyphen", "abc-", False),
        ("too-many-hyphen", "Abc-Def-Ghi-Jkl", False),
        ("too-many-hyphen", "abc-def-ghi-jkl", False),
        ("consecutive-hyphen", "Abc--Def", False),
        ("consecutive-hyphen", "abc--def", False),
        ("consecutive-hyphen", "123--456", False),
    ])
    def test_word(self, rule, value, expected) -> None:

        result = self.sut.is_valid(value)
        self.assertEqual(result, expected, f"{rule}: {value}")
