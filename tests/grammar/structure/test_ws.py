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

"""test_ws"""

import unittest

from parameterized import parameterized

from biz.dfch.ste100parser import GrammarType, Parser, Token, TokenMetrics
from biz.dfch.ste100parser.transformer import StructureTransformer


class TestWs(unittest.TestCase):
    """TestWs"""

    @parameterized.expand([
        ("single", ' text', True),
        ("double", '  text', True),
        ("triple", '   text', True),
        ("tab_single", '\ttext', True),
        ("tab_double", '\t\ttext', True),
        ("tab_triple", '\t\t\ttext', True),
        ("mixed", '\t \t text', True),
    ])
    def test_ws_single_token(self, rule, value, expected):

        _ = rule
        _ = expected

        initial = Parser(GrammarType.STRUCTURE).invoke(value)
        print(initial.pretty)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(3, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(1, metrics[Token.WS])
        self.assertEqual(1, metrics[Token.TEXT])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    @parameterized.expand([
        ("tab", '\t.', True),
        ("single", ' .', True),
    ])
    def test_ws_start(self, rule, value, expected):

        _ = rule
        _ = expected

        initial = Parser(GrammarType.STRUCTURE).invoke(value)
        print(initial.pretty())

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(3, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(1, metrics[Token.WS])
        self.assertEqual(1, metrics[Token.TEXT])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    @parameterized.expand([
        ("single", '. ', True),
        ("tab", '.\t', True),
    ])
    def test_ws_end(self, rule, value, expected):

        _ = rule
        _ = expected

        initial = Parser(GrammarType.STRUCTURE).invoke(value)
        print(initial.pretty())

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(3, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(1, metrics[Token.WS])
        self.assertEqual(1, metrics[Token.TEXT])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)
