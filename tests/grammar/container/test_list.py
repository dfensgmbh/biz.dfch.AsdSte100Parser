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

from parameterized import parameterized

from biz.dfch.ste100parser import GrammarType, Parser, Token
from biz.dfch.ste100parser.transformer import ContainerTransformer

from ...test_case_container_base import TestCaseContainerBase
from ...test_data.test_data import TestData


class TestList(TestCaseContainerBase):
    """TestList"""

    def _invoke(self, value: str, expected):

        initial = self.invoke(value)
        transformed = self.transform(initial)

        print(transformed.pretty())

        token_tree = self.get_token_tree(transformed)
        token, children = token_tree
        self.assertEqual(Token.start, token)

        result = self.get_tokens(children)
        self.assertEqual(expected, result)

    @parameterized.expand([
        ("bullet", "Para-start:\n * First\n * Second\n * Last.\nPara-end.", True),
        ("bullet", "Para-start:\n  * First\n  * Second\n  * Last.\nPara-end.", True),
        ("bullet_with_bold", "Para-start:\n * *First*\n * Second\n * Last.\nPara-end.", True),
        ("dash", "Para-start:\n - First\n - Second\n - Last.\nPara-end.", True),
        ("dash", "Para-start:\n  - First\n  - Second\n  - Last.\nPara-end.", True),
        ("number", "Para-start:\n 1 First\n 2 Second\n 3 Last.\nPara-end.", True),
        ("lower", "Para-start:\n a First\n b Second\n c Last.\nPara-end.", True),
        ("upper", "Para-start:\n A First\n B Second\n C Last.\nPara-end.", True),
        ("mixed", "Para-start:\n 1A First\n1B Second\n 1C Last.\nPara-end.", True),
        ("mixed", "Para-start:\n 1a First\n 1c Second\n 1c Last.\nPara-end.", True),
    ])
    def test(self, rule, value, expected):
        _ = rule
        _ = expected

        initial = Parser(GrammarType.CONTAINER).invoke(value)

        transformed = ContainerTransformer(log=True).transform(initial)
        print(transformed.pretty())

    def test_list_in_paragraph(self):

        expected = [
            Token.paragraph,
        ]

        value = self.load_test_file(TestData.LIST_IN_PARAGRAPH)
        self._invoke(value, expected)

    def test_list_in_proc(self):

        expected = [
            Token.proc_item,
            Token.proc_item,
            Token.paragraph,
        ]

        value = self.load_test_file(TestData.LIST_IN_PROC)
        self._invoke(value, expected)
