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

"""TestCodeBlock"""

from biz.dfch.ste100parser import Token
from tests.test_case_container_base import TestCaseContainerBase


class TestCodeBlock(TestCaseContainerBase):

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

    def test_single_line(self):
        value = """```some_code more code```
"""
        expected = [
            Token.code_block,
            Token.NEWLINE,
        ]
        self.assert_tree(value, expected, Token.start)

    def test_single_line_with_lang_id(self):
        value = """```py
some_code more code```
"""
        expected = [
            Token.code_block,
            Token.NEWLINE,
        ]
        self.assert_tree(value, expected, Token.start)
