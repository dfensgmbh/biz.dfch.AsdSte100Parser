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

"""test_bold_emph"""

from biz.dfch.ste100parser import GrammarType, Parser, Token
from biz.dfch.ste100parser.transformer import ContainerTransformer

from ...test_case_container_base import TestCaseContainerBase


class TestBoldEmph(TestCaseContainerBase):
    """TestBoldEmph"""

    def _invoke(self, value: str, expected, start_token: Token = Token.start):

        initial = self.invoke(value)
        transformed = self.transform(initial)

        print(transformed.pretty())

        token_tree = self.get_token_tree(transformed)
        token, children = token_tree
        self.assertEqual(start_token, token)

        result = self.get_tokens(children)
        self.assertEqual(expected, result)

    def test(self):

        value = "*_bold-emph text_* at the start"
        initial = Parser(GrammarType.CONTAINER).invoke(value)

        transformed = ContainerTransformer(log=True).transform(initial)
        print(transformed.pretty())

    def test_multi_line_fails(self):

        value = "*_some_code\nmore code_* "
        result = Parser(GrammarType.CONTAINER).is_valid(value)

        self.assertFalse(result)

    def test_single_open_fails(self):
        value = "*_"
        result = Parser(GrammarType.CONTAINER).is_valid(value)

        self.assertFalse(result)

    def test_single_close_fails(self):
        value = "_*"
        result = Parser(GrammarType.CONTAINER).is_valid(value)

        self.assertFalse(result)

    def test_empty_fails(self):
        value = "*__*"
        result = Parser(GrammarType.CONTAINER).is_valid(value)

        self.assertFalse(result)

    def test_in_dquote(self):
        value = '"*__*"'
        initial = Parser(GrammarType.CONTAINER).invoke(value)

        transformed = ContainerTransformer(log=True).transform(initial)
        print(transformed.pretty())

    def test_in_squote(self):
        value = "'*__*'"
        initial = Parser(GrammarType.CONTAINER).invoke(value)

        transformed = ContainerTransformer(log=True).transform(initial)
        print(transformed.pretty())
