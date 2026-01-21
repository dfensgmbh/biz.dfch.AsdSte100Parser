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

"""test_generic"""

from parameterized import parameterized

from biz.dfch.ste100parser import Char, GrammarType, Parser, Token
from biz.dfch.ste100parser.transformer import ContainerTransformer

from ...test_case_container_base import TestCaseContainerBase


class TestGeneric(TestCaseContainerBase):

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

    def test(self):

        value = "`_first`: 4 * 3\nNext-line-ddf\r\n\nFourth-line"

        expected = [
            Token.paragraph,
            Token.paragraph,
        ]
        self.assert_tree(value, expected)

        expected = [
            Token.CODE,
            Token.TEXT,
            Token.WS,
            Token.TEXT,
            Token.MULTIPLY,
            Token.TEXT,
            Token.LINEBREAK,
            Token.TEXT,
        ]
        self.assert_tree(value, expected, Token.paragraph, level=1)

    def test_newline(self):

        value = "first line\r\n\nsecond and last line"

        expected = [
            Token.paragraph,
            Token.paragraph,
        ]
        self.assert_tree(value, expected, Token.start)

        expected = [
            Token.TEXT,
            Token.WS,
            Token.TEXT,
        ]
        self.assert_tree(value, expected, Token.paragraph, level=1)

    @parameterized.expand([
        ("empty", Char.EMPTY, False),
        ("space", Char.SPACE, False),
        ("tab", Char.TAB, False),

        ("char_lower", 'a', True),
        ("char_upper", 'A', True),
        ("chars_lower", 'abc', True),
        ("chars_upper", 'ABC', True),
        ("chars_mixed", 'Abc', True),
        ("alpha_numeric1", 'abcABC123', True),
        ("alpha_numeric2", 'ABCabc123', True),
        ("alpha_numeric3", '123ABCabc', True),

        ("dot", Char.DOT, True),
        ("comma", Char.COMMA, True),
        ("colon", Char.COLON, True),
        ("question", Char.QUESTION, True),
        ("exclamation", Char.EXCLAMATION, True),

        ("alpha_num_ends_with_dot", "1TextThatEndsWithDot.", True),
        ("alpha_num_ends_with_comma", "1TextThatEndsWithComma,", True),
        ("alpha_num_ends_with_colon", "1TextThatEndsWithColon:", True),
        ("alpha_num_ends_with_question", "1TextThatEndsWithQuestion?", True),
        ("alpha_num_ends_with_exclamation", "1TextThatEndsWithExcl!", True),
    ])
    def test_text0(self, rule, value, expected):

        sut = Parser(GrammarType.CONTAINER)

        if expected is False:
            self.assertFalse(sut.is_valid(value), rule)
            return

        expected = [
            Token.TEXT,
        ]
        self.assert_tree(value, expected, Token.paragraph)

    @parameterized.expand([
        ("text_space", "text ", True),
        ("space_text", " text", False),
    ])
    def test_text1(self, rule, value, expected):

        _ = rule
        _ = expected

        if not expected:
            result = Parser(GrammarType.CONTAINER).is_valid(value)
            self.assertFalse(result)

            return

        initial = Parser(GrammarType.CONTAINER).invoke(value)

        transformed = ContainerTransformer(log=True).transform(initial)
        print(transformed.pretty())

    @parameterized.expand([
        ("text_space", "text1 text2 ", True),
        ("space_text", " text1 text2", False),
    ])
    def test_text2(self, rule, value, expected):

        _ = rule

        if not expected:
            result = Parser(GrammarType.CONTAINER).is_valid(value)
            self.assertFalse(result)

            return

        initial = Parser(GrammarType.CONTAINER).invoke(value)

        transformed = ContainerTransformer(log=True).transform(initial)
        print(transformed.pretty())
