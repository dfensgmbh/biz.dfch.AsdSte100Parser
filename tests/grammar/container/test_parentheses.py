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

"""test_parentheses"""

from parameterized import parameterized

from biz.dfch.ste100parser import GrammarType, Parser, Token
from biz.dfch.ste100parser.transformer import ContainerTransformer

from ...test_case_container_base import TestCaseContainerBase


class TestParentheses(TestCaseContainerBase):

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

    def test_standalone(self):

        value = "(some-text-in-parentheses)"

        expected = [
            Token.paren,
        ]
        self.assert_tree(value, expected, Token.paragraph)

        expected = [
            Token.TEXT,
        ]
        self.assert_tree(value, expected, Token.paren, level=1)

    def test_multiline(self):

        value = "(some-multiline-text\nin-parentheses)"

        expected = [
            Token.paren,
        ]
        self.assert_tree(value, expected, Token.paragraph)

        expected = [
            Token.TEXT,
            Token.NEWLINE,
            Token.TEXT,
        ]
        self.assert_tree(value, expected, Token.paren, level=1)

    def test_pair_start(self):

        value = "(some text in parentheses) There is some text."

        expected = [
            Token.paragraph,
        ]
        self.assert_tree(value, expected)

        expected = [
            Token.paren,
            Token.WS,
            Token.TEXT,
            Token.WS,
            Token.TEXT,
            Token.WS,
            Token.TEXT,
            Token.WS,
            Token.TEXT,
        ]
        self.assert_tree(value, expected, Token.paragraph, level=1)

        expected = [
            Token.TEXT,
            Token.WS,
            Token.TEXT,
            Token.WS,
            Token.TEXT,
            Token.WS,
            Token.TEXT,
        ]
        self.assert_tree(value, expected, Token.paren, level=2)

    def test_nested(self):

        value = "((round-brackets) some-text-in-parentheses)"

        expected = [
            Token.paren,
        ]
        self.assert_tree(value, expected, Token.paragraph)

        expected = [
            Token.paren,
            Token.WS,
            Token.TEXT,
        ]
        self.assert_tree(value, expected, Token.paren, level=1)

        expected = [
            Token.TEXT,
        ]
        self.assert_tree(value, expected, Token.paren, level=2)

    def test_dquote_in_paren1(self):

        value = """(some-text-in-parentheses "round-brackets")"""
        initial = Parser(GrammarType.CONTAINER).invoke(value)

        transformed = ContainerTransformer(log=True).transform(initial)
        print(transformed.pretty())

    def test_dquote_in_paren2(self):

        value = """(some-text-in-parentheses "(round-brackets)")"""
        initial = Parser(GrammarType.CONTAINER).invoke(value)

        transformed = ContainerTransformer(log=True).transform(initial)
        print(transformed.pretty())

    @parameterized.expand([
        ("dquote", '''"(round\nbrackets)"''', False),
        ("dquote", '''"(round\r\nbrackets)"''', False),
        ("squote", """'(round\nbrackets)'""", False),
        ("squote", """'(round\r\nbrackets)'""", False),
    ])
    # NOSONAR(54144)
    def test_newline_in_paren_in_quote(self, rule, value, expected):

        result = Parser(GrammarType.CONTAINER).is_valid(value)
        self.assertEqual(expected, result, rule)

    def test_empty(self):
        value = "()"
        initial = Parser(GrammarType.CONTAINER).invoke(value)

        transformed = ContainerTransformer(log=True).transform(initial)
        print(transformed.pretty())

    def test_empty_in_dquote(self):
        value = '"()"'
        initial = Parser(GrammarType.CONTAINER).invoke(value)

        transformed = ContainerTransformer(log=True).transform(initial)
        print(transformed.pretty())

    def test_paren_open_fails(self):
        value = ")"
        result = Parser(GrammarType.CONTAINER).is_valid(value)

        self.assertFalse(result)

    def test_paren_close_fails(self):
        value = ")"
        result = Parser(GrammarType.CONTAINER).is_valid(value)

        self.assertFalse(result)

    def test_open_in_dquote(self):
        value = '"("'
        initial = Parser(GrammarType.CONTAINER).invoke(value)

        transformed = ContainerTransformer(log=True).transform(initial)
        print(transformed.pretty())

    def test_close_in_dquote(self):
        value = '")"'
        initial = Parser(GrammarType.CONTAINER).invoke(value)

        transformed = ContainerTransformer(log=True).transform(initial)
        print(transformed.pretty())
