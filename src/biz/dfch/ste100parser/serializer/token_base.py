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

"""TokenBase and derived classes."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from ..char import Char
from ..note_or_safety_keyword import NoteOrSafetyKeyword
from ..string_builder import StringBuilder

from .span import Span


@dataclass
class TokenBase:
    """This is an abstract base token."""
    span: Span

    @property
    def text(self) -> str:
        return str(self.span)


@dataclass
class EmptyToken(TokenBase):
    """This is a token with a constant value."""


@dataclass
class ValueToken(TokenBase):
    """This is a token with a string value."""

    value: str

    @property
    def text(self) -> str:
        return self.value


@dataclass
class ListToken(TokenBase):
    """This is a token with a list of tokens."""

    tokens: list[TokenBase]

    @property
    def text(self) -> str:
        sb = StringBuilder()
        for token in self.tokens:
            assert isinstance(token, TokenBase)
            sb.append(token.text)

        return sb.to_string()


@dataclass
class ProcItem(ListToken):
    """This is a work step in a procedure."""
    step: str
    delimiter: str


@dataclass
class ListItem(ListToken):
    """This is a list item."""
    indent: int
    marker: str


@dataclass
class NoteOrSafetyInstruction(ListToken):
    """This is a keyword in a Note or Safety Instruction."""
    keyword: NoteOrSafetyKeyword


@dataclass
class Paragraph(ListToken):
    """This is a paragraph in a descriptive text."""


class QuoteType(StrEnum):
    """Define available quote types."""
    SINGLE = "SINGLE"
    DOUBLE = "DOUBLE"
    CITE = "CITE"


@dataclass
class Quote(ListToken):
    """This is a quote token."""

    type_: QuoteType


class FormatType(StrEnum):
    """Define available format types."""
    BOLD = "BOLD"
    EMPH = "EMPH"
    BOLD_EMPH = "BOLD_EMPH"


@dataclass
class Format(ListToken):
    """This is a format token."""

    type_: FormatType


@dataclass
class Parentheses(ListToken):
    """This is a quote token."""


@dataclass
class Heading(ListToken):
    """This is a heading token."""

    level: int


@dataclass
class LineBreak(EmptyToken):
    """This is a linebreak token."""

    @property
    def text(self) -> str:
        return Char.SPACE


@dataclass
class Multiply(EmptyToken):
    """This is a multiply token."""

    @property
    def text(self) -> str:
        return f"{Char.SPACE}{Char.MULTIPLY}{Char.SPACE}"


@dataclass
class Plural(EmptyToken):
    """This is a plural 's' token."""

    @property
    def text(self) -> str:
        result = f"{Char.PAREN_OPEN}{Char.CHAR_LOWER_S}{Char.PAREN_CLOSE}"
        return result


@dataclass
class Text(ValueToken):
    """This is a text token."""


@dataclass
class Code(ValueToken):
    """This is a code token."""


@dataclass
class CodeBlock(ValueToken):
    """This is a code block token."""

    language: str


@dataclass
class WhiteSpace(ValueToken):
    """This is a normalized whitespace token."""


@dataclass
class Apostrophe(ValueToken):
    """This is an apostrophe token."""

    @property
    def text(self) -> str:
        result = f"{Char.SQUOTE}{self.value}"
        return result
