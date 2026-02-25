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

# pylint: disable=C0103
# pylint: disable=C0116
# pylint: disable=W0212

"""StringBuilder class."""

from __future__ import annotations

from .char import Char


class StringBuilder:
    """A simple StringBuilder object for fast string add operations."""

    _new_line: str
    _items: list[str]

    def __init__(
        self,
        new_line: str = Char.LF
    ) -> None:

        assert isinstance(new_line, str)

        self._items = []
        self._new_line = new_line

    def append(self, value: str = Char.EMPTY) -> StringBuilder:
        """
        Add text to the StringBuilder object. This does not add a new line.
        """

        assert isinstance(value, str)

        self._items.append(value)

        return self

    def append_line(self, value: str = Char.EMPTY) -> StringBuilder:
        """
        Add text to the StringBuilder object. This does add a new line.
        """

        self.append(value)
        self.append(self._new_line)

        return self

    def extend(self, other: StringBuilder) -> StringBuilder:
        """
        Add one StringBuilder instance to this StringBuilder instance.

        :param other: The other instance that adds to this instance.
        :type other: StringBuilder
        :return: This instance.
        :rtype: StringBuilder
        """

        assert isinstance(other, StringBuilder), type(other)

        self._items.extend(other._items)
        return self

    def to_string(self) -> str:
        """Returns the string representation of the object."""

        return Char.EMPTY.join(self._items)

    def __str__(self) -> str:
        """Return the string representation of the object."""
        return self.to_string()

    def __repr__(self) -> str:
        """Return the string representation of the object."""
        return self.to_string()
