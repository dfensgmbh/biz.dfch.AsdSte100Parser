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

"""test_text"""

from parameterized import parameterized

from biz.dfch.ste100parser import Token

from ...test_case_container_base import TestCaseContainerBase


class TestText(TestCaseContainerBase):
    """TestText"""

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
        ("lower", "abcdefghijklmopqrstuvwxzy", True),
        ("upper", "ABCDEFGHIJKLMOPQRSTUVWXYZ", True),
        ("digit", "0123456789", True),
        ("umlaut", "äöü", True),
        ("french", r"áàéèëíìïóòúùç", True),
        ("symbols", r"-+=%&/\<>^$£[]{}#@¨´", True),
        ("punctuation", ".,:?!", True),
        ("unicode", "←→↑↓↔↕⇐⇒⇑⇓", True),
        ("guillemets_double", "«", True),
        ("guillemets_double", "»", True),
        ("guillemets_single", "‹", True),
        ("guillemets_single", "›", True),
        ("german_double", "„", True),
        ("german_double", "“", True),
        ("german_single", "‚", True),
        ("german_single", "‘", True),
        ("single_word_with_dash", "single-word", True),

        ("bold", "*", False),
        ("bold_emph", "*_", False),
        ("bold_emph", "_*", False),
        ("emph", "_", False),
        ("code", "`", False),
        ("paren_open", "(", False),
        ("paren_close", ")", False),
    ])
    def test_word(self, rule, value, _expected):
        """Allowed characters."""

        _ = rule
        _ = _expected

        result = self._parser.is_valid(value)
        if False is _expected:
            self.assertFalse(result)
            return

        expected = [
            Token.TEXT,
        ]
        self.assert_tree(value, expected, Token.paragraph)

    def test_single_word_is_paragraph(self):
        """Cite after a line break is valid."""

        value = "this-is-text"

        expected = [
            Token.TEXT,
        ]
        self.assert_tree(value, expected, Token.paragraph)

    def test_multi_word_is_paragraph(self):
        """Cite after a line break is valid."""

        value = "this-is-text this-is-also-text"

        expected = [
            Token.paragraph,
        ]
        self.assert_tree(value, expected)

        expected = [
            Token.TEXT,
            Token.WS,
            Token.TEXT,
        ]
        self.assert_tree(value, expected, Token.paragraph, level=1)
