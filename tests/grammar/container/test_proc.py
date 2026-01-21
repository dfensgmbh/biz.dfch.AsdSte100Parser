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

# pylint: disable=C0115
# pylint: disable=C0116
# pylint: disable=C0301
# type: ignore

"""test_proc"""

from parameterized import parameterized

from biz.dfch.ste100parser import Token

from ...test_case_container_base import TestCaseContainerBase


class TestProc(TestCaseContainerBase):

    def assert_tree(
        self,
        value: str,
        expected,
        start_token: Token = Token.start,
        level: int = 0,
    ):

        initial = self.invoke(value)
        transformed = self.transform(initial)

        print(transformed.pretty())

        token_tree = self.get_token_tree(transformed)
        token, children = token_tree
        for _ in range(level):
            token, children = children[0]
        self.assertEqual(start_token, token)

        result = self.get_tokens(children)
        self.assertEqual(expected, result)

    def test_proc3(self):

        value = "\n91. first-text more-text\n02. next-text more-text\nend-text"

        expected = [
            Token.proc_item,
            Token.proc_item,
            Token.paragraph,
        ]
        self.assert_tree(value, expected)

        expected = [
            Token.PROC_STEP,
            Token.PROC_DELIMITER,
            Token.TEXT,
            Token.WS,
            Token.TEXT,
        ]
        self.assert_tree(value, expected, Token.proc_item, level=1)

    @parameterized.expand([
        ("numbered_sof", '''\n1. some-text more-text''', True),
        ("numbered_sof_with_ws", '''\n 1. some-text''', False),
        ("numbered_sof_with_ws", '''\n 1. some-text''', False),
        ("numbered_sof_with_ws", '''\n   1. some-text''', False),
        ("multi_numbered_sof", '''\n123. some-text more-text''', True),
        ("multi_numbered_sof_with_ws", '''\n 123. some-text''', False),
        ("multi_numbered_sof_with_ws", '''\n  123. some-text''', False),
        ("multi_numbered_sof_with_ws", '''\n   123. some-text''', False),

        ("upper_sof", '''\nA. some-text more-text''', True),
        ("upper_sof_with_ws", '''\n A. some-text more-text''', False),
        ("upper_sof_with_ws", '''\n  A. some-text more-text''', False),
        ("upper_sof_with_ws", '''\n   A. some-text more-text''', False),
        ("multi_upper_sof", '''\nABC. some-text more-text''', True),
        ("multi_upper_sof_with_ws", '''\n ABC. some-text more-text''', False),
        ("multi_upper_sof_with_ws", '''\n  ABC. some-text more-text''', False),
        ("multi_upper_sof_with_ws", '''\n   ABC. some-text more-text''', False),

        ("lower_sof", '''\na. some-text more-text''', True),
        ("lower_sof_with_ws", '''\n a. some-text more-text''', False),
        ("lower_sof_with_ws", '''\n  a. some-text more-text''', False),
        ("lower_sof_with_ws", '''\n   a. some-text more-text''', False),
        ("multi_lower_sof", '''\nabc. some-text more-text''', True),
        ("multi_lower_sof_with_ws", '''\n abc. some-text more-text''', False),
        ("multi_lower_sof_with_ws", '''\n  abc. some-text more-text''', False),
        ("multi_lower_sof_with_ws", '''\n   abc. some-text more-text''', False),

        ("numbered_sof", '''\n1. some-text more-text\n''', True),
        ("numbered_sof_with_ws", '''\n 1. some-text\n''', False),
        ("numbered_sof_with_ws", '''\n  1. some-text\n''', False),
        ("numbered_sof_with_ws", '''\n   1. some-text\n''', False),
        ("multi_numbered_sof", '''\n123. some-text more-text\n''', True),
        ("multi_numbered_sof_with_ws", '''\n 123. some-text\n''', False),
        ("multi_numbered_sof_with_ws", '''\n  123. some-text\n''', False),
        ("multi_numbered_sof_with_ws", '''\n   123. some-text\n''', False),

        ("upper_sof", '''\nA. some-text more-text\n''', True),
        ("upper_sof_with_ws", '''\n A. some-text more-text\n''', False),
        ("upper_sof_with_ws", '''\n  A. some-text more-text\n''', False),
        ("upper_sof_with_ws", '''\n   A. some-text more-text\n''', False),
        ("multi_upper_sof", '''\nABC. some-text more-text\n''', True),
        ("multi_upper_sof_with_ws", '''\n ABC. some-text more-text\n''', False),
        ("multi_upper_sof_with_ws", '''\n  ABC. some-text more-text\n''', False),
        ("multi_upper_sof_with_ws", '''\n   ABC. some-text more-text\n''', False),

        ("lower_sof", '''\na. some-text more-text\n''', True),
        ("lower_sof_with_ws", '''\n a. some-text more-text\n''', False),
        ("lower_sof_with_ws", '''\n  a. some-text more-text\n''', False),
        ("lower_sof_with_ws", '''\n   a. some-text more-text\n''', False),
        ("multi_lower_sof", '''abc. some-text more-text\n''', True),
        ("multi_lower_sof_with_ws", '''\n abc. some-text more-text\n''', False),
        ("multi_lower_sof_with_ws", '''\n  abc. some-text more-text\n''', False),
        ("multi_lower_sof_with_ws", '''\n   abc. some-text more-text\n''', False),

        ("numbered_mid", '''\n1. some-text more-text''', True),
        ("numbered_mid_with_ws", '''\n 1. some-text''', False),
        ("numbered_mid_with_ws", '''\n  1. some-text''', False),
        ("numbered_mid_with_ws", '''\n   1. some-text''', False),
        ("multi_numbered_mid", '''\n123. some-text more-text''', True),
        ("multi_numbered_mid_with_ws", '''\n 123. some-text''', False),
        ("multi_numbered_mid_with_ws", '''\n  123. some-text''', False),
        ("multi_numbered_mid_with_ws", '''\n   123. some-text''', False),

        ("upper_mid", '''\nA. some-text more-text''', True),
        ("upper_mid_with_ws", '''\n A. some-text more-text''', False),
        ("upper_mid_with_ws", '''\n  A. some-text more-text''', False),
        ("upper_mid_with_ws", '''\n   A. some-text more-text''', False),
        ("multi_upper_mid", '''\nABC. some-text more-text''', True),
        ("multi_upper_mid_with_ws", '''\n ABC. some-text more-text''', False),
        ("multi_upper_mid_with_ws", '''\n  ABC. some-text more-text''', False),
        ("multi_upper_mid_with_ws", '''\n   ABC. some-text more-text''', False),

        ("lower_mid", '''\na. some-text more-text''', True),
        ("lower_mid_with_ws", '''\n a. some-text more-text''', False),
        ("lower_mid_with_ws", '''\n  a. some-text more-text''', False),
        ("lower_mid_with_ws", '''\n   a. some-text more-text''', False),
        ("multi_lower_mid", '''\nabc. some-text more-text''', True),
        ("multi_lower_mid_with_ws", '''\n abc. some-text more-text''', False),
        ("multi_lower_mid_with_ws", '''\n  abc. some-text more-text''', False),
        ("multi_lower_mid_with_ws", '''\n   abc. some-text more-text''', False),

        ("multi_space_invalid", '''\n1 .  some-text more-text''', False),

        ("alpha_num_mid", '''\n1a. some-text more-text''', True),
        ("alpha_num_mid_with_ws", '''\n 1a. some-text''', False),
        ("alpha_num_mid_with_ws", '''\n  1a. some-text''', False),
        ("alpha_num_mid_with_ws", '''\n   1a. some-text''', False),
        ("multi_alpha_num_mid", '''\n123a. some-text more-text''', True),
        ("multi_alpha_num_mid_with_ws", '''\n 123a. some-text''', False),
        ("multi_alpha_num_mid_with_ws", '''\n  123a. some-text''', False),
        ("multi_alpha_num_mid_with_ws", '''\n   123a. some-text''', False),
    ])
    def test_is_valid(self, rule, value, expected):  # NOSONAR(54144)

        result = self._parser.is_valid(value)
        self.assertEqual(expected, result, rule)

    def test_proc2(self):
        value = "\n91. first-text more-text\n02. next-text more-text\nend-text"

        expected = [
            Token.proc_item,
            Token.proc_item,
            Token.paragraph,
        ]
        self.assert_tree(value, expected)

        expected = [
            Token.PROC_STEP,
            Token.PROC_DELIMITER,
            Token.TEXT,
            Token.WS,
            Token.TEXT,
        ]
        self.assert_tree(value, expected, Token.proc_item, level=1)

    @parameterized.expand([
        ("leading_space_multi",
         "\n 01. first-text more-text\n  02.  next-text more-text\nend-text", False),
        ("leading_space_multi",
         "\n  01. first-text more-text\r\n  02.  next-text more-text\nend-text", False),
        ("leading_crlf_multi",
         "\n99. first-text more-text\n02. next-text more-text\nend-text", True),
        ("leading_crlf_multi",
         "\n88. first-text more-text\n02. next-text more-text\nend-text", True),
        ("leading_crlf_and_space_multi",
         "\r\n 01. first-text more-text\n 02.  next-text more-text\nend-text", False),
        ("leading_crlf_and_space_multi",
         "\n 01. first-text more-text\n  02.  next-text more-text\nend-text", False),
    ])
    def test_proc(self, rule, value, _expected):  # NOSONAR(54144)

        _ = rule

        if not _expected:
            result = self._parser.is_valid(value)
            self.assertFalse(result)
            return

        expected = [
            Token.proc_item,
            Token.proc_item,
            Token.paragraph,
        ]
        self.assert_tree(value, expected)

        expected = [
            Token.PROC_STEP,
            Token.PROC_DELIMITER,
            Token.TEXT,
            Token.WS,
            Token.TEXT,
        ]
        self.assert_tree(value, expected, Token.proc_item, level=1)
