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

"""TestCaseBase"""

import unittest
from pathlib import Path

from biz.dfch.ste100parser import Token
from biz.dfch.ste100parser.transformer import TokenConverter


class TestCaseBase(unittest.TestCase):
    """Base class for test cases that use a file as the input."""

    _test_data_dir = Path(__file__).parent / "test_data"

    def load_test_file(self, filename: str) -> str:
        """
        Utility function that loads test files from the test_data
        directory.
        """

        file_path = self._test_data_dir / filename
        if not file_path.exists():
            self.fail(f"File not found: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def get_token_tree(self, parse_tree) -> tuple[Token, list] | str:
        result = TokenConverter().invoke(parse_tree)

        return result

    def get_tokens(self, children) -> list:
        result = [
            child[0] for child in children
            if isinstance(child, tuple)
        ]
        return result

    def format_parse_tree(
        self,
        skeleton: tuple[Token, list] | str,
        indent: int = 0
    ) -> str:
        """
        Formats the result of the TokenConverter into a readable indented
        format.
        """

        padding = "." * indent

        # If the converter returned a string, it is a leaf value.
        if isinstance(skeleton, str):
            return skeleton

        token, children = skeleton
        token_name = token.name

        # Check if this node contains only a single string leaf.
        if 1 == len(children) and isinstance(children[0], str):
            return f"{padding}{token_name} {children[0]}"

        # Otherwise, it is a container with multiple children or sub-trees.
        result = [f"{padding}{token_name}"]
        for child in children:
            formatted_child = self.format_parse_tree(child, indent + 1)

            # If the child was a sub-tree, it is already padded.
            # If it was a raw string (not inlined), we pad it here.
            if isinstance(child, str):
                result.append(f"{padding}  {formatted_child}")
            else:
                result.append(formatted_child)

        return "\n".join(result)
