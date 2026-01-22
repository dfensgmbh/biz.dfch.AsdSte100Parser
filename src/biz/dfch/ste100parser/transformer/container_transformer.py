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

"""container_transformer"""

from lark import lexer, Tree, Discard

from ..char import Char
from ..token import Token

from .transformer_base import TransformerBase

__all__ = [
    "ContainerTransformer",
]


class ContainerTransformerRules:
    """
    Rules for ContainerTransformer start.

    These rules removed NEWLINE between different rules.
    """
    rules = [
        (
            [Token.NEWLINE, Token.NEWLINE, Token.heading],
            lambda n1, n2, h: h,
            True,
        ),
        (
            [Token.NEWLINE, Token.cite],
            lambda n, c: c,
            True,
        ),
        (
            [Token.NEWLINE, Token.heading],
            lambda n, h: h,
            True,
        ),
        (
            [Token.NEWLINE, Token.NEWLINE, Token.paragraph],
            lambda n1, n2, p: p,
            True,
        ),
        (
            [Token.heading, Token.NEWLINE],
            lambda h, n1: h,
            True,
        ),
        (
            [Token.cite, Token.NEWLINE],
            lambda c, n1: c,
            True,
        ),
        (
            [Token.proc_item, Token.NEWLINE, Token.NEWLINE, Token.paragraph],  # noqa: E501
            lambda proc, n1, n2, para: [proc, para],
            False,
        ),
        (
            [Token.proc_item, Token.NEWLINE, Token.NOTE],
            lambda proc, n, note: [proc, note],
            False,
        ),
        (
            [Token.proc_item, Token.NEWLINE, Token.paragraph],
            lambda proc, n, para: [proc, para],
            False,
        ),
        (
            [Token.paragraph, Token.NEWLINE, Token.proc_item],
            lambda para, n, proc: [para, proc],  # noqa: E501
            True,
        ),
        (
            [Token.paragraph, Token.NEWLINE, Token.paragraph],
            lambda a, n, b: Tree(Token.paragraph.name, a.children + b.children),  # noqa: E501
            True,
        ),
        (
            [Token.paragraph, Token.paragraph],
            lambda a, b: Tree(Token.paragraph.name, a.children + b.children),  # noqa: E501
            False,
        ),
    ]


class ContainerTransformer(TransformerBase):  # pylint: disable=R0904
    """Transformer for pass 1."""

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

        result = Tree(token.name, [mid.value])

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

        token = Token.cite

        items = []
        for line in children:
            items.extend(line)

        result = Tree(token.name, items)
        return result

    def cite_line(self, children):
        assert isinstance(children, list)
        assert 2 <= len(children), len(children)

        token = Token.cite

        _, *mid = children

        self.print(children, token.name)

        result = mid
        return result

    def NEWLINE(self, children):  # pylint: disable=C0103
        assert isinstance(children, lexer.Token)
        assert 1 <= len(children)

        token = Token.NEWLINE

        self.print(children, token.name)

        result = Tree(token.name, [Char.LF])
        return result

    def WS(self, children):  # pylint: disable=C0103
        assert isinstance(children, lexer.Token)
        assert 1 <= len(children)

        token = Token.WS

        self.print(children, token.name)

        result = Tree(token.name, [str(len(children))])
        return result

    def MULTIPLY(self, children):  # pylint: disable=C0103
        assert isinstance(children, lexer.Token)
        assert 1 <= len(children)

        token = Token.MULTIPLY

        self.print(children, token.name)

        result = Tree(token.name, [f" {Char.MULTIPLY} "])
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

        value = children[0]
        result = Tree(token.name, [value])
        return result

    def proc_indent_prefix(self, children):
        _ = children

        # Remove the token from the tree.
        return Discard

    def proc_indent_suffix(self, children):
        _ = children

        # Remove the token from the tree.
        return Discard

    def PROC_MARKER(self, children):  # pylint: disable=C0103
        assert isinstance(children, lexer.Token), type(children)
        assert 1 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.PROC_STEP

        self.print(children, token.name)

        items = [str(children)]
        result = Tree(token.name, items)
        return result

    def PROC_DELIMITER(self, children):  # pylint: disable=C0103
        assert isinstance(children, lexer.Token), type(children)
        assert 1 == len(children), f"#{len(children)}: [{children}]."

        token = Token.PROC_DELIMITER

        self.print(children, token.name)

        items = [str(children)]
        result = Tree(token.name, items)
        return result

    def PROC_LINE_START(self, children):  # pylint: disable=C0103
        assert isinstance(children, lexer.Token), type(children)
        assert 1 == len(children), f"#{len(children)}: [{children}]."

        return Discard

    def proc_line(self, children):
        assert isinstance(children, list), children
        assert 4 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.proc_item

        self.print(children, token.name)

        item = children[0]
        assert isinstance(item, Tree)
        assert Token.PROC_STEP.name == item.data

        step, delimiter, _, *remaining = children

        items = [
            step,
            delimiter,
            *remaining
        ]
        result = Tree(token.name, items)
        return result

    def TEXT(self, children):  # pylint: disable=C0103
        assert isinstance(children, lexer.Token), type(children)
        assert 1 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.TEXT

        self.print(children, token.name)

        result = Tree(token.name, [str(children)])
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

        result = Tree(token.name, [last])
        return result

    def heading_marker_suffix(self, children):
        _ = children

        # Remove the token from the tree.
        return Discard

    def HEADING_MARKER(self, children):  # pylint: disable=C0103
        assert isinstance(children, lexer.Token)
        assert 1 <= len(children)

        token = Token.HEADING_LEVEL

        self.print(children, token.name)

        result = Tree(token.name, [str(len(children))])
        return result

    def _process_heading_line(self, children):
        assert isinstance(children, list), children
        assert 2 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.heading

        self.print(children, token.name)

        level, _, *remaining = children

        items = [
            level,
            *remaining
        ]
        result = Tree(token.name, items)
        return result

    def heading_first_line(self, children):
        assert isinstance(children, list), children
        assert 2 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.heading

        self.print(children, token.name)

        return self._process_heading_line(children)

    def heading_next_line(self, children):
        assert isinstance(children, list), children
        assert 2 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.heading

        self.print(children, token.name)

        return self._process_heading_line(children)

    def heading(self, children):
        assert isinstance(children, list), children
        assert 1 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.heading

        self.print(children, token.name)

        items = []
        for item in children:
            items.extend(item.children)

        result = Tree(token.name, items)
        return result

    def SPACE(self, children):  # pylint: disable=C0103
        assert isinstance(children, lexer.Token), children
        assert 1 == len(children), f"#{len(children)}: [{children}]."

        token = Token.SPACE

        self.print(children, token.name)

        items = children[0]

        result = Tree(token.name, [items])
        return result

    def SINGLE_NEWLINE(self, children):  # pylint: disable=C0103
        assert isinstance(children, lexer.Token), children
        assert 1 == len(children), f"#{len(children)}: [{children}]."

        token = Token.LINEBREAK

        self.print(children, token.name)

        items = children[0]

        result = Tree(token.name, [items])
        return result

    def paragraph(self, children):
        assert isinstance(children, list), children
        assert 1 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.paragraph

        self.print(children, token.name)

        if (
            children and
            isinstance(children[-1], Tree) and
            Token.LINEBREAK.name == children[-1].data
        ):
            children = children[:-1]

        items = children

        result = Tree(token.name, items)
        return result

    def list_line(self, children):
        assert isinstance(children, list), children
        assert 3 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.list_item

        self.print(children, token.name)

        item = children[0]
        if isinstance(item, lexer.Token) and "LIST_LINE_START" == item.type:
            children = children[1:]

        item = children[0]
        assert isinstance(item, Tree) and Token.WS.name == item.data
        indent = Tree(Token.LIST_INDENT.name, item.children[0])
        children = children[1:]

        self.print(children, token.name)

        marker_token = children.pop(0)
        assert isinstance(marker_token, lexer.Token)
        marker = Tree(Token.LIST_MARKER.name, [marker_token.value])

        space_token = children.pop(0)
        assert isinstance(space_token, Tree)
        assert Token.SPACE.name == space_token.data

        items = [
            marker,
            indent,
            *children
        ]

        result = Tree(token.name, items)
        return result

    def _rewrite_children(self, children: list, rules: list) -> list:
        """Rewrites the children based ony rules."""

        assert isinstance(children, list)
        assert isinstance(rules, list)

        i = 0
        while i < len(children):
            for pattern, replacer, do_again in rules:
                pattern_length = len(pattern)

                if i + pattern_length > len(children):
                    continue

                segment = children[i:i + pattern_length]

                if all(
                    isinstance(node, Tree) and token.name == node.data
                    for node, token in zip(segment, pattern)
                ):
                    new_segment = replacer(*segment)
                    if isinstance(new_segment, list):
                        children[i:i + pattern_length] = new_segment
                        # new_segment_length = len(new_segment)
                    else:
                        children[i:i + pattern_length] = [new_segment]
                        # new_segment_length = 1

                    if not do_again:
                        i += 1
                    break
            else:
                i += 1

        return children

    def start(self, children):
        """start"""

        assert isinstance(children, list), children
        assert 1 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.start

        self.print(children, token.name)

        rules = ContainerTransformerRules().rules
        children = self._rewrite_children(children, rules)
        self.print(children, token.name)

        result = Tree(token.name, children)
        return result

    def note(self, children):
        return self._process_note_or_safety(Token.NOTE, children)

    def warning(self, children):
        return self._process_note_or_safety(Token.WARNING, children)

    def caution(self, children):
        return self._process_note_or_safety(Token.CAUTION, children)

    def _process_note_or_safety(self, token: Token, children):
        assert isinstance(token, Token)
        assert token in (Token.NOTE, Token.WARNING, Token.CAUTION)
        assert isinstance(children, list), children
        assert 3 <= len(children), f"#{len(children)}: [{children}]."

        self.print(children, token.name)

        item = children.pop(0)
        assert lexer.Token == type(item), item
        assert "NOTE_OR_SAFETY_LINE_START" == item.type

        marker = children.pop(0)
        assert Tree == type(marker), marker
        assert marker.data in (
            "note_marker", "warning_marker", "caution_marker")

        result = Tree(token.name, children)
        return result
