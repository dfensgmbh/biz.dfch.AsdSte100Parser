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

"""ContainersRenderer class."""

from biz.dfch.ste100parser.char import Char
from biz.dfch.ste100parser.transformer.transformer_base import TransformerBase


class ContainersRenderer(TransformerBase):
    """ContainersRenderer"""

    def dquote(self, children):
        """dquote"""

        assert isinstance(children, list)
        assert 0 < len(children)

        self.print(children, "renderer dquote")

        result = f"{Char.DQUOTE}{Char.EMPTY.join(children)}{Char.DQUOTE}"

        return result

    def squote(self, children):
        """squote"""

        assert isinstance(children, list)
        assert 0 < len(children)

        self.print(children, "renderer squote")

        result = f"{Char.SQUOTE}{Char.EMPTY.join(children)}{Char.SQUOTE}"

        return result
