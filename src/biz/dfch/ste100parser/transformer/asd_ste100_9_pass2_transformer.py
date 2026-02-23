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

"""asd_ste100_9_pass2_transformer"""

from lark import Tree, v_args

from ..token import Token
from ..serializer.sentencizer import Sentencizer

from .asd_ste100_9_pass2_transformer_rules import (
    AsdSte1009Pass2TransformerRules
)
from .transformer_base import TransformerBase
from .transformer_configuration import TransformerConfiguration
from .tree_rewriter import TreeRewriter

__all__ = [
    "AsdSte1009Pass2Transformer",
]


class AsdSte1009Pass2Transformer(TransformerBase):  # pylint: disable=R0904
    """Transformer for pass 2.

    This transformer creates theses tokens from TEXT:
      * WORD
      * ABBREV
      * PUNCT
    From these, the transformer creates sentences inside a paragraph.
    """

    _sentencizer: Sentencizer

    def __init__(
        self,
        cfg: TransformerConfiguration = TransformerConfiguration(
            log=False,
        ),
    ) -> None:

        assert isinstance(cfg, TransformerConfiguration)

        super().__init__(cfg)

        self._sentencizer = Sentencizer()

    @v_args(meta=True)
    def start(self, meta, children):
        """start"""

        assert isinstance(children, list), children
        assert 1 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.start.name

        self.print(children, token)

        rules = AsdSte1009Pass2TransformerRules().get_rules_start()
        children = TreeRewriter().invoke(children, rules)
        self.print(children, token)

        result = Tree(token, children, meta=meta)
        return result

    @v_args(meta=True)
    def heading(self, meta, children):
        assert isinstance(children, list), type(children)
        assert 1 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.heading.name

        level, *remaining = children
        trees = self._sentencizer.invoke(remaining, meta=meta)
        items = [level, *trees]
        result = Tree(token, items, meta=meta)
        return result

    @v_args(meta=True)
    def proc_item(self, meta, children):
        assert isinstance(children, list), type(children)
        assert 1 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.proc_item.name

        step, delimiter, *remaining = children
        items = [step, delimiter]
        trees = self.get_sentences(remaining, meta=meta)
        items.extend(trees)

        result = Tree(token, items, meta=meta)
        return result

    @v_args(meta=True)
    def list_item(self, meta, children):
        assert isinstance(children, list), type(children)
        assert 1 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.list_item.name

        indent, marker, *remaining = children
        trees = self._sentencizer.invoke(remaining, meta)
        items = [indent, marker, *trees]
        result = Tree(token, items, meta=meta)
        return result

    @v_args(meta=True)
    def NOTE(self, meta, children):  # pylint: disable=C0103
        return self._process_note_or_safety_instruction(
            meta=meta,
            children=children,
            token=Token.NOTE.name,
        )

    @v_args(meta=True)
    def WARNING(self, meta, children):  # pylint: disable=C0103
        return self._process_note_or_safety_instruction(
            meta=meta,
            children=children,
            token=Token.WARNING.name,
        )

    @v_args(meta=True)
    def CAUTION(self, meta, children):  # pylint: disable=C0103
        return self._process_note_or_safety_instruction(
            meta=meta,
            children=children,
            token=Token.CAUTION.name,
        )

    def _process_note_or_safety_instruction(self, meta, children, token: str):
        assert isinstance(children, list), type(children)
        assert 1 <= len(children), f"#{len(children)}: [{children}]."

        trees = self._sentencizer.invoke(children, meta)
        for tree in trees:
            print(tree.pretty())
        items = [*trees]
        result = Tree(token, items, meta=meta)
        return result

    @v_args(meta=True)
    def paren(self, meta, children):
        assert isinstance(children, list), type(children)
        assert 1 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.paren.name

        trees = self._sentencizer.invoke(children, meta)
        items = [*trees]

        result = Tree(token, items, meta=meta)
        return result

    @v_args(meta=True)
    def cite(self, meta, children):
        assert isinstance(children, list), type(children)
        assert 1 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.cite.name

        trees = self._sentencizer.invoke(children, meta)
        items = [*trees]

        result = Tree(token, items, meta=meta)
        return result

    @v_args(meta=True)
    def dquote(self, meta, children):
        assert isinstance(children, list), type(children)
        assert 1 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.dquote.name

        items = children
        result = Tree(token, items, meta=meta)
        return result

    @v_args(meta=True)
    def squote(self, meta, children):
        assert isinstance(children, list), type(children)
        assert 1 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.squote.name

        items = children
        result = Tree(token, items, meta=meta)
        return result

    def get_sentences(self, tokens: list[Tree], meta) -> list[Tree]:
        special_tokens: list[str] = [
            Token.list_item.name,
            Token.NOTE.name,
            Token.WARNING.name,
            Token.CAUTION.name
        ]

        result: list[Tree] = []
        chunk: list[Tree] = []
        for item in tokens:
            assert isinstance(item, Tree), type(item)
            if item.data not in special_tokens:
                chunk.append(item)
                continue

            if chunk:
                trees = self._sentencizer.invoke(children=chunk, meta=meta)
                chunk.clear()
                result.extend(trees)
            result.append(item)

        if chunk:
            trees = self._sentencizer.invoke(children=chunk, meta=meta)
            chunk.clear()
            result.extend(trees)

        return result

    @v_args(meta=True)
    def paragraph(self, meta, children):
        assert isinstance(children, list), type(children)
        assert 1 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.paragraph.name

        items = []
        trees = self.get_sentences(children, meta=meta)
        items.extend(trees)

        result = Tree(token, items, meta=meta)
        return result
