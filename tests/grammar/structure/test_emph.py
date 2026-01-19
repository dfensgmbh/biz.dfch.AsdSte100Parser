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

"""test_emph"""

import unittest

from biz.dfch.ste100parser import GrammarType, Parser, Token, TokenMetrics
from biz.dfch.ste100parser.transformer import StructureTransformer


class TestEmph(unittest.TestCase):
    """TestEmph"""

    def test_single(self):

        value = "_some-emph_ at-the-start."
        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(5, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.paragraph])
        self.assertEqual(1, metrics[Token.emph])
        self.assertEqual(2, metrics[Token.TEXT])
        self.assertEqual(1, metrics[Token.WS])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.paragraph, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.emph, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_double(self):

        value = "_some-emph_ _more-emph_"
        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(6, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.paragraph])
        self.assertEqual(2, metrics[Token.emph])
        self.assertEqual(1, metrics[Token.WS])
        self.assertEqual(2, metrics[Token.TEXT])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.paragraph, metrics.pop())
        self.assertEqual(Token.emph, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.emph, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_multi_line_fails(self):

        value = "_some-emph\nmore-emph_ "
        result = Parser(GrammarType.STRUCTURE).is_valid(value)

        self.assertFalse(result)

    def test_single_fails(self):
        value = "_"
        result = Parser(GrammarType.STRUCTURE).is_valid(value)

        self.assertFalse(result)

    def test_in_dquote(self):
        value = '"_"'
        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(3, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.paragraph])
        self.assertEqual(1, metrics[Token.dquote])
        self.assertEqual(1, metrics[Token.CHAR])

    def test_in_squote(self):
        value = "'_'"
        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(3, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.paragraph])
        self.assertEqual(1, metrics[Token.squote])
        self.assertEqual(1, metrics[Token.CHAR])
