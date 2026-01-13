# Copyright (C) 2026 Ronald Rink, d-fens GmbH
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

"""containers_transformer"""

from lark import Tree

from ..char import Char
from .transformer_base import TransformerBase


class ContainersTransformer(TransformerBase):
    """ContainersTransformer"""

    def dquote(self, children):
        """Remove trailing double quotes from token."""

        assert isinstance(children, list) and 3 <= len(children)
        first, *mid, last = children

        self.print(children, "dquote")

        assert isinstance(first, str) and Char.DQUOTE == first
        assert isinstance(last, str) and Char.DQUOTE == last

        result = Tree("dquote", mid)

        return result

    def squote(self, children):
        """Remove trailing single quotes from token."""

        assert isinstance(children, list) and 3 <= len(children)
        self.print(children, "squote")

        first, *mid, last = children

        assert isinstance(first, str) and Char.SQUOTE == first
        assert isinstance(last, str) and Char.SQUOTE == last

        result = Tree("squote", mid)

        return result
