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
# pylint: disable=C0301
# type: ignore

"""test_quote"""

import unittest

from parameterized import parameterized

from biz.dfch.ste100parser import GrammarType, Parser, Token, TokenMetrics
from biz.dfch.ste100parser.transformer import StructureTransformer


class TestQuote(unittest.TestCase):
    """TestQuote"""

    def test(self):
        value = "# This-is-a-heading-level-1"
        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(3, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.heading])
        self.assertEqual(1, metrics[Token.HEADING_LEVEL])
        self.assertEqual(1, metrics[Token.TEXT])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.heading, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.HEADING_LEVEL, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_multi(self):
        value = "# This-is-a-heading-level-1\n\n## This-is-a-heading-level-2\n\nThis-is-normal-text."
        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(12, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(2, metrics[Token.heading])
        self.assertEqual(2, metrics[Token.HEADING_LEVEL])
        self.assertEqual(3, metrics[Token.TEXT])
        self.assertEqual(4, metrics[Token.NEWLINE])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(Token.NEWLINE, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())

        self.assertEqual(Token.heading, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.HEADING_LEVEL, metrics.pop())

        self.assertEqual(Token.NEWLINE, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())

        self.assertEqual(Token.heading, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.HEADING_LEVEL, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    @parameterized.expand([
        ("heading_level_1", "# This-is-a-heading-level-1", 1),
        ("heading_level_2", "## This-is-a-heading-level-2", 2),
        ("heading_level_3", "### This-is-a-heading-level-3", 3),
        ("heading_level_4", "#### This-is-a-heading-level-4", 4),
        ("heading_level_5", "#### This-is-a-heading-level-5", 5),
    ])
    def test_single_char(self, rule, value, expected):

        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        _ = rule
        _ = expected

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(3, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.heading])
        self.assertEqual(1, metrics[Token.HEADING_LEVEL])
        self.assertEqual(1, metrics[Token.TEXT])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.heading, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.HEADING_LEVEL, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)
