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

"""test_apostrophe"""

import unittest

from biz.dfch.ste100parser import GrammarType, Parser, Token, TokenMetrics
from biz.dfch.ste100parser.transformer import StructureTransformer


class TestApostrophe(unittest.TestCase):
    """TestApostrophe"""

    def test_apostrophe_singular(self):

        value = """Peter's cat."""

        initial = Parser(GrammarType.STRUCTURE).invoke(value)
        print(initial.pretty())

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(5, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(1, metrics[Token.APOSTROPHE])
        self.assertEqual(1, metrics[Token.WS])
        self.assertEqual(2, metrics[Token.TEXT])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.APOSTROPHE, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_apostrophe_inside_squote(self):

        value = """'Peter's cat.' in squote."""

        initial = Parser(GrammarType.STRUCTURE).invoke(value)
        print(initial.pretty())

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(10, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(4, metrics[Token.TEXT])
        self.assertEqual(3, metrics[Token.WS])
        self.assertEqual(1, metrics[Token.squote])
        self.assertEqual(1, metrics[Token.APOSTROPHE])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.squote, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.APOSTROPHE, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_apostrophe_inside_dquote(self):

        value = """"Peter's cat." in squote."""

        initial = Parser(GrammarType.STRUCTURE).invoke(value)
        print(initial.pretty())

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(10, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(4, metrics[Token.TEXT])
        self.assertEqual(3, metrics[Token.WS])
        self.assertEqual(1, metrics[Token.dquote])
        self.assertEqual(1, metrics[Token.APOSTROPHE])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.dquote, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.APOSTROPHE, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_apostrophe_plural(self):

        value = """Manufacturers' regulations."""

        initial = Parser(GrammarType.STRUCTURE).invoke(value)
        print(initial.pretty())

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(5, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(2, metrics[Token.TEXT])
        self.assertEqual(1, metrics[Token.WS])
        self.assertEqual(1, metrics[Token.APOSTROPHE])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.APOSTROPHE, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_apostrophe_plural_in_squote(self):

        value = """'Manufacturers' regulations' in squote."""

        initial = Parser(GrammarType.STRUCTURE).invoke(value)
        print(initial.pretty())

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(10, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(4, metrics[Token.TEXT])
        self.assertEqual(1, metrics[Token.squote])
        self.assertEqual(3, metrics[Token.WS])
        self.assertEqual(1, metrics[Token.APOSTROPHE])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.squote, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.APOSTROPHE, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_apostrophe_plural_in_dquote(self):

        value = """"Manufacturers' regulations" in squote."""

        initial = Parser(GrammarType.STRUCTURE).invoke(value)
        print(initial.pretty())

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(10, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(4, metrics[Token.TEXT])
        self.assertEqual(1, metrics[Token.dquote])
        self.assertEqual(3, metrics[Token.WS])
        self.assertEqual(1, metrics[Token.APOSTROPHE])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.dquote, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.APOSTROPHE, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)
