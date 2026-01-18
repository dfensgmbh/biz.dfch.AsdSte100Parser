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
# pylint: disable=W0212
# type: ignore

"""TokenMetrics class."""

from biz.dfch.ste100parser import Token


class TokenMetrics:
    """TokenMetrics"""

    _values: list[Token]

    def __init__(self) -> None:
        self._values = []

    def pop(
        self,
        index: int = -1,
        default_value: Token | None = None,
    ) -> Token | None:
        """
        Remove and return item at index (default last).

        Returns `default_value` if list is empty or index is out of range.
        """
        try:
            return self._values.pop(index)
        except IndexError:
            return default_value

    def __iter__(self):
        return iter(self._values)

    def __len__(self):
        """
        Docstring for __len__

        :param self: Description
        """
        return len(self._values)

    def __getitem__(self, token: Token) -> int:
        """
        Docstring for __getitem__

        :param self: Description
        :param token: Description
        :type token: Token
        :return: Description
        :rtype: int
        """
        return self._values.count(token)

    def clear(self) -> None:
        self._values.clear()

    def append(self, token: Token) -> None:

        assert isinstance(token, Token)

        self._values.append(token)

    def __str__(self):
        return str(self._values)

    def __repr__(self) -> str:
        return self.__str__()
