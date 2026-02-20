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

"""Inspector."""


from biz.dfch.ste100parser.token_map import TokenMap

from .char import Char
from .doc import Doc
from .string_builder import StringBuilder

from .serializer.token_base import EmptyToken
from .serializer.token_base import ListToken
from .serializer.token_base import TokenBase
from .serializer.token_base import ValueToken


class Inspector:
    """Inspect STE100 token trees."""

    _indent: int
    _delimiter: str

    def __init__(self, indent: int = 1, delimiter: str = ". ") -> None:
        assert isinstance(indent, int), type(indent)
        assert 0 <= indent, indent
        assert isinstance(delimiter, str), type(delimiter)
        assert 0 < len(delimiter), len(delimiter)

        self._indent = indent
        self._delimiter = delimiter

    def ste100doc(self, doc: Doc, token_map: TokenMap | None = None) -> str:
        assert isinstance(doc, Doc), type(Doc)

        if isinstance(token_map, TokenMap):
            map_ = token_map
        else:
            map_ = TokenMap()

        def process(
            tokens: list[TokenBase],
            level: int,
            delimiter: str = Char.SPACE
        ) -> StringBuilder:

            assert isinstance(tokens, list), type(tokens)
            assert isinstance(level, int), type(level)
            assert 0 <= level, level
            assert isinstance(delimiter, str), type(delimiter)
            assert 0 < len(delimiter), len(delimiter)

            result = StringBuilder()

            leading_indent: str = (level * self._indent) * delimiter
            count_ = len(tokens)
            for i, t in enumerate(tokens):
                if isinstance(t, (EmptyToken, ValueToken)):
                    result.append_line(
                        f"[{level:02}:{count_:02}:{i:02}]{leading_indent}"
                        f"'{t.text}' [{type(t).__name__}] "
                        f"[id:{map_[t]:02}]"
                        f"[p:{map_[t.parent]:02}] "
                    )
                    continue

                if isinstance(t, ListToken):
                    result.append_line(
                        f"[{level:02}:{count_:02}:{i:02}]{leading_indent}"
                        f"[{type(t).__name__}] "
                        f"[id:{map_[t]:02}]"
                        f"[p:{map_[t.parent]:02}] "
                        f"[#{len(t.tokens)}]"
                    )
                    result.extend(process(t.tokens, level + 1, delimiter))
                    continue
            return result

        result = StringBuilder()
        result.append_line("[level:count:idx]")

        tokens = list(doc)
        result.extend(process(tokens, 0, self._delimiter))

        return result.to_string()
