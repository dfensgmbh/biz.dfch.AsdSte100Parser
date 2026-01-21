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
# type: ignore

"""test_ws"""

from parameterized import parameterized

from biz.dfch.ste100parser import Token

from ...test_case_container_base import TestCaseContainerBase


class TestWs(TestCaseContainerBase):

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

    @parameterized.expand([
        ("single", 'text ', True),
        ("double", 'text  ', True),
        ("triple", 'text   ', True),
        ("single_tab", 'text\t', True),
        ("double_tab", 'text\t\t', True),
        ("triple_tab", 'text\t\t\t', True),
        ("mixed", 'text\t \t', True),
    ])
    def test_ws_single_token(self, rule, value, expected):

        _ = rule
        _ = expected

        expected = [
            Token.TEXT,
            Token.WS,
        ]
        self.assert_tree(value, expected, Token.paragraph)

    @parameterized.expand([
        ("tab", '\t.', False),
        ("single", ' .', False),
        ("single", ' text', False),
        ("double", '  text', False),
        ("triple", '   text', False),
        ("tab_single", '\ttext', False),
        ("tab_double", '\t\ttext', False),
        ("tab_triple", '\t\t\ttext', False),
        ("mixed", '\t \t text', False),
    ])
    def test_ws_start_fails(self, rule, value, expected):

        _ = rule
        _ = expected

        result = self._parser.is_valid(value)
        self.assertFalse(result)

    @parameterized.expand([
        ("single", '. ', True),
        ("tab", '.\t', True),
    ])
    def test_ws_end(self, rule, value, expected):

        _ = rule
        _ = expected

        expected = [
            Token.TEXT,
            Token.WS,
        ]
        self.assert_tree(value, expected, Token.paragraph)
