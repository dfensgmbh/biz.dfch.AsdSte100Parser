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

"""ste100_serializer class."""

from __future__ import annotations

from typing import Callable

from lark import Tree
from lark.tree import Meta

from ..ste100doc import Ste100Doc as Ste100DDoc
from ..token import Token

from .span import Span
from .token_base import TokenBase
from .token_base import TokenRoot
from .token_base import EmptyToken
from .token_base import ListToken
from .token_base import ValueToken
from .token_base import Sentence
from .token_base import Heading
from .token_base import Paragraph
from .token_base import NoteOrSafetyInstruction

from .token_base import Parentheses
from .token_base import Format
from .token_base import FormatType
from .token_base import Quote
from .token_base import QuoteType
from .token_base import Code

from .token_base import Text
from .token_base import Word
from .token_base import Number
from .token_base import Punct
from .token_base import Ws
from .token_base import LineBreak

_map = Callable[[TokenBase], Tree]


def from_span(span: Span) -> Meta:
    result = Meta()

    result.line = span.line
    result.column = span.column
    result.start_pos = span.start_pos
    result.end_pos = span.end_pos

    return result


class Ste100Serializer:
    """Change a Ste100 document into a lark tree."""

    _start_token: str

    @staticmethod
    def list_token(token: TokenBase) -> Tree:
        assert isinstance(token, ListToken), type(token)

        token_name = Ste100Serializer._func_map[type(token)][1]

        print(f"{token_name}: '{token.text}' [{type(token).__name__}]")

        children = Ste100Serializer._visit(token.tokens)

        result = Tree(token_name, children, from_span(token.span))

        return result

    @staticmethod
    def heading(token: TokenBase) -> Tree:
        assert isinstance(token, Heading), type(token)

        items: list[Tree] = [
            Tree(Token.HEADING_LEVEL, [str(token.level)]),
        ]

        token_name = Ste100Serializer._func_map[type(token)][1]

        print(f"{token_name}: '{token.text}' [{type(token).__name__}]")

        children = Ste100Serializer._visit(token.tokens)
        items.extend(children)

        result = Tree(token_name, items, from_span(token.span))

        return result

    @staticmethod
    def format(token: TokenBase) -> Tree:
        assert isinstance(token, Format), type(token)

        token_name_map: dict[FormatType, Token] = {
            FormatType.BOLD: Token.bold,
            FormatType.EMPH: Token.emph,
            FormatType.BOLD_EMPH: Token.bold_emph,
        }
        token_name = token_name_map[token.type_]

        print(f"{token_name}: '{token.text}' [{type(token).__name__}]")

        children = Ste100Serializer._visit(token.tokens)

        result = Tree(token_name, children, from_span(token.span))

        return result

    @staticmethod
    def quote(token: TokenBase) -> Tree:
        assert isinstance(token, Quote), type(token)

        token_name_map: dict[QuoteType, Token] = {
            QuoteType.SINGLE: Token.squote,
            QuoteType.DOUBLE: Token.dquote,
            QuoteType.CITE: Token.cite,
        }
        token_name = token_name_map[token.type_]

        print(f"{token_name}: '{token.text}' [{type(token).__name__}]")

        children = Ste100Serializer._visit(token.tokens)

        result = Tree(token_name, children, from_span(token.span))

        return result

    @staticmethod
    def parentheses(token: TokenBase) -> Tree:
        assert isinstance(token, Parentheses), type(token)

        token_name = Ste100Serializer._func_map[type(token)][1]

        print(f"{token_name}: '{token.text}' [{type(token).__name__}]")

        children = Ste100Serializer._visit(token.tokens)

        result = Tree(token_name, children, from_span(token.span))

        return result

    @staticmethod
    def text(token: TokenBase) -> Tree:

        token_name = Ste100Serializer._func_map[type(token)][1]

        print(f"{token_name}: '{token.text}' [{type(token).__name__}]")

        result = Tree(token_name, [token.text], from_span(token.span))

        return result

    @staticmethod
    def code(token: TokenBase) -> Tree:

        token_name = Ste100Serializer._func_map[type(token)][1]

        print(f"{token_name}: '{token.text}' [{type(token).__name__}]")

        result = Tree(token_name, [token.text], from_span(token.span))

        return result

    @staticmethod
    def ws(token: TokenBase) -> Tree:
        assert isinstance(token, ValueToken), type(token)
        assert not token.text.strip(), token.text

        token_name = Ste100Serializer._func_map[type(token)][1]

        print(f"{token_name}: '{token.text}' [{type(token).__name__}]")

        result = Tree(token_name, [str(len(token.text))], from_span(token.span))

        return result

    @staticmethod
    def line_break(token: TokenBase) -> Tree:
        assert isinstance(token, EmptyToken), type(token)

        token_name = Ste100Serializer._func_map[type(token)][1]

        print(f"{token_name}: '{token.text}' [{type(token).__name__}]")

        result = Tree(token_name, [str(len(token.text))], from_span(token.span))

        return result

    _func_map: dict[type, tuple[_map, str]] = {
        TokenRoot: (list_token, Token.start.name),
        Sentence: (list_token, Token.sentence.name),
        Heading: (heading, Token.heading.name),
        Paragraph: (list_token, Token.paragraph.name),
        Parentheses: (list_token, Token.paren.name),
        NoteOrSafetyInstruction: (list_token, Token.NOTE.name),

        Format: (format, Token.default.name),
        Quote: (quote, Token.default.name),
        Code: (code, Token.CODE.name),

        Text: (text, Token.TEXT.name),
        Word: (text, Token.TEXT.name),
        Number: (text, Token.TEXT.name),
        Ws: (ws, Token.WS.name),
        LineBreak: (line_break, Token.LINEBREAK.name),
        Punct: (text, Token.TEXT.name),
    }

    def __init__(
        self,
        start_token_name: str = Token.start.name,
    ) -> None:
        assert isinstance(start_token_name, str), type(start_token_name)
        assert start_token_name.strip()

        self._start_token = start_token_name

    @staticmethod
    def _visit(tokens: list[TokenBase]) -> list[Tree]:
        assert isinstance(tokens, list), type(tokens)

        result: list[Tree] = []
        for token in tokens:
            assert isinstance(token, TokenBase), type(token)

            func = Ste100Serializer._func_map[type(token)][0]
            result.append(func(token))

        return result

    def to_lark_tree(self, doc: Ste100DDoc) -> list[Tree]:
        """
        Change the document into the lark tree.

        :param doc: The ASD STE100 document.
        :type doc: Ste100DDoc
        :return: The lark tree.
        :rtype: Tree[Any]
        """

        assert isinstance(doc, Ste100DDoc), type(doc)
        assert 0 < len(doc), len(doc)

        children = self._visit(list(doc))
        print(children)
        assert 0 < len(children), len(children)
        root = children[0]
        assert isinstance(root, Tree), type(root)

        meta = from_span(Span.default())
        result = Tree(root.data, children=root.children, meta=meta)

        return children
