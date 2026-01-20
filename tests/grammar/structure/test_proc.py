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

"""test_proc"""

import unittest

from parameterized import parameterized

from biz.dfch.ste100parser import GrammarType, Parser, Token, TokenMetrics
from biz.dfch.ste100parser.transformer import StructureTransformer


class TestProc(unittest.TestCase):
    """TestProc"""

    @parameterized.expand([
        ("numbered_sof", '''1. some-text more-text''', True),
        ("numbered_sof_with_ws", ''' 1. some-text''', True),
        ("numbered_sof_with_ws", '''  1. some-text''', True),
        ("numbered_sof_with_ws", '''   1. some-text''', True),
        ("multi_numbered_sof", '''123. some-text more-text''', True),
        ("multi_numbered_sof_with_ws", ''' 123. some-text''', True),
        ("multi_numbered_sof_with_ws", '''  123. some-text''', True),
        ("multi_numbered_sof_with_ws", '''   123. some-text''', True),

        ("upper_sof", '''A. some-text more-text''', True),
        ("upper_sof_with_ws", ''' A. some-text more-text''', True),
        ("upper_sof_with_ws", '''  A. some-text more-text''', True),
        ("upper_sof_with_ws", '''   A. some-text more-text''', True),
        ("multi_upper_sof", '''ABC. some-text more-text''', True),
        ("multi_upper_sof_with_ws", ''' ABC. some-text more-text''', True),
        ("multi_upper_sof_with_ws", '''  ABC. some-text more-text''', True),
        ("multi_upper_sof_with_ws", '''   ABC. some-text more-text''', True),

        ("lower_sof", '''a. some-text more-text''', True),
        ("lower_sof_with_ws", ''' a. some-text more-text''', True),
        ("lower_sof_with_ws", '''  a. some-text more-text''', True),
        ("lower_sof_with_ws", '''   a. some-text more-text''', True),
        ("multi_lower_sof", '''abc. some-text more-text''', True),
        ("multi_lower_sof_with_ws", ''' abc. some-text more-text''', True),
        ("multi_lower_sof_with_ws", '''  abc. some-text more-text''', True),
        ("multi_lower_sof_with_ws", '''   abc. some-text more-text''', True),

        ("numbered_sof", '''1. some-text more-text\n''', True),
        ("numbered_sof_with_ws", ''' 1. some-text\n''', True),
        ("numbered_sof_with_ws", '''  1. some-text\n''', True),
        ("numbered_sof_with_ws", '''   1. some-text\n''', True),
        ("multi_numbered_sof", '''123. some-text more-text\n''', True),
        ("multi_numbered_sof_with_ws", ''' 123. some-text\n''', True),
        ("multi_numbered_sof_with_ws", '''  123. some-text\n''', True),
        ("multi_numbered_sof_with_ws", '''   123. some-text\n''', True),

        ("upper_sof", '''A. some-text more-text\n''', True),
        ("upper_sof_with_ws", ''' A. some-text more-text\n''', True),
        ("upper_sof_with_ws", '''  A. some-text more-text\n''', True),
        ("upper_sof_with_ws", '''   A. some-text more-text\n''', True),
        ("multi_upper_sof", '''ABC. some-text more-text\n''', True),
        ("multi_upper_sof_with_ws", ''' ABC. some-text more-text\n''', True),
        ("multi_upper_sof_with_ws", '''  ABC. some-text more-text\n''', True),
        ("multi_upper_sof_with_ws", '''   ABC. some-text more-text\n''', True),

        ("lower_sof", '''a. some-text more-text\n''', True),
        ("lower_sof_with_ws", ''' a. some-text more-text\n''', True),
        ("lower_sof_with_ws", '''  a. some-text more-text\n''', True),
        ("lower_sof_with_ws", '''   a. some-text more-text\n''', True),
        ("multi_lower_sof", '''abc. some-text more-text\n''', True),
        ("multi_lower_sof_with_ws", ''' abc. some-text more-text\n''', True),
        ("multi_lower_sof_with_ws", '''  abc. some-text more-text\n''', True),
        ("multi_lower_sof_with_ws", '''   abc. some-text more-text\n''', True),

        ("numbered_mid", '''\n1. some-text more-text''', True),
        ("numbered_mid_with_ws", '''\n 1. some-text''', True),
        ("numbered_mid_with_ws", '''\n  1. some-text''', True),
        ("numbered_mid_with_ws", '''\n   1. some-text''', True),
        ("multi_numbered_mid", '''\n123. some-text more-text''', True),
        ("multi_numbered_mid_with_ws", '''\n 123. some-text''', True),
        ("multi_numbered_mid_with_ws", '''\n  123. some-text''', True),
        ("multi_numbered_mid_with_ws", '''\n   123. some-text''', True),

        ("upper_mid", '''\nA. some-text more-text''', True),
        ("upper_mid_with_ws", '''\n A. some-text more-text''', True),
        ("upper_mid_with_ws", '''\n  A. some-text more-text''', True),
        ("upper_mid_with_ws", '''\n   A. some-text more-text''', True),
        ("multi_upper_mid", '''\nABC. some-text more-text''', True),
        ("multi_upper_mid_with_ws", '''\n ABC. some-text more-text''', True),
        ("multi_upper_mid_with_ws", '''\n  ABC. some-text more-text''', True),
        ("multi_upper_mid_with_ws", '''\n   ABC. some-text more-text''', True),

        ("lower_mid", '''\na. some-text more-text''', True),
        ("lower_mid_with_ws", '''\n a. some-text more-text''', True),
        ("lower_mid_with_ws", '''\n  a. some-text more-text''', True),
        ("lower_mid_with_ws", '''\n   a. some-text more-text''', True),
        ("multi_lower_mid", '''\nabc. some-text more-text''', True),
        ("multi_lower_mid_with_ws", '''\n abc. some-text more-text''', True),
        ("multi_lower_mid_with_ws", '''\n  abc. some-text more-text''', True),
        ("multi_lower_mid_with_ws", '''\n   abc. some-text more-text''', True),

        ("multi_space_will_push_space_into_line", '''1 .  some-text more-text''', True),

        ("alpha_num_mid", '''\n1a. some-text more-text''', True),
        ("alpha_num_mid_with_ws", '''\n 1a. some-text''', True),
        ("alpha_num_mid_with_ws", '''\n  1a. some-text''', True),
        ("alpha_num_mid_with_ws", '''\n   1a. some-text''', True),
        ("multi_alpha_num_mid", '''\n123a. some-text more-text''', True),
        ("multi_alpha_num_mid_with_ws", '''\n 123a. some-text''', True),
        ("multi_alpha_num_mid_with_ws", '''\n  123a. some-text''', True),
        ("multi_alpha_num_mid_with_ws", '''\n   123a. some-text''', True),
    ])
    def test_is_valid(self, rule, value, expected):  # NOSONAR(54144)

        result = Parser(GrammarType.STRUCTURE).is_valid(value)
        self.assertEqual(expected, result, rule)

    def test_proc2(self):
        value = "91. first-text more-text\n02. next-text more-text\nend-text"
        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

    @parameterized.expand([
        ("sof_multi", "01.  first-text more-text\r\n  02.  next-text more-text\r\nend-text", True),
        ("sof_multi", "01. first-text more-text\n  02.  next-text more-text\nend-text", True),
        ("leading_space_multi", " 01. first-text more-text\n  02.  next-text more-text\nend-text", True),
        ("leading_space_multi", "  01. first-text more-text\r\n  02.  next-text more-text\nend-text", True),
        ("leading_crlf_multi", "\r\n01. first-text more-text\n  02.  next-text more-text\nend-text", True),
        ("leading_crlf_multi", "\n01. first-text more-text\n  02.  next-text more-text\nend-text", True),
        ("leading_crlf_and_space_multi", "\r\n 01. first-text more-text\n  02.  next-text more-text\nend-text", True),
        ("leading_crlf_and_space_multi", "\n 01. first-text more-text\n  02.  next-text more-text\nend-text", True),
    ])
    def test_proc(self, rule, value, expected):  # NOSONAR(54144)

        _ = rule
        _ = expected

        value = " 01. first-text more-text\n  02.  next-text more-text\nend-text"
        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(14, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(1, metrics[Token.paragraph])
        self.assertEqual(5, metrics[Token.TEXT])
        self.assertEqual(3, metrics[Token.WS])
        self.assertEqual(2, metrics[Token.NEWLINE])
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
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)
