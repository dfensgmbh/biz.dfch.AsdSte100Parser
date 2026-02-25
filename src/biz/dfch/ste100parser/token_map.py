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

"""TokenMap."""

from itertools import count

from .serializer.token_base import TokenBase


class TokenMap:
    """A token to id map.

    This map creates a consecutive id for each unique STE100 token.
    """

    NONE_IDX = -1
    _id_gen: count
    _map: dict[int, int]

    def __init__(self) -> None:
        self._id_gen = count(self.NONE_IDX)
        self._map = {}
        # The first entry in the token map is:
        # id(None) : -1
        self._map[id(None)] = next(self._id_gen)

    def contains(self, token: TokenBase) -> bool:
        if token is None:
            return True

        assert isinstance(token, TokenBase), type(token)

        return id(token) in self._map

    def __getitem__(self, token: TokenBase) -> int:
        return self.get(token)

    def get(self, token: TokenBase | None) -> int:
        if token is None:
            return self.NONE_IDX

        assert isinstance(token, TokenBase), type(token)

        key = id(token)
        idx = self._map.get(key)
        if idx is not None:
            return idx

        idx = next(self._id_gen)
        self._map[key] = idx

        return idx
