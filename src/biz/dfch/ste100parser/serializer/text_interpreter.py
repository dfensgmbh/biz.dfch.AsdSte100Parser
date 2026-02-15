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

"""TextInterpreter class."""

from __future__ import annotations

from lark import Tree
from lark.visitors import Interpreter

from ..char import Char
from ..note_or_safety_keyword import NoteOrSafetyKeyword

from .token_base import TokenBase
from .token_factory import TokenFactory
from .token_factory import from_lark_meta


class TextInterpreter(Interpreter):  # pylint: disable=R0904
    """This moves through the tree from top to bottom."""

    def start(self, tree) -> list:
        assert isinstance(tree, Tree), type(tree)

        print(f"start: [{tree.data}].")

        print(f"{[type(t) for t in tree.children]}")

        result = self.visit_children(tree)

        return ["start", result]

    def flatten_result(self, items: list) -> list:
        assert isinstance(items, list), type(items)

        result: list[TokenBase] = []

        for item in items:
            assert isinstance(item, (list, TokenBase))
            if isinstance(item, list):
                assert 1 == len(item), len(item)
                nested_item = item[0]
                assert isinstance(nested_item, TokenBase), type(nested_item)
                result.append(nested_item)
            else:
                result.append(item)

        return result

    def TEXT(self, tree) -> list:
        assert isinstance(tree, Tree), type(tree)
        assert 1 == len(tree.children), len(tree.children)
        value = tree.children[0]
        assert isinstance(value, str), type(value)

        result = TokenFactory.Text(
            meta=tree.meta,
            value=value,
        )

        return [result]

    def APOSTROPHE(self, tree) -> list:
        assert isinstance(tree, Tree), type(tree)
        assert 1 == len(tree.children), len(tree.children)
        value = tree.children[0]
        assert isinstance(value, str), type(value)

        result = TokenFactory.Apostrophe(
            meta=tree.meta,
            value=value,
        )

        return [result]

    def WS(self, tree) -> list:
        assert isinstance(tree, Tree), type(tree)
        assert 1 == len(tree.children), len(tree.children)
        value = tree.children[0]
        assert isinstance(value, str), type(value)
        assert value.isdigit(), value

        result = TokenFactory.WhiteSpace(
            meta=tree.meta,
            value=int(value) * Char.SPACE,
        )

        return [result]

    def paragraph(self, tree) -> list:
        assert isinstance(tree, Tree), type(tree)

        result = TokenFactory.Paragraph(
            meta=tree.meta,
            tokens=self._get_items(tree.children),
        )

        return [result]

    def proc_item(self, tree) -> list:
        assert isinstance(tree, Tree), type(tree)

        step_tree, delimiter_tree, *remaining = tree.children

        assert isinstance(step_tree, Tree)
        assert 1 == len(step_tree.children)
        step = step_tree.children[0]
        assert isinstance(step, str)

        assert isinstance(delimiter_tree, Tree)
        assert 1 == len(delimiter_tree.children)
        delimiter = delimiter_tree.children[0]
        assert isinstance(delimiter, str)

        result = TokenFactory.ProcItem(
            meta=tree.meta,
            step=step,
            delimiter=delimiter,
            tokens=self._get_items(remaining),
        )

        return [result]

    def heading(self, tree) -> list:
        assert isinstance(tree, Tree), type(tree)

        level_tree, *remaining = tree.children

        assert isinstance(level_tree, Tree)
        assert 1 == len(level_tree.children)
        level = level_tree.children[0]
        assert isinstance(level, str), type(level)
        assert level.isdigit(), level

        result = TokenFactory.Heading(
            meta=tree.meta,
            level=int(level),
            tokens=self._get_items(remaining),
        )

        return [result]

    def list_item(self, tree) -> list:
        assert isinstance(tree, Tree), type(tree)

        indent_tree, marker_tree, *remaining = tree.children

        assert isinstance(indent_tree, Tree)
        assert 1 == len(indent_tree.children)
        indent = indent_tree.children[0]
        assert isinstance(indent, str)
        assert indent.isdigit(), indent

        assert isinstance(marker_tree, Tree)
        assert 1 == len(marker_tree.children)
        marker = marker_tree.children[0]
        assert isinstance(marker, str)
        assert marker.isalnum(), marker

        result = TokenFactory.ListItem(
            meta=tree.meta,
            tokens=self._get_items(remaining),
            indent=int(indent),
            marker=marker,
        )

        return [result]

    def WARNING(self, tree) -> list:
        return self._note_or_safety_instruction(
            tree, NoteOrSafetyKeyword.WARNING)

    def CAUTION(self, tree) -> list:
        return self._note_or_safety_instruction(
            tree, NoteOrSafetyKeyword.CAUTION)

    def NOTE(self, tree) -> list:
        return self._note_or_safety_instruction(
            tree, NoteOrSafetyKeyword.NOTE)

    def _note_or_safety_instruction(
        self,
        tree,
        keyword: NoteOrSafetyKeyword
    ) -> list:
        assert isinstance(tree, Tree), type(tree)
        assert isinstance(keyword, str), type(keyword)

        result = TokenFactory.NoteOrSafetyInstruction(
            meta=tree.meta,
            keyword=keyword,
            tokens=self._get_items(tree.children),
        )

        return [result]

    def _get_items(self, remaining: list) -> list[TokenBase]:

        assert isinstance(remaining, list)
        assert 0 < len(remaining), len(remaining)

        result = []
        for item in remaining:
            assert isinstance(item, Tree), type(item)
            visited = self.visit(item)
            if isinstance(visited, list):
                result.extend(visited)
            elif visited is not None:
                result.append(visited)

        return result

    def PLURAL_S(self, tree) -> list:
        assert isinstance(tree, Tree), type(tree)

        result = TokenFactory.Plural(
            meta=tree.meta,
        )

        return [result]

    def MULTIPLY(self, tree) -> list:
        assert isinstance(tree, Tree), type(tree)

        result = TokenFactory.Multiply(
            meta=tree.meta,
        )

        return [result]

    def LINEBREAK(self, tree) -> list:
        assert isinstance(tree, Tree), type(tree)

        result = TokenFactory.LineBreak(
            meta=tree.meta,
        )

        return [result]

    def NEWLINE(self, tree) -> list:
        assert isinstance(tree, Tree), type(tree)

        span = from_lark_meta(tree.meta)
        raise NotImplementedError(
            "LogicError: NEWLINE is not permitted at this point in text. "
            f"{span}"
        )

    def dquote(self, tree) -> list:
        assert isinstance(tree, Tree), type(tree)

        result = TokenFactory.Dquote(
            meta=tree.meta,
            tokens=self._get_items(tree.children)
        )

        return [result]

    def squote(self, tree) -> list:
        assert isinstance(tree, Tree), type(tree)

        result = TokenFactory.Squote(
            meta=tree.meta,
            tokens=self._get_items(tree.children)
        )

        return [result]

    def cite(self, tree) -> list:
        assert isinstance(tree, Tree), type(tree)

        result = TokenFactory.Cite(
            meta=tree.meta,
            tokens=self._get_items(tree.children)
        )

        return [result]

    def bold(self, tree) -> list:
        assert isinstance(tree, Tree), type(tree)

        result = TokenFactory.Bold(
            meta=tree.meta,
            tokens=self._get_items(tree.children)
        )

        return [result]

    def emph(self, tree) -> list:
        assert isinstance(tree, Tree), type(tree)

        result = TokenFactory.Emph(
            meta=tree.meta,
            tokens=self._get_items(tree.children)
        )

        return [result]

    def bold_emph(self, tree) -> list:
        assert isinstance(tree, Tree), type(tree)

        result = TokenFactory.BoldEmph(
            meta=tree.meta,
            tokens=self._get_items(tree.children)
        )

        return [result]

    def CODE(self, tree) -> list:
        assert isinstance(tree, Tree), type(tree)
        assert 1 == len(tree.children), len(tree.children)
        value = tree.children[0]
        assert isinstance(value, str), type(value)

        result = TokenFactory.Code(
            meta=tree.meta,
            value=value,
        )

        return [result]

    def code_block(self, tree) -> list:
        assert isinstance(tree, Tree), type(tree)
        assert 2 == len(tree.children), len(tree.children)

        language_tree = tree.children[0]
        assert isinstance(language_tree, Tree), type(language_tree)
        assert 1 == len(language_tree.children), len(language_tree.children)
        language = language_tree.children[0]
        assert isinstance(language, str)

        value_tree = tree.children[1]
        assert isinstance(value_tree, Tree), type(value_tree)
        assert 1 == len(value_tree.children), len(value_tree.children)
        value = value_tree.children[0]
        assert isinstance(value, str)

        result = TokenFactory.CodeBlock(
            meta=tree.meta,
            value=value,
            language=language,
        )

        return [result]

    def paren(self, tree) -> list:
        assert isinstance(tree, Tree), type(tree)

        result = TokenFactory.Parentheses(
            meta=tree.meta,
            tokens=self._get_items(tree.children)
        )

        return [result]

    def __default__(self, tree) -> list:
        assert isinstance(tree, Tree), type(tree)

        span = from_lark_meta(tree.meta)
        raise NotImplementedError(
            f"'{tree.data}' {span}"
        )
