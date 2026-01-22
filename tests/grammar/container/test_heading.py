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
# pylint: disable=C0301
# type: ignore

"""test_quote"""

from parameterized import parameterized

from biz.dfch.ste100parser import Token

from ...test_case_container_base import TestCaseContainerBase


class TestHeading(TestCaseContainerBase):

    def _invoke(self, value: str, expected):

        initial = self.invoke(value)
        transformed = self.transform(initial)

        print(transformed.pretty())

        token_tree = self.get_token_tree(transformed)
        token, children = token_tree
        self.assertEqual(Token.start, token)

        result = self.get_tokens(children)
        self.assertEqual(expected, result)

    def test_single_heading(self):

        expected = [
            Token.heading,
        ]

        value = "# This-is-a-heading-level-1\n"
        self._invoke(value, expected)

    def test_multi_headings(self):

        expected = [
            Token.heading,
            Token.heading,
            Token.paragraph,
        ]
        value = "# This-is-a-heading-level-1\n\n## This-is-a-heading-level-2\n\nThis-is-normal-text.\n"
        self._invoke(value, expected)

    @parameterized.expand([
        ("level_1", "# This-is-a-heading-level-1\n", 1),
        ("level_2", "## This-is-a-heading-level-2\n", 2),
        ("level_3", "### This-is-a-heading-level-3\n", 3),
        ("level_4", "#### This-is-a-heading-level-4\n", 4),
        ("level_5", "##### This-is-a-heading-level-5\n", 5),
    ])
    def test_heading(self, rule, value, expected):

        _ = rule
        _ = expected

        expected = [
            Token.heading,
        ]

        self._invoke(value, expected)
