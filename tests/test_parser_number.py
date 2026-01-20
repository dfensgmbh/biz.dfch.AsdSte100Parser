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

"""test_parser_number."""

import unittest

from parameterized import parameterized

from biz.dfch.ste100parser import Parser, GrammarType


class TestParserNumber(unittest.TestCase):
    """TestParserNumber"""

    sut: Parser

    def setUp(self):
        self.sut = Parser()

    def test_and_display(self):

        value = "0"
        self.sut = Parser(GrammarType.INT)

        try:
            result = self.sut.invoke(value)
            print(result.pretty())

            result = self.sut.is_valid(value)
            self.assertTrue(result)

        except Exception as ex:  # pylint: disable=W0718
            self.fail(ex)

    @parameterized.expand([
        ("zero", "0", True),
        ("zero", "+0", True),
        ("zero", "-0", True),

        ("valid_positive", "1", True),
        ("valid_positive", "12", True),
        ("valid_positive", "123", True),

        ("valid_plus", "+1", True),
        ("valid_plus", "+12", True),
        ("valid_plus", "+123", True),

        ("valid_negative", "-1", True),
        ("valid_negative", "-12", True),
        ("valid_negative", "-123", True),
    ])
    def test_int(self, rule, value, expected) -> None:

        self.sut = Parser(GrammarType.INT)

        result = self.sut.is_valid(value)
        self.assertEqual(result, expected, rule)

    @parameterized.expand([
        ("multi_dot_fails", "12.34.56", False),
        ("missing_dot_fails", "0", False),
        ("missing_dot_fails", "1", False),
        ("missing_dot_fails", "12", False),
        ("multi_leading_zero", "00.0", True),

        ("zero", "0.0", True),
        ("zero", "0.00", True),
        ("zero", "+0.0", True),
        ("zero", "+0.00", True),
        ("zero", "-0.0", True),
        ("zero", "-0.00", True),

        ("valid_positive", "1.0", True),
        ("valid_positive", "1.00", True),
        ("valid_positive", "12.3", True),
        ("valid_positive", "12.34", True),

        ("valid_plus", "+1.0", True),
        ("valid_plus", "+1.00", True),
        ("valid_plus", "+12.3", True),
        ("valid_plus", "+12.34", True),

        ("valid_negative", "-1.0", True),
        ("valid_negative", "-1.00", True),
        ("valid_negative", "-12.3", True),
        ("valid_negative", "-12.34", True),
    ])
    def test_fp(self, rule, value, expected) -> None:

        self.sut = Parser(GrammarType.FP)

        result = self.sut.is_valid(value)
        self.assertEqual(result, expected, rule)

    @parameterized.expand([
        ("multi_dot_fails", "12.34.56", False),
        ("missing_dot_is_int", "0", True),
        ("missing_dot_is_int", "1", True),
        ("missing_dot_is_int", "12", True),

        ("zero", "0.0", True),
        ("zero", "0.00", True),
        ("zero", "+0.0", True),
        ("zero", "+0.00", True),
        ("zero", "-0.0", True),
        ("zero", "-0.00", True),

        ("valid_positive", "1.0", True),
        ("valid_positive", "1.00", True),
        ("valid_positive", "12.3", True),
        ("valid_positive", "12.34", True),

        ("valid_plus", "+1.0", True),
        ("valid_plus", "+1.00", True),
        ("valid_plus", "+12.3", True),
        ("valid_plus", "+12.34", True),

        ("valid_negative", "-1.0", True),
        ("valid_negative", "-1.00", True),
        ("valid_negative", "-12.3", True),
        ("valid_negative", "-12.34", True),
    ])
    def test_number(self, rule, value, expected) -> None:

        self.sut = Parser(GrammarType.NUMBER)

        result = self.sut.is_valid(value)
        self.assertEqual(result, expected, rule)
