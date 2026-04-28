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

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum

from ..char import Char as Character
from ..note_or_safety_keyword import NoteOrSafetyKeyword
from ..string_builder import StringBuilder

from .span import Span


@dataclass
class TokenBase(ABC):
    """
    This is an abstract base token. It represents the smallest unit of language
        syntax in a document.

    Attributes:
        span (Span): The location and length of this token within its context
            or container.
        parent (TokenBase): The parent token of this token.

    Args:
        text (str): A string representation of the `Span`.
            This is used to get the actual text represented by the token, which
            may be different from the span itself in some cases.
    """

    span: Span
    parent: TokenBase

    @property
    @abstractmethod
    def token_info(self) -> list[TokenInfo]:
        pass

    @property
    @abstractmethod
    def text(self) -> str:
        pass


@dataclass
class EmptyToken(TokenBase):
    """This is a token with a constant value."""


@dataclass
class ValueToken(TokenBase):
    """This is a token with a string value."""

    value: str

    @property
    def token_info(self) -> list[TokenInfo]:
        return [TokenInfo(
            text=self.text,
            token=self,
        )]

    @property
    def text(self) -> str:
        return self.value


@dataclass
class ListToken(TokenBase):
    """This is a token with a list of tokens."""

    tokens: list[TokenBase]

    @property
    def token_info(self) -> list[TokenInfo]:
        raise NotImplementedError(f"token_info: [{type(self).__name__}]")

    @property
    def text(self) -> str:
        sb = StringBuilder()
        for token in self.tokens:
            assert isinstance(token, TokenBase)
            sb.append(token.text)

        return sb.to_string()


@dataclass
class TokenRoot(ListToken):
    """This is the start token."""


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


@dataclass
class TokenInfo:
    """This class contains text with its related
    token, if there is one."""
    text: str
    token: TokenBase | None


@dataclass
class Sentence(ListToken):
    """This is a sentence in an ASD-STE100 text."""

    @property
    def token_info(self) -> list[TokenInfo]:
        result: list[TokenInfo] = []

        count: int = -1
        for token in self.tokens:
            assert isinstance(token, TokenBase)
            count += 1
            if isinstance(token, Ws):
                result.append(TokenInfo(
                    text=Character.SPACE,
                    token=token,
                ))
                continue

            if isinstance(token, (Text, Punct)):
                result.append(TokenInfo(
                    text=token.text,
                    token=token,
                ))
                continue

            if isinstance(token, Parentheses):
                result.append(TokenInfo(
                    text=Character.PAREN_OPEN,
                    token=None,
                ))
                result.append(TokenInfo(
                    text=Character.PAREN_CLOSE,
                    token=None,
                ))
                continue

            if isinstance(token, Quote):
                if QuoteType.DOUBLE == token.type_:
                    result.append(TokenInfo(
                        text=Character.DQUOTE,
                        token=None,
                    ))
                elif QuoteType.SINGLE == token.type_:
                    result.append(TokenInfo(
                        text=Character.SQUOTE,
                        token=None,
                    ))

                for t in token.tokens:
                    result.extend(t.token_info)

                if QuoteType.DOUBLE == token.type_:
                    result.append(TokenInfo(
                        text=Character.SQUOTE,
                        token=None,
                    ))
                elif QuoteType.SINGLE == token.type_:
                    result.append(TokenInfo(
                        text=Character.DQUOTE,
                        token=None,
                    ))
                continue

        return result

    @property
    def text(self) -> str:
        sb = StringBuilder()
        for token in self.tokens:
            assert isinstance(token, TokenBase)
            if isinstance(token, Ws):
                sb.append(Character.SPACE)
                continue
            if isinstance(token, (Text, Punct)):
                sb.append(token.text)
                continue
            if isinstance(token, Parentheses):
                sb.append(Character.PAREN_OPEN)
                sb.append(Character.PAREN_CLOSE)
                continue
            if isinstance(token, Quote):
                if QuoteType.DOUBLE == token.type_:
                    sb.append(Character.DQUOTE)
                elif QuoteType.SINGLE == token.type_:
                    sb.append(Character.SQUOTE)
                for t in token.tokens:
                    sb.append(t.text)
                if QuoteType.DOUBLE == token.type_:
                    sb.append(Character.DQUOTE)
                elif QuoteType.SINGLE == token.type_:
                    sb.append(Character.SQUOTE)
                continue

        return sb.to_string()


class QuoteType(StrEnum):
    """Define available quote types."""
    SINGLE = "SINGLE"
    DOUBLE = "DOUBLE"
    CITE = "CITE"


@dataclass
class Quote(ListToken):
    """This is a quote token."""

    type_: QuoteType

    @property
    def token_info(self) -> list[TokenInfo]:
        result: list[TokenInfo] = []
        for t in self.tokens:
            if isinstance(t, Parentheses):
                result.append(TokenInfo(
                    text=Character.PAREN_OPEN,
                    token=None,
                ))
                result.append(TokenInfo(
                    text=Character.PAREN_CLOSE,
                    token=None,
                ))
                continue
            result.extend(t.token_info)
        return result


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
        return Character.SPACE

    @property
    def token_info(self) -> list[TokenInfo]:
        return [TokenInfo(
            text=Character.LF,
            token=self,
        )]

@dataclass
class Text(ValueToken):
    """This is a text token."""


@dataclass
class SpecialText(Text):
    """This is a base class for special text tokens."""


@dataclass
class Multiply(SpecialText):
    """This is a multiply token."""

    @property
    def text(self) -> str:
        return f"{Character.SPACE}{Character.MULTIPLY}{Character.SPACE}"


@dataclass
class Plural(SpecialText):
    """This is a plural 's' token."""

    @property
    def text(self) -> str:
        result = (
            f"{Character.PAREN_OPEN}"
            f"{Character.CHAR_LOWER_S}"
            f"{Character.PAREN_CLOSE}"
        )
        return result


@dataclass
class Number(Text):
    """This is a number token."""


@dataclass
class Char(SpecialText):
    """This is a character token."""


@dataclass
class Apostrophe(SpecialText):
    """This is an apostrophe token."""

    @property
    def text(self) -> str:
        result = f"{Character.SQUOTE}{self.value}"
        return result


@dataclass
class Word(Text):
    """This is a word token."""


@dataclass
class Punct(ValueToken):
    """This is a punctuation token."""


@dataclass
class Code(ValueToken):
    """This is a code token."""


@dataclass
class CodeBlock(ValueToken):
    """This is a code block token."""

    language: str


@dataclass
class Ws(ValueToken):
    """This is a normalized whitespace token."""
