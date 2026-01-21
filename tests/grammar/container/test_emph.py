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

"""test_emph"""

from biz.dfch.ste100parser import GrammarType, Parser, Token

from ...test_case_container_base import TestCaseContainerBase


class TestEmph(TestCaseContainerBase):

    def _invoke(self, value: str, expected, start_token: Token = Token.start):

        initial = self.invoke(value)
        transformed = self.transform(initial)

        print(transformed.pretty())

        token_tree = self.get_token_tree(transformed)
        token, children = token_tree
        self.assertEqual(start_token, token)

        result = self.get_tokens(children)
        self.assertEqual(expected, result)

    def test_single(self):

        expected = [
            Token.paragraph,
        ]

        value = "_some-emph_ at-the-start."
        self._invoke(value, expected)

    def test_double(self):

        expected = [
            Token.paragraph,
        ]

        value = "_some-emph_ _more-emph_"
        self._invoke(value, expected)

    def test_multi_line_fails(self):

        value = "_some-emph\nmore-emph_ "
        result = self._parser.is_valid(value)
        self.assertFalse(result)

    def test_single_fails(self):
        value = "_"
        result = Parser(GrammarType.CONTAINER).is_valid(value)

        self.assertFalse(result)

    def test_under_in_dquote(self):

        expected = [
            Token.dquote,
        ]

        value = '"_"'
        self._invoke(value, expected, Token.paragraph)

    def test_under_in_squote(self):

        expected = [
            Token.squote,
        ]

        value = "'_'"
        self._invoke(value, expected, Token.paragraph)
