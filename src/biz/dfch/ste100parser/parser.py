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

"""TestMain"""

from pathlib import Path

from lark import Lark, ParseTree

from .grammar.grammar_type import GrammarType


class Parser:
    """Parser class."""

    _lark: Lark
    _grammar: GrammarType

    def __init__(self, grammar: GrammarType = GrammarType.DEFAULT):
        """Default .ctor."""

        assert isinstance(grammar, GrammarType) and grammar.strip()

        self._grammar = grammar

        path = Path("grammar") / grammar
        self._lark = Lark.open(
            path.as_posix(),
            rel_to=__file__,
            propagate_positions=True,
        )  # type: ignore

    def is_valid(self, text: str) -> bool:
        """Returns True, if the text is valid. False, otherwise."""

        try:
            self.invoke(text)

            return True
        except Exception:  # pylint: disable=W0718
            return False

    def invoke(self, text: str) -> ParseTree:
        """Invokes the parser."""

        assert isinstance(text, str) and text.strip()

        result = self._lark.parse(text)  # type: ignore

        return result
