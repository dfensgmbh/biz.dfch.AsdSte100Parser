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

"""test_quote"""

import unittest

from parameterized import parameterized

from biz.dfch.ste100parser import GrammarType, Parser, Token, TokenMetrics
from biz.dfch.ste100parser.transformer import StructureTransformer


class TestQuote(unittest.TestCase):
    """TestQuote"""

    @parameterized.expand([
        ("paren_open_in_squote", "'('", Token.squote),
        ("paren_close_in_squote", "')'", Token.squote),
        ("star_in_squote", "'*'", Token.squote),
        ("under_in_squote", "'_'", Token.squote),
        ("back_tick_in_squote", "'`'", Token.squote),

        ("paren_open_in_dquote", '"("', Token.dquote),
        ("paren_close_in_dquote", '")"', Token.dquote),
        ("star_in_dquote", '"*"', Token.dquote),
        ("under_in_dquote", '"_"', Token.dquote),
        ("back_tick_in_dquote", '"`"', Token.dquote),
    ])
    def test_single_char(self, rule, value, expected):

        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        _ = rule
        _ = expected

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(2, len(metrics), metrics)
        self.assertEqual(1, metrics[expected])
        self.assertEqual(1, metrics[Token.CHAR])

        # Assert order of tokens (recursively).
        self.assertEqual(expected, metrics.pop())
        self.assertEqual(Token.CHAR, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)
