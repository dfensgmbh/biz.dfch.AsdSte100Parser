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

"""TestParser"""

import unittest
from parameterized import parameterized

from biz.dfch.ste100parser import Parser, GrammarType


class TestParser(unittest.TestCase):
    """TestParser"""

    sut: Parser

    def setUp(self):
        self.sut = Parser()

    def test_and_display(self):

        value = "00.00"
        self.sut = Parser(GrammarType.NUMBER)

        try:
            result = self.sut.invoke(value)
            print(result.pretty())

            result = not self.sut.is_valid(value)
            self.assertTrue(result)

        except Exception as ex:  # pylint: disable=W0718
            self.fail(ex)

    def test_single_word_ending_with_dot(self):

        value = "Hello."
        result = self.sut.is_valid(value)
        self.assertTrue(result)

    def test_single_word_fails(self):
        """The sentence must end with an EOS."""

        value = "Hello"

        result = self.sut.is_valid(value)

        self.assertFalse(result)

    def test_two_words(self):

        value = "Hello world."

        result = self.sut.is_valid(value)

        self.assertTrue(result)

    def test_two_words_with_comma(self):

        value = "Hello, world."

        result = self.sut.is_valid(value)

        self.assertTrue(result)

    def test_two_words_with_comma_missing_space_fails(self):

        value = "Hello,world."

        result = self.sut.is_valid(value)

        self.assertFalse(result)

    def test_sth(self):

        value = "Hello, world. " \
            "This is a test sentence. " \
            "I use the number 8.15."

        result = self.sut.is_valid(value)

        self.assertTrue(result)

    @parameterized.expand([
        ("valid_case", "Hello, world. 8.15.", True),
        ("missing_eos", "Hello", False),
        ("missing_space", "Hello,world.", False),
        ("double_space", "Hello  world.", False),
        ("valid_case", "Hello, world.", True),
        ("valid_case", "Hello, world!", True),
        ("valid_case", "Hello, world?", True),
        ("valid_case", "Hello, world:", True),
        ("multiple_comma", "Hello, world, last word.", True),
        ("valid_case", "No numbers here.", True),
        ("short_case", "8.15", False),
        ("valid_case", "8.15.", True),
    ])
    def test_is_valid(self, rule, value, expected):  # NOSONAR(54144)

        result = self.sut.is_valid(value)

        self.assertEqual(result, expected, rule)
