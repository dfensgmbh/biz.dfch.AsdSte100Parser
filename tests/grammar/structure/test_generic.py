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

"""test_generic"""

import unittest

from parameterized import parameterized

from biz.dfch.ste100parser import Char, GrammarType, Parser, Token, TokenMetrics
from biz.dfch.ste100parser.transformer import StructureTransformer


class TestGeneric(unittest.TestCase):
    """TestGeneric"""

    def test_inspect(self):

        value = "`_first`: 4 * 3\nNext-line-ddf\r\n\nFourth-line"
        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(12, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(1, metrics[Token.MULTIPLY])
        self.assertEqual(1, metrics[Token.CODE])
        self.assertEqual(5, metrics[Token.TEXT])
        self.assertEqual(3, metrics[Token.NEWLINE])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.MULTIPLY, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.CODE, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_newline(self):

        value = "first-line\r\n\nthird-line"
        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(5, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(2, metrics[Token.TEXT])
        self.assertEqual(2, metrics[Token.NEWLINE])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    @parameterized.expand([
        ("empty", Char.EMPTY, False),
        ("space", Char.SPACE, False),
        ("tab", Char.TAB, False),

        ("char_lower", 'a', True),
        ("char_upper", 'A', True),
        ("chars_lower", 'abc', True),
        ("chars_upper", 'ABC', True),
        ("chars_mixed", 'Abc', True),
        ("alpha_numeric1", 'abcABC123', True),
        ("alpha_numeric2", 'ABCabc123', True),
        ("alpha_numeric3", '123ABCabc', True),

        ("dot", Char.DOT, True),
        ("comma", Char.COMMA, True),
        ("colon", Char.COLON, True),
        ("question", Char.QUESTION, True),
        ("exclamation", Char.EXCLAMATION, True),

        ("alpha_num_ends_with_dot", "1TextThatEndsWithDot.", True),
        ("alpha_num_ends_with_comma", "1TextThatEndsWithComma,", True),
        ("alpha_num_ends_with_colon", "1TextThatEndsWithColon:", True),
        ("alpha_num_ends_with_question", "1TextThatEndsWithQuestion?", True),
        ("alpha_num_ends_with_exclamation", "1TextThatEndsWithExcl!", True),
    ])
    def test_text0(self, rule, value, expected):

        sut = Parser(GrammarType.STRUCTURE)

        if expected is False:
            self.assertFalse(sut.is_valid(value), rule)
            return

        initial = sut.invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(1, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.TEXT])

    @parameterized.expand([
        ("text_space", "text ", True),
        ("space_text", " text", True),
    ])
    def test_text1(self, rule, value, expected):

        _ = rule
        _ = expected

        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(3, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(1, metrics[Token.TEXT])
        self.assertEqual(1, metrics[Token.WS])

    @parameterized.expand([
        ("text_space", "text1 text2 ", True),
        ("space_text", " text1 text2", True),
    ])
    def test_text2(self, rule, value, expected):

        _ = rule
        _ = expected

        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(5, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(2, metrics[Token.TEXT])
        self.assertEqual(2, metrics[Token.WS])
