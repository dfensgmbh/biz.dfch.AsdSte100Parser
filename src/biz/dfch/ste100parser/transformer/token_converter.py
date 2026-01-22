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

"""token_converter module."""

from lark import Tree

from ..token import Token

__all__ = [
    "TokenConverter",
]


class TokenConverter:
    """TokenConverter"""

    def invoke(self, node: Tree | str) -> tuple[Token, list] | str:
        """
            Converts a Lark Tree into a nested structure using Token StrEnum
            values.
        """

        if not isinstance(node, Tree):
            return str(node)

        token = Token[node.data]

        children = [self.invoke(c) for c in node.children]

        return (token, children)
