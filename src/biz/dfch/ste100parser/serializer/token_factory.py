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

from lark.tree import Meta

from .span import Span

from .token_base import TokenBase

from .token_base import Apostrophe
from .token_base import Text
from .token_base import Word
from .token_base import Number
from .token_base import Char
from .token_base import Punct
from .token_base import Ws
from .token_base import Plural
from .token_base import Multiply
from .token_base import LineBreak

from .token_base import Format
from .token_base import FormatType

from .token_base import Code
from .token_base import CodeBlock

from .token_base import NoteOrSafetyInstruction
from .token_base import NoteOrSafetyKeyword

from .token_base import TokenRoot
from .token_base import Heading
from .token_base import Paragraph
from .token_base import Sentence
from .token_base import ProcItem
from .token_base import ListItem

from .token_base import Parentheses

from .token_base import Quote
from .token_base import QuoteType


def from_lark_meta(meta) -> Span:
    assert hasattr(meta, "line")
    assert hasattr(meta, "column")
    assert hasattr(meta, "start_pos")
    assert hasattr(meta, "end_pos")

    result = Span(
        line=int(meta.line),
        column=int(meta.column),
        start_pos=int(meta.start_pos),
        end_pos=int(meta.end_pos),
    )

    return result


class TokenFactory:
    """Create a token instance."""

    @staticmethod
    def ProcItem(
        meta: Meta,
        parent: TokenBase,
        tokens: list[TokenBase],
        step: str,
        delimiter: str,
    ):
        return ProcItem(from_lark_meta(meta), parent, tokens, step, delimiter)

    @staticmethod
    def ListItem(
        meta: Meta,
        parent: TokenBase,
        tokens: list[TokenBase],
        indent: int,
        marker: str,
    ):
        return ListItem(from_lark_meta(meta), parent, tokens, indent, marker)

    @staticmethod
    def TokenRoot(
        meta: Meta,
        tokens: list[TokenBase],
    ):
        return TokenRoot(from_lark_meta(meta), None, tokens)  # type: ignore

    @staticmethod
    def Paragraph(
        meta: Meta,
        parent: TokenBase,
        tokens: list[TokenBase],
    ):
        return Paragraph(from_lark_meta(meta), parent, tokens)

    @staticmethod
    def NoteOrSafetyInstruction(
        meta: Meta,
        parent: TokenBase,
        tokens: list[TokenBase],
        keyword: NoteOrSafetyKeyword,
    ):
        return NoteOrSafetyInstruction(
            from_lark_meta(meta), parent, tokens, keyword)

    @staticmethod
    def Heading(
        meta: Meta,
        parent: TokenBase,
        tokens: list[TokenBase],
        level: int,
    ):
        return Heading(from_lark_meta(meta), parent, tokens, level)

    @staticmethod
    def Squote(
        meta: Meta,
        parent: TokenBase,
        tokens: list[TokenBase],
    ):
        return Quote(from_lark_meta(meta), parent, tokens, QuoteType.SINGLE)

    @staticmethod
    def Sentence(
        meta: Meta,
        parent: TokenBase,
        tokens: list[TokenBase],
    ):
        return Sentence(from_lark_meta(meta), parent, tokens)

    @staticmethod
    def Dquote(
        meta: Meta,
        parent: TokenBase,
        tokens: list[TokenBase],
    ):
        return Quote(from_lark_meta(meta), parent, tokens, QuoteType.DOUBLE)

    @staticmethod
    def Cite(
        meta: Meta,
        parent: TokenBase,
        tokens: list[TokenBase],
    ):
        return Quote(from_lark_meta(meta), parent, tokens, QuoteType.CITE)

    @staticmethod
    def Bold(
        meta: Meta,
        parent: TokenBase,
        tokens: list[TokenBase],
    ):
        return Format(from_lark_meta(meta), parent, tokens, FormatType.BOLD)

    @staticmethod
    def Emph(
        meta: Meta,
        parent: TokenBase,
        tokens: list[TokenBase],
    ):
        return Format(from_lark_meta(meta), parent, tokens, FormatType.EMPH)

    @staticmethod
    def BoldEmph(
        meta: Meta,
        parent: TokenBase,
        tokens: list[TokenBase],
    ):
        return Format(
            from_lark_meta(meta), parent, tokens, FormatType.BOLD_EMPH)

    @staticmethod
    def Parentheses(
        meta: Meta,
        parent: TokenBase,
        tokens: list[TokenBase],
    ):
        return Parentheses(from_lark_meta(meta), parent, tokens)

    @staticmethod
    def Text(
        meta: Meta,
        parent: TokenBase,
        value: str,
    ):
        return Text(from_lark_meta(meta), parent, value)

    @staticmethod
    def Char(
        meta: Meta,
        parent: TokenBase,
        value: str,
    ):
        return Char(from_lark_meta(meta), parent, value)

    @staticmethod
    def Word(
        meta: Meta,
        parent: TokenBase,
        value: str,
    ):
        return Word(from_lark_meta(meta), parent, value)

    @staticmethod
    def Number(
        meta: Meta,
        parent: TokenBase,
        value: str,
    ):
        return Number(from_lark_meta(meta), parent, value)

    @staticmethod
    def Punct(
        meta: Meta,
        parent: TokenBase,
        value: str,
    ):
        return Punct(from_lark_meta(meta), parent, value)

    @staticmethod
    def Ws(
        meta: Meta,
        parent: TokenBase,
        value: str,
    ):
        return Ws(from_lark_meta(meta), parent, value)

    @staticmethod
    def Apostrophe(
        meta: Meta,
        parent: TokenBase,
        value: str,
    ):
        return Apostrophe(from_lark_meta(meta), parent, value)

    @staticmethod
    def Plural(
        meta: Meta,
        parent: TokenBase,
    ):
        return Plural(from_lark_meta(meta), parent)

    @staticmethod
    def Multiply(
        meta: Meta,
        parent: TokenBase,
    ):
        return Multiply(from_lark_meta(meta), parent)

    @staticmethod
    def LineBreak(
        meta: Meta,
        parent: TokenBase,
    ):
        return LineBreak(from_lark_meta(meta), parent)

    @staticmethod
    def Code(
        meta: Meta,
        parent: TokenBase,
        value: str,
    ):
        return Code(from_lark_meta(meta), parent, value)

    @staticmethod
    def CodeBlock(
        meta: Meta,
        parent: TokenBase,
        value: str,
        language: str,
    ):
        return CodeBlock(from_lark_meta(meta), parent, value, language)
