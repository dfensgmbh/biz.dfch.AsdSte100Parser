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

from enum import auto, Enum
from pathlib import Path

from lark import Lark, ParseTree

from .grammar.grammar_type import GrammarType
from .transformer import AsdSte1009Pass1Transformer
from .transformer import AsdSte1009Pass2Transformer


class ParserAction(Enum):
    """Define parser action."""
    PARSE = auto()
    PASS1 = auto()
    PASS2 = auto()
    DEFAULT = PARSE


class Parser:
    """Parser class."""

    _lark: Lark
    _grammar: GrammarType
    _pass1_transformer: AsdSte1009Pass1Transformer
    _pass2_transformer: AsdSte1009Pass2Transformer

    def __init__(
        self,
        grammar: GrammarType = GrammarType.DEFAULT
    ):
        """Initializes a `Parser` instance with the specified `GrammarType`."""

        assert isinstance(grammar, GrammarType), type(grammar)
        assert grammar.strip()

        self._grammar = grammar
        self._pass1_transformer = AsdSte1009Pass1Transformer()
        self._pass2_transformer = AsdSte1009Pass2Transformer()

        path = Path("grammar") / grammar
        self._lark = Lark.open(
            path.as_posix(),
            rel_to=__file__,
            propagate_positions=True,
        )  # type: ignore

    def is_valid(self, text: str) -> bool:
        """
        Returns True, if the text is grammatically valid.
        False, otherwise.
        """

        try:
            self.invoke(text)

            return True
        except Exception:  # pylint: disable=W0718
            return False

    def invoke(
        self,
        text: str,
        *,
        action: ParserAction = ParserAction.DEFAULT,
    ) -> ParseTree:
        """
        Parses the text based on the specified grammar.

        Args:
            text (str): The text to parse.
            action (ParserAction): See `ParseAction` for details.

        Returns:
            result (ParseTree): The `ParseTree` from `text`.
        """

        assert isinstance(text, str), type(text)
        assert text.strip()
        assert isinstance(action, ParserAction), type(action)

        result = self._lark.parse(text)  # type: ignore

        if GrammarType.ASD_STE100_9 != self._grammar:
            return result

        if ParserAction.PARSE == action:
            return result

        pass1 = self._pass1_transformer.transform(result)
        if ParserAction.PASS1 == action:
            return pass1

        pass2 = self._pass2_transformer.transform(pass1)
        if ParserAction.PASS2 == action:
            return pass2

        result = pass2
        return result
