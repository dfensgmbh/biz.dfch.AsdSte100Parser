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

"""test_paragraph"""

from biz.dfch.ste100parser import GrammarType, Parser, Token

from ...test_case_container_base import TestCaseContainerBase


class TestParagraph(TestCaseContainerBase):

    def _invoke(self, value: str, expected, start_token: Token = Token.start):

        initial = self.invoke(value)
        transformed = self.transform(initial)

        print(transformed.pretty())

        token_tree = self.get_token_tree(transformed)
        token, children = token_tree
        self.assertEqual(start_token, token)

        result = self.get_tokens(children)
        self.assertEqual(expected, result)

    def test_leading_ws_at_sof_fails(self):
        value = " leading-space-is-not-valid"

        result = Parser(GrammarType.CONTAINER).is_valid(value)
        self.assertFalse(result)

    def test_newline_is_part_of_para(self):

        expected = [
            Token.paragraph,
        ]

        value = "arbitrary-text-that-is-part-of-the-paragraph\nmore-paragraph-text.\n"
        self._invoke(value, expected)

    def test_double_newline_ends_para(self):

        expected = [
            Token.paragraph,
            Token.paragraph,
        ]

        value = "text-in-1st-para\n\ntext-in-2nd-para"
        self._invoke(value, expected)

    def test_bold_in_para(self):

        expected = [
            Token.paragraph,
        ]

        value = "text-in*bold*"
        self._invoke(value, expected)

    def test_emph_in_para(self):

        expected = [
            Token.paragraph,
        ]

        value = "text-in_emph_"

        self._invoke(value, expected)

    def test_bold_emph_in_para(self):

        expected = [
            Token.paragraph,
        ]

        value = "text-in*_bold-emph_*"
        self._invoke(value, expected)

    def test_dquote_in_para(self):

        expected = [
            Token.paragraph,
        ]

        value = 'text-in"dquote"'
        self._invoke(value, expected)

    def test_squote_in_para(self):

        expected = [
            Token.paragraph,
        ]

        value = "text-in'squote'"
        self._invoke(value, expected)

    def test_paren_in_para(self):

        expected = [
            Token.paragraph,
        ]

        value = "text-in(parentheses)"
        self._invoke(value, expected)

    def test_mul_in_para(self):

        expected = [
            Token.MULTIPLY,
        ]

        value = " * "
        self._invoke(value, expected, Token.paragraph)

    def test_apostrophe_in_para1(self):

        expected = [
            Token.paragraph,
        ]

        value = "Peter's."
        self._invoke(value, expected)

    def test_apostrophe_in_para2(self):

        expected = [
            Token.paragraph,
        ]

        value = "Manufacturers'."
        self._invoke(value, expected)

    def test_proc_after_para(self):

        expected = [
            Token.paragraph,
            Token.proc_item,
        ]

        value = "Some-text.\n\n1. proc-item"
        self._invoke(value, expected)
