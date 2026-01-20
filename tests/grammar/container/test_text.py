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

"""test_text"""

import unittest

from parameterized import parameterized

from biz.dfch.ste100parser import GrammarType, Parser, Token, TokenMetrics
from biz.dfch.ste100parser.transformer import ContainerTransformer


class TestText(unittest.TestCase):
    """TestText"""

    @parameterized.expand([
        ("lower", "abcdefghijklmopqrstuvwxzy", True),
        ("upper", "ABCDEFGHIJKLMOPQRSTUVWXYZ", True),
        ("digit", "0123456789", True),
        ("umlaut", "äöü", True),
        ("french", r"áàéèëíìïóòúùç", True),
        ("symbols", r"-+=%&/\<>^$£[]{}#@¨´", True),
        ("punctuation", ".,:?!", True),
        ("unicode", "←→↑↓↔↕⇐⇒⇑⇓", True),
        ("guillemets_double", "«", True),
        ("guillemets_double", "»", True),
        ("guillemets_single", "‹", True),
        ("guillemets_single", "›", True),
        ("german_double", "„", True),
        ("german_double", "“", True),
        ("german_single", "‚", True),
        ("german_single", "‘", True),
        ("single_word_with_dash", "single-word", True),

        ("bold", "*", False),
        ("bold_emph", "*_", False),
        ("bold_emph", "_*", False),
        ("emph", "_", False),
        ("code", "`", False),
        ("paren_open", "(", False),
        ("paren_close", ")", False),
    ])
    def test_word(self, rule, value, expected):
        """Allowed characters."""

        _ = rule
        _ = expected

        result = Parser(GrammarType.CONTAINER).is_valid(value)
        if not expected:
            self.assertFalse(result)
            return

        initial = Parser(GrammarType.CONTAINER).invoke(value)

        metrics = TokenMetrics()
        transformed = ContainerTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(2, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.paragraph])
        self.assertEqual(1, metrics[Token.TEXT])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.paragraph, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_single_word_is_paragraph(self):
        """Cite after a line break is valid."""

        value = "this-is-text"
        initial = Parser(GrammarType.CONTAINER).invoke(value)

        metrics = TokenMetrics()
        transformed = ContainerTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(2, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.paragraph])
        self.assertEqual(1, metrics[Token.TEXT])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.paragraph, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_multi_word_is_paragraph(self):
        """Cite after a line break is valid."""

        value = "this-is-text this-is-also-text"
        initial = Parser(GrammarType.CONTAINER).invoke(value)

        metrics = TokenMetrics()
        transformed = ContainerTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(4, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.paragraph])
        self.assertEqual(2, metrics[Token.TEXT])
        self.assertEqual(1, metrics[Token.WS])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.paragraph, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)
