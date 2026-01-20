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

"""test_paragraph"""

import unittest

from biz.dfch.ste100parser import GrammarType, Parser, Token, TokenMetrics
from biz.dfch.ste100parser.transformer import StructureTransformer


class TestParagraph(unittest.TestCase):
    """TestParagraph"""

    def test_leading_ws_fails(self):
        value = " leading-space-is-not-valid"

        result = Parser(GrammarType.STRUCTURE).is_valid(value)
        self.assertFalse(result)

    def test_leading_newline_is_not_part_of_para(self):
        value = "\narbitrary-text-that-is-part-of-the-paragraph."

        initial = Parser(GrammarType.STRUCTURE).invoke(value)
        print(initial.pretty())

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(4, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(1, metrics[Token.NEWLINE])
        self.assertEqual(1, metrics[Token.paragraph])
        self.assertEqual(1, metrics[Token.TEXT])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.paragraph, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_newline_is_part_of_para(self):
        value = "arbitrary-text-that-is-part-of-the-paragraph\nmore-paragraph-text."

        initial = Parser(GrammarType.STRUCTURE).invoke(value)
        print(initial.pretty())

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(4, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.paragraph])
        self.assertEqual(1, metrics[Token.LINEBREAK])
        self.assertEqual(2, metrics[Token.TEXT])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.paragraph, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.LINEBREAK, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_double_newline_ends_para(self):
        # value = "text-in-1st-para\n\ntext-in-2nd-para."
        value = "text-in-1st-para\n\ntext-in-2nd-para"

        initial = Parser(GrammarType.STRUCTURE).invoke(value)
        print(initial.pretty())

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(7, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(2, metrics[Token.paragraph])
        self.assertEqual(2, metrics[Token.NEWLINE])
        self.assertEqual(2, metrics[Token.TEXT])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.paragraph, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())
        self.assertEqual(Token.paragraph, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_bold_in_para(self):
        value = "text-in*bold*"

        initial = Parser(GrammarType.STRUCTURE).invoke(value)
        print(initial.pretty())

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(4, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.paragraph])
        self.assertEqual(1, metrics[Token.bold])
        self.assertEqual(2, metrics[Token.TEXT])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.paragraph, metrics.pop())
        self.assertEqual(Token.bold, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_emph_in_para(self):
        value = "text-in_emph_"

        initial = Parser(GrammarType.STRUCTURE).invoke(value)
        print(initial.pretty())

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(4, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.paragraph])
        self.assertEqual(1, metrics[Token.emph])
        self.assertEqual(2, metrics[Token.TEXT])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.paragraph, metrics.pop())
        self.assertEqual(Token.emph, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_bold_emph_in_para(self):
        value = "text-in*_bold-emph_*"

        initial = Parser(GrammarType.STRUCTURE).invoke(value)
        print(initial.pretty())

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(4, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.paragraph])
        self.assertEqual(1, metrics[Token.bold_emph])
        self.assertEqual(2, metrics[Token.TEXT])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.paragraph, metrics.pop())
        self.assertEqual(Token.bold_emph, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_dquote_in_para(self):
        value = 'text-in"dquote"'

        initial = Parser(GrammarType.STRUCTURE).invoke(value)
        print(initial.pretty())

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(4, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.paragraph])
        self.assertEqual(1, metrics[Token.dquote])
        self.assertEqual(2, metrics[Token.TEXT])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.paragraph, metrics.pop())
        self.assertEqual(Token.dquote, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_squote_in_para(self):
        value = "text-in'squote'"

        initial = Parser(GrammarType.STRUCTURE).invoke(value)
        print(initial.pretty())

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(4, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.paragraph])
        self.assertEqual(1, metrics[Token.squote])
        self.assertEqual(2, metrics[Token.TEXT])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.paragraph, metrics.pop())
        self.assertEqual(Token.squote, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_paren_in_para(self):
        value = "text-in(parentheses)"

        initial = Parser(GrammarType.STRUCTURE).invoke(value)
        print(initial.pretty())

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(4, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.paragraph])
        self.assertEqual(1, metrics[Token.paren])
        self.assertEqual(2, metrics[Token.TEXT])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.paragraph, metrics.pop())
        self.assertEqual(Token.paren, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_mul_in_para(self):
        value = " * "

        initial = Parser(GrammarType.STRUCTURE).invoke(value)
        print(initial.pretty())

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(2, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.paragraph])
        self.assertEqual(1, metrics[Token.MULTIPLY])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.paragraph, metrics.pop())
        self.assertEqual(Token.MULTIPLY, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_apostrophe_in_para1(self):
        value = "Peter's."

        initial = Parser(GrammarType.STRUCTURE).invoke(value)
        print(initial.pretty())

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(4, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.paragraph])
        self.assertEqual(1, metrics[Token.APOSTROPHE])
        self.assertEqual(2, metrics[Token.TEXT])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.paragraph, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.APOSTROPHE, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_apostrophe_in_para2(self):
        value = "Manufacturers'."

        initial = Parser(GrammarType.STRUCTURE).invoke(value)
        print(initial.pretty())

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(4, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.paragraph])
        self.assertEqual(1, metrics[Token.APOSTROPHE])
        self.assertEqual(2, metrics[Token.TEXT])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.paragraph, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.APOSTROPHE, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_proc_after_para(self):
        value = "Some-text.\n\n1. proc-item"

        initial = Parser(GrammarType.STRUCTURE).invoke(value)
        print(initial.pretty())

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(7, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(1, metrics[Token.proc_item])
        self.assertEqual(2, metrics[Token.TEXT])
        self.assertEqual(2, metrics[Token.NEWLINE])
        self.assertEqual(1, metrics[Token.paragraph])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.proc_item, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())
        self.assertEqual(Token.paragraph, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)
