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

"""test_cite"""

from biz.dfch.ste100parser import Token

from ...test_case_container_base import TestCaseContainerBase


class TestCite(TestCaseContainerBase):
    """TestCite"""

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

    def test_cite(self):

        value = "\r\n> cite-text more-text\nend-text"

        expected = [
            Token.cite,
            Token.paragraph,
        ]
        self.assert_tree(value, expected)

        expected = [
            Token.TEXT,
            Token.WS,
            Token.TEXT,
        ]
        self.assert_tree(value, expected, Token.cite, level=1)

    def test_cite_sof(self):
        """Cite at the start of the input (without a line break at the start) is valid."""

        value = "> cite-text more-text\nend-text"

        expected = [
            Token.cite,
            Token.paragraph,
        ]
        self.assert_tree(value, expected)

        expected = [
            Token.TEXT,
            Token.WS,
            Token.TEXT,
        ]
        self.assert_tree(value, expected, Token.cite, level=1)

    def test_cite_with_bold(self):

        value = "\r\n> cite-text *bold-text*\nend-text"

        expected = [
            Token.cite,
            Token.paragraph,
        ]
        self.assert_tree(value, expected)

        expected = [
            Token.TEXT,
            Token.WS,
            Token.bold,
        ]
        self.assert_tree(value, expected, Token.cite, level=1)

    def test_empty_fails(self):
        """An 'empty' cite line must contain a minimum of one WS."""

        value = "\n> \n"

        result = self._parser.is_valid(value)
        self.assertFalse(result)

    def test_ws_fails(self):
        """An 'empty' cite line must contain a minimum of one WS."""

        value = "\n>  \n"

        result = self._parser.is_valid(value)
        self.assertFalse(result)

    def test_multi(self):

        value = "\r\n> first-text *some-text*\n> next-text 'more-text'\nend-text"

        expected = [
            Token.cite,
            Token.cite,
            Token.paragraph,
        ]
        self.assert_tree(value, expected)

        expected = [
            Token.TEXT,
            Token.WS,
            Token.bold,
        ]
        self.assert_tree(value, expected, Token.cite, level=1)

    def test_cite_with_paren(self):

        value = "\r\n> cite-text (more-text)\nend-text"

        expected = [
            Token.cite,
            Token.paragraph,
        ]
        self.assert_tree(value, expected)

        expected = [
            Token.TEXT,
            Token.WS,
            Token.paren,
        ]
        self.assert_tree(value, expected, Token.cite, level=1)

    def test_cite_with_nested_paren(self):

        value = "\r\n> ((cite-text)) (more-text)\nend-text"

        expected = [
            Token.cite,
            Token.paragraph,
        ]
        self.assert_tree(value, expected)

        expected = [
            Token.paren,
            Token.WS,
            Token.paren,
        ]
        self.assert_tree(value, expected, Token.cite, level=1)

        expected = [
            Token.paren,
        ]
        self.assert_tree(value, expected, Token.paren, level=2)

        expected = [
            Token.TEXT,
        ]
        self.assert_tree(value, expected, Token.paren, level=3)
