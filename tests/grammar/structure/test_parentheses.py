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

"""test_parentheses"""

import unittest

from parameterized import parameterized

from biz.dfch.ste100parser import GrammarType, Parser, Token, TokenMetrics
from biz.dfch.ste100parser.transformer import StructureTransformer


class TestParentheses(unittest.TestCase):
    """TestParentheses"""

    def test_standalone(self):

        value = "(some-text-in-parentheses)"
        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(3, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.paragraph])
        self.assertEqual(1, metrics[Token.paren])
        self.assertEqual(1, metrics[Token.TEXT])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.paragraph, metrics.pop())
        self.assertEqual(Token.paren, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_multiline(self):

        value = "(some-multiline-text\nin-parentheses)"
        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(5, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.paragraph])
        self.assertEqual(1, metrics[Token.paren])
        self.assertEqual(2, metrics[Token.TEXT])
        self.assertEqual(1, metrics[Token.NEWLINE])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.paragraph, metrics.pop())
        self.assertEqual(Token.paren, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_pair_start(self):

        value = "(some-text-in-parentheses)"
        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(3, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.TEXT])
        self.assertEqual(1, metrics[Token.paren])
        self.assertEqual(1, metrics[Token.paragraph])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.paragraph, metrics.pop())
        self.assertEqual(Token.paren, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_nested(self):

        value = "(some-text-in-parentheses (round-brackets))"
        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(6, len(metrics), metrics)
        self.assertEqual(2, metrics[Token.TEXT])
        self.assertEqual(1, metrics[Token.WS])
        self.assertEqual(2, metrics[Token.paren])
        self.assertEqual(1, metrics[Token.paragraph])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.paragraph, metrics.pop())
        self.assertEqual(Token.paren, metrics.pop())
        self.assertEqual(Token.paren, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_dquote_in_paren1(self):

        value = """(some-text-in-parentheses "round-brackets")"""
        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(6, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.paragraph])
        self.assertEqual(1, metrics[Token.paren])
        self.assertEqual(1, metrics[Token.dquote])
        self.assertEqual(2, metrics[Token.TEXT])
        self.assertEqual(1, metrics[Token.WS])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.paragraph, metrics.pop())
        self.assertEqual(Token.paren, metrics.pop())
        self.assertEqual(Token.dquote, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_dquote_in_paren2(self):

        value = """(some-text-in-parentheses "(round-brackets)")"""
        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(7, len(metrics), metrics)
        self.assertEqual(2, metrics[Token.TEXT])
        self.assertEqual(1, metrics[Token.WS])
        self.assertEqual(2, metrics[Token.paren])
        self.assertEqual(1, metrics[Token.paragraph])
        self.assertEqual(1, metrics[Token.dquote])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.paragraph, metrics.pop())
        self.assertEqual(Token.paren, metrics.pop())
        self.assertEqual(Token.dquote, metrics.pop())
        self.assertEqual(Token.paren, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    @parameterized.expand([
        ("dquote", '''"(round\nbrackets)"''', False),
        ("dquote", '''"(round\r\nbrackets)"''', False),
        ("squote", """'(round\nbrackets)'""", False),
        ("squote", """'(round\r\nbrackets)'""", False),
    ])
    def test_newline_in_paren_in_quote(self, rule, value, expected):  # NOSONAR(54144)

        result = Parser(GrammarType.STRUCTURE).is_valid(value)
        self.assertEqual(expected, result, rule)

    def test_empty(self):
        value = "()"
        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(2, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.paragraph])
        self.assertEqual(1, metrics[Token.paren])

    def test_empty_in_dquote(self):
        value = '"()"'
        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(3, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.paragraph])
        self.assertEqual(1, metrics[Token.paren])
        self.assertEqual(1, metrics[Token.dquote])

    def test_paren_open_fails(self):
        value = ")"
        result = Parser(GrammarType.STRUCTURE).is_valid(value)

        self.assertFalse(result)

    def test_paren_close_fails(self):
        value = ")"
        result = Parser(GrammarType.STRUCTURE).is_valid(value)

        self.assertFalse(result)

    def test_open_in_dquote(self):
        value = '"("'
        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(3, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.dquote])
        self.assertEqual(1, metrics[Token.paragraph])
        self.assertEqual(1, metrics[Token.CHAR])

    def test_close_in_dquote(self):
        value = '")"'
        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(3, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.dquote])
        self.assertEqual(1, metrics[Token.paragraph])
        self.assertEqual(1, metrics[Token.CHAR])
