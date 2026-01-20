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

"""test_list"""

import unittest

from parameterized import parameterized

from biz.dfch.ste100parser import GrammarType, Parser, Token, TokenMetrics
from biz.dfch.ste100parser.transformer import ContainerTransformer


class TestList(unittest.TestCase):
    """TestList"""

    @parameterized.expand([
        ("bullet", "Para-start:\n* First\n* Second\n* Last.\nPara-end.", True),
        ("bullet_with_bold", "Para-start:\n* *First*\n* Second\n* Last.\nPara-end.", True),
        ("dash", "Para-start:\n- First\n- Second\n- Last.\nPara-end.", True),
        ("number", "Para-start:\n1 First\n2 Second\n3 Last.\nPara-end.", True),
        ("lower", "Para-start:\na First\nb Second\nc Last.\nPara-end.", True),
        ("upper", "Para-start:\nA First\nB Second\nC Last.\nPara-end.", True),
        ("mixed", "Para-start:\n1A First\n1B Second\n1C Last.\nPara-end.", True),
        ("mixed", "Para-start:\n1a First\n1c Second\n1c Last.\nPara-end.", True),
    ])
    def test(self, rule, value, expected):
        _ = rule
        _ = expected

        initial = Parser(GrammarType.CONTAINER).invoke(value)

        metrics = TokenMetrics()
        transformed = ContainerTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

    def test_list_in_paragraph(self):

        value = "This-is-text:\nAA First-line second-item\n* Second-line fourth-item\nMore-paragraph-text."
        initial = Parser(GrammarType.CONTAINER).invoke(value)

        metrics = TokenMetrics()
        transformed = ContainerTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(12, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.paragraph])
        self.assertEqual(1, metrics[Token.LINEBREAK])
        self.assertEqual(6, metrics[Token.TEXT])
        self.assertEqual(2, metrics[Token.WS])
        self.assertEqual(2, metrics[Token.list_item])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.paragraph, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.LINEBREAK, metrics.pop())
        self.assertEqual(Token.list_item, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.list_item, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        # The last TEXT element is the word ending in ":".
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_list_in_proc(self):

        value = " 01. first-text more-text:\n* First\n* Second\n* Last.\n02.  next-text more-text\nend-text"
        initial = Parser(GrammarType.CONTAINER).invoke(value)

        metrics = TokenMetrics()
        transformed = ContainerTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(20, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(1, metrics[Token.paragraph])
        self.assertEqual(2, metrics[Token.NEWLINE])
        self.assertEqual(8, metrics[Token.TEXT])
        self.assertEqual(3, metrics[Token.WS])
        self.assertEqual(3, metrics[Token.list_item])
        self.assertEqual(2, metrics[Token.proc_item])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.paragraph, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())
        self.assertEqual(Token.proc_item, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())
        self.assertEqual(Token.proc_item, metrics.pop())
        self.assertEqual(Token.list_item, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.list_item, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.list_item, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)
