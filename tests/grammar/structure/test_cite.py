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

    def test_cite(self):
        """Cite after a line break is valid."""

        value = "\r\n> cite-text more-text\nend-text"
        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(7, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(3, metrics[Token.TEXT])
        self.assertEqual(1, metrics[Token.NEWLINE])
        self.assertEqual(1, metrics[Token.cite])
        self.assertEqual(1, metrics[Token.WS])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())

        self.assertEqual(Token.cite, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_cite_sof(self):
        """Cite at the start of the input (without a line break at the start) is valid."""

        value = "> cite-text more-text\nend-text"
        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(7, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(3, metrics[Token.TEXT])
        self.assertEqual(1, metrics[Token.NEWLINE])
        self.assertEqual(1, metrics[Token.cite])
        self.assertEqual(1, metrics[Token.WS])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())

        self.assertEqual(Token.cite, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_single(self):

        value = "\r\n> cite-text *bold-text*\nend-text"
        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(8, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(1, metrics[Token.cite])
        self.assertEqual(1, metrics[Token.bold])
        self.assertEqual(1, metrics[Token.NEWLINE])
        self.assertEqual(3, metrics[Token.TEXT])
        self.assertEqual(1, metrics[Token.WS])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())

        self.assertEqual(Token.cite, metrics.pop())
        self.assertEqual(Token.bold, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_empty(self):
        """An 'empty' cite line must contain a minimum of one WS."""

        value = ">  \n>  \n"
        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(6, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(2, metrics[Token.cite])
        self.assertEqual(1, metrics[Token.NEWLINE])
        self.assertEqual(2, metrics[Token.WS])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())

        self.assertEqual(Token.cite, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.cite, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_multi(self):

        # value = "\r\n> block-quote-text1 *more-text*\n> block-quote-text1 *more-text*\nend-text"
        value = "\r\n> first-text *some-text*\n> next-text 'more-text'\nend-text"
        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(13, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        # self.assertEqual(2, metrics[Token.cite])
        self.assertEqual(1, metrics[Token.bold])
        self.assertEqual(1, metrics[Token.squote])
        self.assertEqual(1, metrics[Token.NEWLINE])
        self.assertEqual(5, metrics[Token.TEXT])
        self.assertEqual(2, metrics[Token.WS])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())

        # # First block.
        self.assertEqual(Token.cite, metrics.pop())
        self.assertEqual(Token.squote, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        # # Second block.
        self.assertEqual(Token.cite, metrics.pop())
        self.assertEqual(Token.bold, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)
