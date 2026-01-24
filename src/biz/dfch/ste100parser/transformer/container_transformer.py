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

from lark import Discard, lexer, Tree, v_args
from lark.tree import Meta

from biz.dfch.ste100parser.transformer.container_transformer_rules import (
    ContainerTransformerRules
)

from ..char import Char
from ..token import Token

from .transformer_base import TransformerBase

__all__ = [
    "ContainerTransformer",
]


class ContainerTransformer(TransformerBase):  # pylint: disable=R0904
    """Transformer for pass 1."""

    def _get_meta(self, node: lexer.Token) -> Meta:
        assert isinstance(node, lexer.Token)

        meta = Meta()
        meta.line = node.line
        meta.column = node.column
        meta.start_pos = node.start_pos
        meta.end_pos = getattr(
            node, 'end_pos',
            node.start_pos + len(node)
        )
        meta.end_line = getattr(node, 'end_line', node.line)
        meta.end_column = getattr(
            node, 'end_column',
            node.column + len(node)
        )

        return meta

    def _process_token_pair(
        self,
        children,
        token: str,
        meta: Meta,
        start: Char,
        end: Char | None = None,
    ):
        assert isinstance(children, list), children
        assert 3 <= len(children), len(children)
        assert isinstance(token, str)
        assert isinstance(meta, Meta)

        first, *mid, last = children

        self.print(children, token)

        if end is None:
            end = start
        assert isinstance(first, str) and start == first
        assert isinstance(last, str) and end == last

        result = Tree(token, mid, meta=meta)
        return result

    def _process_empty_token_pair(
        self,
        children,
        token: str,
        meta: Meta,
        start: Char,
        end: Char | None = None,
    ):
        assert isinstance(children, list), children
        assert 2 <= len(children), len(children)
        assert isinstance(token, str)
        assert isinstance(meta, Meta)

        first, *mid, last = children
        if 2 == len(children):
            mid = Char.EMPTY

        self.print(children, token)

        if end is None:
            end = start
        assert isinstance(first, str) and start == first, first
        assert isinstance(last, str) and end == last, last

        result = Tree(token, mid, meta=meta)
        return result

    @v_args(meta=True)
    def bold(self, meta, children):
        return self._process_token_pair(
            children,
            Token.bold.name,
            meta,
            Char.STAR
        )

    @v_args(meta=True)
    def emph(self, meta, children):
        return self._process_token_pair(
            children,
            Token.emph.name,
            meta,
            Char.UNDER
        )

    @v_args(meta=True)
    def bold_emph(self, meta, children):
        return self._process_token_pair(
            children,
            Token.bold_emph.name,
            meta,
            Char.BOLD_EMPH_OPEN,
            Char.BOLD_EMPH_CLOSE
        )

    @v_args(meta=True)
    def code(self, meta, children):
        assert isinstance(children, list)
        assert 3 == len(children), len(children)

        first, mid, last = children

        token = Token.CODE.name
        self.print(children, token)

        assert isinstance(first, str) and Char.CODE == first
        assert isinstance(last, str) and Char.CODE == last

        result = Tree(token, [mid.value], meta=meta)

        return result

    @v_args(meta=True)
    def dquote(self, meta, children):
        return self._process_token_pair(
            children,
            Token.dquote.name,
            meta,
            Char.DQUOTE
        )

    @v_args(meta=True)
    def squote(self, meta, children):
        return self._process_token_pair(
            children,
            Token.squote.name,
            meta,
            Char.SQUOTE
        )

    @v_args(meta=True)
    def paren(self, meta, children):
        return self._process_empty_token_pair(
            children, Token.paren.name, meta, Char.PAREN_OPEN, Char.PAREN_CLOSE)

    @v_args(meta=True)
    def paren_sl(self, meta, children):
        """Single line parentheses change to standard parentheses."""
        return self._process_empty_token_pair(
            children, Token.paren.name, meta, Char.PAREN_OPEN, Char.PAREN_CLOSE)

    @v_args(meta=True)
    def cite(self, meta, children):
        assert isinstance(children, list)
        assert 1 <= len(children), len(children)

        token = Token.cite.name

        items = []
        for line in children:
            items.extend(line)

        result = Tree(token, items, meta=meta)
        return result

    def cite_line(self, children):
        assert isinstance(children, list)
        assert 2 <= len(children), len(children)

        token = Token.cite.name

        _, *mid = children

        self.print(children, token)

        result = mid
        return result

    def NEWLINE(self, children):  # pylint: disable=C0103
        assert isinstance(children, lexer.Token)
        assert 1 <= len(children)

        token = Token.NEWLINE.name

        self.print(children, token)

        meta = self._get_meta(children)
        result = Tree(token, [Char.LF], meta=meta)
        return result

    def WS(self, children):  # pylint: disable=C0103
        assert isinstance(children, lexer.Token)
        assert 1 <= len(children)

        token = Token.WS.name

        self.print(children, token)

        meta = self._get_meta(children)
        result = Tree(token, [str(len(children))], meta=meta)
        return result

    def MULTIPLY(self, children):  # pylint: disable=C0103
        assert isinstance(children, lexer.Token)
        assert 1 <= len(children)

        token = Token.MULTIPLY.name

        self.print(children, token)

        meta = self._get_meta(children)
        result = Tree(token, [f" {Char.MULTIPLY} "], meta=meta)
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

        token = Token.CHAR.name

        self.print(children, token)

        value = children[0]
        meta = self._get_meta(value)
        result = Tree(token, [value], meta=meta)
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

        token = Token.PROC_STEP.name

        self.print(children, token)

        items = [str(children)]
        meta = self._get_meta(children)
        result = Tree(token, items, meta=meta)
        return result

    def PROC_DELIMITER(self, children):  # pylint: disable=C0103
        assert isinstance(children, lexer.Token), type(children)
        assert 1 == len(children), f"#{len(children)}: [{children}]."

        token = Token.PROC_DELIMITER.name

        self.print(children, token)

        items = [str(children)]
        meta = self._get_meta(children)
        result = Tree(token, items, meta=meta)
        return result

    def PROC_LINE_START(self, children):  # pylint: disable=C0103
        assert isinstance(children, lexer.Token), type(children)
        assert 1 == len(children), f"#{len(children)}: [{children}]."

        return Discard

    @v_args(meta=True)
    def proc_line(self, meta, children):
        assert isinstance(children, list), children
        assert 4 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.proc_item.name

        self.print(children, token)

        item = children[0]
        assert isinstance(item, Tree)
        assert Token.PROC_STEP.name == item.data

        step, delimiter, _, *remaining = children

        items = [
            step,
            delimiter,
            *remaining
        ]
        proc_item_meta = Meta()
        proc_item_meta.line = step.meta.line
        proc_item_meta.column = step.meta.column
        proc_item_meta.start_pos = step.meta.start_pos
        proc_item_meta.end_pos = meta.end_pos
        result = Tree(token, items, meta=proc_item_meta)
        return result

    def TEXT(self, children):  # pylint: disable=C0103
        assert isinstance(children, lexer.Token), type(children)
        assert 1 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.TEXT.name

        self.print(children, token)

        meta = self._get_meta(children)
        result = Tree(token, [str(children)], meta=meta)
        return result

    def APOSTROPHE(self, children):  # pylint: disable=C0103
        assert isinstance(children, lexer.Token)
        assert 2 >= len(children)

        token = Token.APOSTROPHE.name

        *_, last = children
        self.print(last, token)

        assert isinstance(last, str)
        assert last in (Char.SQUOTE, Char.CHAR_LOWER_S)

        if Char.SQUOTE == last:
            last = Char.EMPTY

        meta = self._get_meta(children)
        result = Tree(token, [last], meta=meta)
        return result

    def heading_marker_suffix(self, children):
        _ = children

        # Remove the token from the tree.
        return Discard

    def HEADING_MARKER(self, children):  # pylint: disable=C0103
        assert isinstance(children, lexer.Token)
        assert 1 <= len(children)

        token = Token.HEADING_LEVEL.name

        self.print(children, token)

        meta = self._get_meta(children)
        result = Tree(token, [str(len(children))], meta=meta)
        return result

    def _process_heading_line(self, children):
        assert isinstance(children, list), children
        assert 2 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.heading.name

        self.print(children, token)

        level, _, *remaining = children

        items = [
            level,
            *remaining
        ]
        result = Tree(token, items)
        return result

    def heading_first_line(self, children):
        assert isinstance(children, list), children
        assert 2 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.heading.name

        self.print(children, token)

        return self._process_heading_line(children)

    def heading_next_line(self, children):
        assert isinstance(children, list), children
        assert 2 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.heading.name

        self.print(children, token)

        return self._process_heading_line(children)

    @v_args(meta=True)
    def heading(self, meta, children):
        assert isinstance(children, list), children
        assert 1 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.heading.name

        self.print(children, token)

        items = []
        for item in children:
            items.extend(item.children)

        result = Tree(token, items, meta=meta)
        return result

    def SPACE(self, children):  # pylint: disable=C0103
        assert isinstance(children, lexer.Token), children
        assert 1 == len(children), f"#{len(children)}: [{children}]."

        token = Token.SPACE.name

        self.print(children, token)

        items = children[0]

        meta = self._get_meta(children)
        result = Tree(token, [items], meta=meta)
        return result

    def SINGLE_NEWLINE(self, children):  # pylint: disable=C0103
        assert isinstance(children, lexer.Token), children
        assert 1 == len(children), f"#{len(children)}: [{children}]."

        token = Token.LINEBREAK.name

        self.print(children, token)

        items = children[0]

        meta = self._get_meta(children)
        result = Tree(token, [items], meta=meta)
        return result

    @v_args(meta=True)
    def paragraph(self, meta, children):
        assert isinstance(children, list), children
        assert 1 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.paragraph.name

        self.print(children, token)

        if (
            children and
            isinstance(children[-1], Tree) and
            Token.LINEBREAK.name == children[-1].data
        ):
            children = children[:-1]

        items = children

        result = Tree(token, items, meta=meta)
        return result

    @v_args(meta=True)
    def list_line(self, meta, children):
        assert isinstance(children, list), children
        assert 3 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.list_item.name

        self.print(children, token)

        item = children[0]
        if isinstance(item, lexer.Token) and "LIST_LINE_START" == item.type:
            children = children[1:]

        item = children[0]
        assert isinstance(item, Tree) and Token.WS.name == item.data
        indent = Tree(Token.LIST_INDENT.name, item.children[0], meta=item.meta)
        children = children[1:]

        self.print(children, token)

        marker_token = children.pop(0)
        assert isinstance(marker_token, lexer.Token)
        marker_meta = self._get_meta(marker_token)
        marker = Tree(Token.LIST_MARKER.name, [
                      marker_token.value], meta=marker_meta)

        space_token = children.pop(0)
        assert isinstance(space_token, Tree)
        assert Token.SPACE.name == space_token.data

        items = [
            indent,
            marker,
            *children
        ]

        list_line_meta = Meta()
        list_line_meta.line = indent.meta.line
        list_line_meta.column = indent.meta.column
        list_line_meta.start_pos = indent.meta.start_pos
        list_line_meta.end_pos = meta.end_pos
        result = Tree(token, items, meta=list_line_meta)
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
                    else:
                        children[i:i + pattern_length] = [new_segment]

                    if not do_again:
                        i += 1
                    break
            else:
                i += 1

        return children

    @v_args(meta=True)
    def start(self, meta, children):
        """start"""

        assert isinstance(children, list), children
        assert 1 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.start.name

        self.print(children, token)

        rules = ContainerTransformerRules().get_rules()
        children = self._rewrite_children(children, rules)
        self.print(children, token)

        result = Tree(token, children, meta=meta)
        return result

    @v_args(meta=True)
    def note(self, meta, children):
        return self._process_note_or_safety(Token.NOTE.name, children, meta)

    @v_args(meta=True)
    def warning(self, meta, children):
        return self._process_note_or_safety(Token.WARNING.name, children, meta)

    @v_args(meta=True)
    def caution(self, meta, children):
        return self._process_note_or_safety(Token.CAUTION.name, children, meta)

    def _process_note_or_safety(self, token: str, children, meta):
        assert isinstance(token, str)
        assert token in (
            Token.NOTE.name,
            Token.WARNING.name,
            Token.CAUTION.name
        )
        assert isinstance(children, list), children
        assert 3 <= len(children), f"#{len(children)}: [{children}]."
        assert isinstance(meta, Meta)

        self.print(children, token)

        item = children.pop(0)
        assert lexer.Token == type(item), item
        assert "NOTE_OR_SAFETY_LINE_START" == item.type

        marker = children.pop(0)
        assert Tree == type(marker), marker
        assert marker.data in (
            "note_marker", "warning_marker", "caution_marker")

        item_meta = Meta()
        item_meta.line = meta.line + 1
        item_meta.column = 1
        item_meta.start_pos = meta.start_pos + 1
        item_meta.end_pos = meta.end_pos
        result = Tree(token, children, meta=item_meta)
        return result
