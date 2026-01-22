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

# pylint: disable=W0212

"""ContainerSerializer class."""

import sys

from biz.dfch.ste100parser.char import Char
from biz.dfch.ste100parser.transformer.transformer_base import TransformerBase


class ContainerSerializer(TransformerBase):
    """ContainerSerializer"""

    def bold(self, children):
        """Insert STAR."""

        assert isinstance(children, list)
        assert 0 < len(children)

        method_name = sys._getframe(0).f_code.co_name
        self.print(children, f"{self.__class__.__name__}-{method_name}")

        result = f"{Char.STAR}{Char.EMPTY.join(children)}{Char.STAR}"

        return result

    def emph(self, children):
        """Insert UNDER."""

        assert isinstance(children, list)
        assert 0 < len(children)

        method_name = sys._getframe(0).f_code.co_name
        self.print(children, f"{self.__class__.__name__}-{method_name}")

        result = f"{Char.UNDER}{Char.EMPTY.join(children)}{Char.UNDER}"

        return result

    def bold_emph(self, children):
        """Insert BOLD_EMPH_OPEN/BOLD_EMPH_CLOSE."""

        assert isinstance(children, list)
        assert 0 < len(children)

        method_name = sys._getframe(0).f_code.co_name
        self.print(children, f"{self.__class__.__name__}-{method_name}")

        result = (
            f"{Char.BOLD_EMPH_OPEN}"
            f"{Char.EMPTY.join(children)}"
            f"{Char.BOLD_EMPH_CLOSE}"
        )

        return result

    def WS(self, children):  # pylint: disable=C0103
        """Insert DQUOTE."""

        # assert isinstance(children, list)
        # assert 0 < len(children)

        method_name = sys._getframe(0).f_code.co_name
        self.print(children, f"{self.__class__.__name__}-{method_name}")

        result = f"{Char.SPACE}{Char.EMPTY.join(children)}{Char.SPACE}"

        return result

    def dquote(self, children):
        """Insert DQUOTE."""

        assert isinstance(children, list)
        assert 0 < len(children)

        method_name = sys._getframe(0).f_code.co_name
        self.print(children, f"{self.__class__.__name__}-{method_name}")

        result = f"{Char.DQUOTE}{Char.EMPTY.join(children)}{Char.DQUOTE}"

        return result

    def squote(self, children):
        """Insert SQUOTE."""

        assert isinstance(children, list)
        assert 0 < len(children)

        method_name = sys._getframe(0).f_code.co_name
        self.print(children, f"{self.__class__.__name__}-{method_name}")

        result = f"{Char.SQUOTE}{Char.EMPTY.join(children)}{Char.SQUOTE}"

        return result
