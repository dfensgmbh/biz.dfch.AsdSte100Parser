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

"""test_structure"""

import unittest

from parameterized import parameterized

from biz.dfch.ste100parser import GrammarType, Parser, Token, TokenMetrics
from biz.dfch.ste100parser.transformer import StructureTransformer
from tests.phrase import Phrase


class TestStructure(unittest.TestCase):
    """TestStructure"""

    def test_and_display(self):

        value = """'I *can* _quote_ Peter's *_opening_* `parentheses` "(" and ")".'"""
        sut = Parser(GrammarType.STRUCTURE)

        try:
            result = sut.invoke(value)
            print(result.pretty())

            result = sut.is_valid(value)
            self.assertTrue(result)

        except Exception as ex:  # pylint: disable=W0718
            self.fail(ex)

    def test_squote_mixed(self):

        value = """'This is _an_ *squote*' at the *start* of a text."""

        initial = Parser(GrammarType.STRUCTURE).invoke(value)
        print(initial.pretty())

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(24, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.paragraph])
        self.assertEqual(1, metrics[Token.squote])
        self.assertEqual(2, metrics[Token.bold])
        self.assertEqual(1, metrics[Token.emph])
        self.assertEqual(10, metrics[Token.TEXT])
        self.assertEqual(9, metrics[Token.WS])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.paragraph, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.bold, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.squote, metrics.pop())
        self.assertEqual(Token.bold, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.emph, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_dquote_mixed(self):

        value = """"This is _a_ *dquote*" at the *start* of a text."""

        initial = Parser(GrammarType.STRUCTURE).invoke(value)
        print(initial.pretty())

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(24, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.paragraph])
        self.assertEqual(1, metrics[Token.dquote])
        self.assertEqual(2, metrics[Token.bold])
        self.assertEqual(1, metrics[Token.emph])
        self.assertEqual(10, metrics[Token.TEXT])
        self.assertEqual(9, metrics[Token.WS])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.paragraph, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.bold, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.dquote, metrics.pop())
        self.assertEqual(Token.bold, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.emph, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    @parameterized.expand([
        (Phrase.DQUOTE_DOT.name, Phrase.DQUOTE_DOT.value, True),
        (Phrase.SQUOTE_DOT.name, Phrase.SQUOTE_DOT.value, True),

        ("dquote_end", 'This is "d quoted text".', True),
        ("dquote_start", '"D quoted text" is at the start.', True),
        ("dquote_mid", 'And here "d quoted" text in the middle.', True),

        ("paren_end", 'This is text with parentheses (near the end).', True),
        ("paren_start", '(Unusual) But this can also occur.', True),
        ("paren_mid", 'Not unusual, (when writing) this can happen.', True),

        ("pq_end", 'I can use quoted text in parentheses ("This is quoted text.").', True),
        ("pq_start", '("Quoted text") Sometimes at the start.', True),
        ("pq_mid", 'Quoted text ("in this example") in the middle.', True),

        ("qp_mid_end", 'I can quote opening parentheses "(" and ")".', True),
        ("qp_start_mid", '"(" and ")" at the start.', True),

        ("bold", "This is text in *bold*", True),

        ("squote_with_apostrophe", "This is Edgar's 'single quoted' text.", True),
        ("squote_with_apostrophe", "This is 'single quoted' text from the 1900's.", True),
        ("squote_with_apostrophe",
         "'Single quoted' text from the manufacturers' specification.", True),
        ("dquote_with_apostrophe", '''This is Edgar's "double quoted" text.''', True),

        ("paren_nested", 'Nested parentheses (that is parentheses within (another pair of) parentheses).', True),
        ("paren_nested", 'Nested parentheses (that is parentheses within (another "pair" of) parentheses).', True),
    ])
    def test_container(self, rule, value, expected) -> None:

        sut = Parser(GrammarType.STRUCTURE)
        result = sut.is_valid(value)
        self.assertEqual(result, expected, f"{rule}: {value}")
