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

"""test_bold_emph"""

import unittest

from biz.dfch.ste100parser import GrammarType, Parser, Token, TokenMetrics
from biz.dfch.ste100parser.transformer import ContainerTransformer


class TestBoldEmph(unittest.TestCase):
    """TestBoldEmph"""

    def test(self):

        value = "*_bold-emph text_* at the start"
        initial = Parser(GrammarType.CONTAINER).invoke(value)

        metrics = TokenMetrics()
        transformed = ContainerTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(11, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.paragraph])
        self.assertEqual(5, metrics[Token.TEXT])
        self.assertEqual(4, metrics[Token.WS])
        self.assertEqual(1, metrics[Token.bold_emph])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.paragraph, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.bold_emph, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_multi_line_fails(self):

        value = "*_some_code\nmore code_* "
        result = Parser(GrammarType.CONTAINER).is_valid(value)

        self.assertFalse(result)

    def test_single_open_fails(self):
        value = "*_"
        result = Parser(GrammarType.CONTAINER).is_valid(value)

        self.assertFalse(result)

    def test_single_close_fails(self):
        value = "_*"
        result = Parser(GrammarType.CONTAINER).is_valid(value)

        self.assertFalse(result)

    def test_empty_fails(self):
        value = "*__*"
        result = Parser(GrammarType.CONTAINER).is_valid(value)

        self.assertFalse(result)

    def test_in_dquote(self):
        value = '"*__*"'
        initial = Parser(GrammarType.CONTAINER).invoke(value)

        metrics = TokenMetrics()
        transformed = ContainerTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(6, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.paragraph])
        self.assertEqual(1, metrics[Token.dquote])
        self.assertEqual(4, metrics[Token.CHAR])

    def test_in_squote(self):
        value = "'*__*'"
        initial = Parser(GrammarType.CONTAINER).invoke(value)

        metrics = TokenMetrics()
        transformed = ContainerTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(6, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.paragraph])
        self.assertEqual(1, metrics[Token.squote])
        self.assertEqual(4, metrics[Token.CHAR])
