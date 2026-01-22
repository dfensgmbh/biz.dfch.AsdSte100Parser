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

"""test_apostrophe"""

from biz.dfch.ste100parser import Token

from ...test_case_container_base import TestCaseContainerBase


class TestApostrophe(TestCaseContainerBase):
    """TestApostrophe"""

    def _invoke(
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

    def test_apostrophe_singular(self):

        expected = [
            Token.TEXT,
            Token.APOSTROPHE,
            Token.WS,
            Token.TEXT,
        ]

        value = """Peter's cat."""
        self._invoke(value, expected, Token.paragraph, level=1)

    def test_apostrophe_inside_squote(self):

        expected = [
            Token.squote,
            Token.WS,
            Token.TEXT,
            Token.WS,
            Token.TEXT,
        ]

        value = """'Peter's cat.' in squote."""
        self._invoke(value, expected, Token.paragraph, level=1)

    def test_apostrophe_inside_dquote(self):

        expected = [
            Token.paragraph,
        ]

        value = """"Peter's cat." in squote."""
        self._invoke(value, expected)

    def test_apostrophe_plural(self):

        expected = [
            Token.TEXT,
            Token.APOSTROPHE,
            Token.WS,
            Token.TEXT,
        ]

        value = """Manufacturers' regulations."""
        self._invoke(value, expected, Token.paragraph, level=1)

    def test_apostrophe_plural_in_squote_is_ambiguous(self):

        value = """'Manufacturers' regulations' in squote."""

        expected = [
            Token.paragraph,
        ]
        self._invoke(value, expected)

        expected = [
            Token.squote,
            Token.WS,
            Token.TEXT,
            Token.WS,
            Token.TEXT,
        ]

        self._invoke(value, expected, Token.paragraph, level=1)

        expected = [
            Token.TEXT,
            Token.APOSTROPHE,
            Token.WS,
            Token.TEXT,
        ]

        self._invoke(value, expected, Token.squote, level=2)

    def test_apostrophe_plural_in_dquote(self):

        expected = [
            Token.paragraph,
        ]

        value = """"Manufacturers' regulations" in squote."""
        self._invoke(value, expected)
