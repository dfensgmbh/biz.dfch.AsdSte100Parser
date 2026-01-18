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

"""structure_transformer"""

import sys

from lark import lexer, Tree, Discard

from ..char import Char
from ..token import Token

from .transformer_base import TransformerBase


class StructureTransformer(TransformerBase):
    """StructureTransformer"""

    def _process_token_pair(
        self,
        children,
        token: Token,
        start: Char,
        end: Char | None = None,
    ):
        assert isinstance(children, list), children
        assert 3 <= len(children), len(children)

        first, *mid, last = children

        self.print(children, token.name)

        if end is None:
            end = start
        assert isinstance(first, str) and start == first
        assert isinstance(last, str) and end == last

        result = Tree(token.name, mid)
        self._metrics.append(token)

        return result

    def _process_empty_token_pair(
        self,
        children,
        token: Token,
        start: Char,
        end: Char | None = None,
    ):
        assert isinstance(children, list), children
        assert 2 <= len(children), len(children)

        first, *mid, last = children
        if 2 == len(children):
            mid = Char.EMPTY

        self.print(children, token.name)

        if end is None:
            end = start
        assert isinstance(first, str) and start == first, first
        assert isinstance(last, str) and end == last, last

        result = Tree(token.name, mid)
        self._metrics.append(token)

        return result

    def start(self, children):
        """start"""

        assert isinstance(children, list) and 1 <= len(children)

        method_name = sys._getframe(0).f_code.co_name
        self.print(children, method_name)

        result = Tree(method_name, children)
        self._metrics.append(Token.start)

        return result

    def bold(self, children):
        return self._process_token_pair(children, Token.bold, Char.STAR)

    def emph(self, children):
        return self._process_token_pair(children, Token.emph, Char.UNDER)

    def bold_emph(self, children):
        return self._process_token_pair(
            children,
            Token.bold_emph,
            Char.BOLD_EMPH_OPEN,
            Char.BOLD_EMPH_CLOSE
        )

    def code(self, children):
        assert isinstance(children, list)
        assert 3 == len(children), len(children)

        first, mid, last = children

        token = Token.CODE
        self.print(children, token.name)

        assert isinstance(first, str) and Char.CODE == first
        assert isinstance(last, str) and Char.CODE == last

        result = Tree(token.name, mid.value)
        self._metrics.append(token)

        return result

    def dquote(self, children):
        return self._process_token_pair(children, Token.dquote, Char.DQUOTE)

    def squote(self, children):
        return self._process_token_pair(children, Token.squote, Char.SQUOTE)

    def paren(self, children):
        return self._process_empty_token_pair(
            children, Token.paren, Char.PAREN_OPEN, Char.PAREN_CLOSE)

    def paren_sl(self, children):
        """Single line parentheses change to standard parentheses."""
        return self._process_empty_token_pair(
            children, Token.paren, Char.PAREN_OPEN, Char.PAREN_CLOSE)

    def cite(self, children):
        assert isinstance(children, list)
        assert 1 <= len(children), len(children)

        return children

    def cite_first_line(self, children):
        assert isinstance(children, list)
        assert 2 <= len(children), len(children)

        token = Token.cite

        _, *mid = children

        self.print(children, token.name)

        tokens: list = []
        tokens.extend(mid)

        result = Tree(token.name, mid)
        self._metrics.append(token)

        return result

    def cite_cont_line(self, children):
        return self.cite_first_line(children)

    def NEWLINE(self, children):  # pylint: disable=C0103
        assert isinstance(children, lexer.Token)
        assert 1 <= len(children)

        token = Token.NEWLINE

        self.print(children, token.name)

        result = Tree(token.name, Char.LF)
        self._metrics.append(token)

        return result

    def WS(self, children):  # pylint: disable=C0103
        assert isinstance(children, lexer.Token)
        assert 1 <= len(children)

        token = Token.WS

        self.print(children, token.name)

        result = Tree(token.name, Char.SPACE * len(children))
        self._metrics.append(token)

        return result

    def MULTIPLY(self, children):  # pylint: disable=C0103
        assert isinstance(children, lexer.Token)
        assert 1 <= len(children)

        token = Token.MULTIPLY

        self.print(children, token.name)

        result = Tree(token.name, f" {Char.MULTIPLY} ")
        self._metrics.append(token)

        return result

    def char_paren_open(self, children):
        return self._process_char(children)

    def char_paren_close(self, children):
        return self._process_char(children)

    def char_star(self, children):
        return self._process_char(children)

    def char_under(self, children):
        return self._process_char(children)

    def char_code(self, children):
        return self._process_char(children)

    def _process_char(self, children):
        assert isinstance(children, list)
        assert 1 == len(children), children

        token = Token.CHAR

        self.print(children, token.name)

        result = Tree(token.name, children)
        self._metrics.append(token)

        return result

    def proc_indent_prefix(self, children):
        _ = children

        # Remove the token from the tree.
        return Discard

    def proc_indent_suffix(self, children):
        _ = children

        # Remove the token from the tree.
        return Discard

    def proc(self, children):
        assert isinstance(children, list), children
        assert 1 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.proc

        self.print(children, token.name)

        items = children

        result = Tree(token.name, items)
        self._metrics.append(token)

        return result

    def proc_marker(self, children):
        assert isinstance(children, list), children
        assert 1 <= len(children), f"#{len(children)}: [{children}]."

        return str(children[0])

    def proc_delimiter(self, children):
        assert isinstance(children, list), children
        assert 1 <= len(children), f"#{len(children)}: [{children}]."

        return str(children[0])

    def proc_first_line(self, children):
        return self._process_proc_line(children)

    def proc_next_line(self, children):
        assert isinstance(children, list), children
        assert 4 <= len(children), f"#{len(children)}: [{children}]."

        return self._process_proc_line(children[1:])

    def _process_proc_line(self, children):
        assert isinstance(children, list), children
        assert 3 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.proc_item

        self.print(children, token.name)

        step, delimiter, *remaining = children

        items = [
            Tree(Token.PROC_STEP.name, step),
            Tree(Token.PROC_DELIMITER.name, delimiter),
            *remaining
        ]
        result = Tree(token.name, items)
        self._metrics.append(token)

        return result

    def TEXT(self, children):  # pylint: disable=C0103
        assert isinstance(children, lexer.Token)
        assert 1 <= len(children)

        token = Token.TEXT

        self.print(children, token.name)

        result = Tree(token.name, str(children))
        self._metrics.append(token)

        return result

    def APOSTROPHE(self, children):  # pylint: disable=C0103
        assert isinstance(children, lexer.Token)
        assert 2 >= len(children)

        token = Token.APOSTROPHE

        *_, last = children
        self.print(last, token.name)

        assert isinstance(last, str)
        assert last in (Char.SQUOTE, Char.CHAR_LOWER_S)

        if Char.SQUOTE == last:
            last = Char.EMPTY

        result = Tree(token.name, last)
        self._metrics.append(token)

        return result
