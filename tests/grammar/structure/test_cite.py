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

"""test_cite"""

import unittest

from biz.dfch.ste100parser import GrammarType, Parser, Token, TokenMetrics
from biz.dfch.ste100parser.transformer import StructureTransformer


class TestCite(unittest.TestCase):
    """TestCite"""

    def test_single(self):

        value = "\r\n> block-quote-text *more-text*\nnormal-text"
        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(9, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(1, metrics[Token.cite])
        self.assertEqual(1, metrics[Token.bold])
        self.assertEqual(2, metrics[Token.NEWLINE])
        self.assertEqual(3, metrics[Token.TEXT])
        self.assertEqual(1, metrics[Token.WS])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.cite, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())
        self.assertEqual(Token.bold, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_double(self):

        value = "\r\n> block-quote-text1 *more-text*\n\n> block-quote-text1 *more-text*\nnormal-text"
        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(16, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(2, metrics[Token.cite])
        self.assertEqual(2, metrics[Token.bold])
        self.assertEqual(4, metrics[Token.NEWLINE])
        self.assertEqual(5, metrics[Token.TEXT])
        self.assertEqual(2, metrics[Token.WS])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        # # First block.
        self.assertEqual(Token.cite, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())
        self.assertEqual(Token.bold, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())

        # # Second block.
        self.assertEqual(Token.cite, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())
        self.assertEqual(Token.bold, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)
