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

"""text_transformer"""

from collections import deque

from lark import Tree, v_args
from lark.tree import Meta

from biz.dfch.ste100parser.transformer.transformer_base import TransformerBase

from biz.dfch.ste100parser.transformer.text_transformer_rules import (
    TextTransformerRules
)
from biz.dfch.ste100parser.transformer.tree_rewriter import TreeRewriter

from ..token import Token
from ..char import Char


class TextTransformer(TransformerBase):  # pylint: disable=R0904
    """Transformer for pass 2.

    This transformer creates theses tokens from TEXT:
      * WORD
      * ABBREV
      * PUNCT
    From these, the transformer creates sentences inside a paragraph.
    """

    @v_args(meta=True)
    def start(self, meta, children):
        """start"""

        assert isinstance(children, list), children
        assert 1 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.start.name

        self.print(children, token)

        rules = TextTransformerRules().get_rules_start()
        children = TreeRewriter().invoke(children, rules)
        self.print(children, token)

        result = Tree(token, children, meta=meta)
        return result

    @v_args(meta=True)
    def TEXT(self, meta, children):  # pylint: disable=C0103
        assert isinstance(children, list), type(children)
        assert 1 == len(children), f"#{len(children)}: [{children}]."

        _ = meta

        token = Token.TEXT.name

        value: str = children[0]
        assert isinstance(value, str)
        assert 0 < len(value)

        flattened = self.divide_text(meta, children)

        if 1 < len(flattened):
            token = Token.FLATTEN.name
            result = Tree(token, flattened, meta=meta)
            return result

        node = flattened[0]
        token = node.data
        result = Tree(token, [str(node.children[0])], meta=node.meta)
        return result

    @v_args(meta=True)
    def proc_item(self, meta, children):
        assert isinstance(children, list), type(children)
        assert 1 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.proc_item.name

        step, delimiter, *remaining = children
        items = [step, delimiter]
        processed_items = self.process_sentences(
            remaining,
            fill=True,
        )
        items.extend(processed_items)
        result = Tree(token, items, meta=meta)
        return result

    @v_args(meta=True)
    def list_item(self, meta, children):
        assert isinstance(children, list), type(children)
        assert 1 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.list_item.name

        indent, marker, *remaining = children
        items = [indent, marker]
        processed_items = self.process_sentences(
            remaining,
            fill=True,
        )
        items.extend(processed_items)
        result = Tree(token, items, meta=meta)
        return result

    @v_args(meta=True)
    def paren(self, meta, children):
        assert isinstance(children, list), type(children)
        assert 1 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.paren.name

        items = self.process_sentences(
            children,
            fill=True,
        )
        result = Tree(token, items, meta=meta)
        return result

    @v_args(meta=True)
    def cite(self, meta, children):
        assert isinstance(children, list), type(children)
        assert 1 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.cite.name

        items = self.process_sentences(
            children,
            fill=True,
        )
        result = Tree(token, items, meta=meta)
        return result

    @v_args(meta=True)
    def dquote(self, meta, children):
        assert isinstance(children, list), type(children)
        assert 1 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.dquote.name

        items = self.process_sentences(
            children,
            fill=False,
        )
        result = Tree(token, items, meta=meta)
        return result

    @v_args(meta=True)
    def squote(self, meta, children):
        assert isinstance(children, list), type(children)
        assert 1 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.squote.name

        items = self.process_sentences(
            children,
            fill=False,
        )
        result = Tree(token, items, meta=meta)
        return result

    @v_args(meta=True)
    def paragraph(self, meta, children):
        assert isinstance(children, list), type(children)
        assert 1 <= len(children), f"#{len(children)}: [{children}]."

        token = Token.paragraph.name

        items = self.process_sentences(
            children,
            fill=True,
            terminators=[Token.list_item],
        )
        result = Tree(token, items, meta=meta)
        return result

    def process_sentences(
        self,
        children: list[Tree],
        fill: bool,
        terminators: list[Token] | None = None,
    ) -> list[Tree]:

        flattened = self.flatten_text_nodes(children)
        sentences = self.get_sentences(
            flattened,
            fill=fill,
            terminators=terminators
        )
        return sentences

    def divide_text(self, meta, children) -> list[Tree]:
        """Divides a TEXT node into WORD and EOS nodes."""

        assert isinstance(children, list), type(children)
        assert 1 == len(children), f"#{len(children)}: [{children}]."
        assert isinstance(meta, Meta)

        result: list[Tree] = []

        value: str = children[0]
        assert isinstance(value, str)
        assert 0 < len(value)

        # 1. Rule
        # When the last character in Token.TEXT is a Char.COMMA,
        # we split Token.TEXT into Token.WORD and Token.COMMA.
        # Continue with rule (2).
        if value[-1] in (Char.COMMA):
            first = value[:-1]
            last = value[-1:]

            first_meta, last_meta = self.get_meta(meta, first, last)
            first_node = Tree(Token.TEXT.name, [first], meta=first_meta)
            last_node = Tree(Token.COMMA.name, [last], meta=last_meta)
            result.append(first_node)
            result.append(last_node)
        else:
            item = Tree(Token.TEXT.name, [value], meta=meta)
            result.append(item)

        # 2. Rule
        # When the last character in Token.TEXT is one of these characters:
        #   * Char.DOT
        #   * Char.COLON
        #   * Char.QUESTION
        #   * Char.EXCLAMATION.
        # We do a test, if Token.TEXT is in the dictionary. If it is in the
        # dictionary, we change Token.TEXT to Token.WORD.
        # We set the status on the result of this test.
        # If it is not in the dictionary, we split Token.TEXT into Token.TEXT
        # and Token.EOS.
        # Do this procedure again, until, there is no Token.TEXT.

        def is_text(node) -> bool:
            return Token.TEXT.name == getattr(node, "data", None)

        processed: list[Tree] = []
        work = deque(result)
        while work:

            node = work.popleft()

            if not is_text(node):
                processed.append(node)
                continue

            value: str = str(*node.children)
            assert isinstance(value, str)

            if 1 == len(value):
                if value in (
                    Char.DOT,
                    Char.COLON,
                    Char.QUESTION,
                    Char.EXCLAMATION
                ):
                    eos = Tree(Token.EOS.name, [value], meta=node.meta)
                    processed.append(eos)
                    continue

                if self.is_in_dictionary(value):
                    word = Tree(Token.WORD.name, [value], meta=node.meta)
                else:
                    word = Tree(Token.WORD.name, [value], meta=node.meta)
                processed.append(word)
                continue

            first_node = value[:-1]
            last_node = value[-1:]
            if last_node in (
                Char.DOT,
                Char.COLON,
                Char.QUESTION,
                Char.EXCLAMATION
            ):
                # We pretend: we found a word with trailing EOS
                # in the dictionary.
                if self.is_in_dictionary(value):
                    item1 = Tree(Token.WORD.name, [value], meta=node.meta)
                    processed.append(item1)
                    continue

                # We pretend: we did not find a word with trailing EOS
                # in the dictionary.
                item1_meta, item2_meta = self.get_meta(
                    meta, first_node, last_node)
                item1 = Tree(Token.TEXT.name, [first_node], meta=item1_meta)
                item2 = Tree(Token.EOS.name, [last_node], meta=item2_meta)
                work.appendleft(item2)
                work.appendleft(item1)
                continue

            # 3. rule
            # A Token.TEXT without trailing EOS.
            # Examine, if the word is in the dictionary.
            if self.is_in_dictionary(value):
                item1 = Tree(Token.WORD.name, [value], meta=node.meta)
                processed.append(item1)
                continue

            item1 = Tree(Token.WORD.name, [value], meta=node.meta)
            processed.append(item1)

        return processed

    def is_in_dictionary(self, value: str) -> bool:
        assert isinstance(value, str)
        assert 0 < len(value)

        result: bool = False
        if "X" == value[-1]:
            result = True

        return result

    def get_meta(self, meta: Meta, a: str, b: str) -> (Meta, Meta):
        assert isinstance(meta, Meta)
        assert isinstance(a, str) and a.strip()
        assert isinstance(b, str) and b.strip()

        a_meta = Meta()
        a_meta.line = meta.line
        a_meta.column = meta.column
        a_meta.start_pos = meta.start_pos
        a_meta.end_pos = meta.end_pos - 1

        b_meta = Meta()
        b_meta.line = meta.line
        b_meta.column = meta.column + len(a)
        b_meta.start_pos = a_meta.end_pos
        b_meta.end_pos = meta.end_pos

        result = (a_meta, b_meta)

        return result

    def flatten_text_nodes(
        self,
        children: list[Tree],
    ) -> list[Tree]:
        """Creates a list of sentences from a list of (word) nodes."""

        assert isinstance(children, list), type(children)
        assert 1 <= len(children), f"#{len(children)}: [{children}]."

        result: list[Tree] = []
        work = deque(children)
        while work:
            node = work.popleft()
            assert isinstance(node, Tree), repr(node)

            if Token.FLATTEN.name != node.data:
                result.append(node)
                continue

            result.extend(node.children)

        return result

    def get_sentences(
        self,
        children: list[Tree],
        fill: bool,
        terminators: list[Token] | None = None,
    ) -> list[Tree]:
        """Creates a list of sentences from a list of (word) nodes."""

        assert isinstance(children, list), type(children)
        assert 1 <= len(children), f"#{len(children)}: [{children}]."
        assert isinstance(terminators, list) or terminators is None

        token = Token.sentence.name

        if 1 == len(children):
            return children

        if terminators is None:
            token_names = []
        else:
            token_names = [token.name for token in terminators]

        result: list[Tree] = []
        words: list[Tree] = []

        work = deque(children)
        while work:
            node = work.popleft()
            assert isinstance(node, Tree), repr(node)

            if Token.EOS.name == node.data:
                words.append(node)
                meta = Meta()
                meta.line = 1
                meta.column = 1
                meta.start_pos = 1
                meta.end_pos = 1
                sentence = Tree(token, words, meta=meta)
                result.append(sentence)
                words = []
                continue

            if node.data in token_names:
                if 0 < len(words):
                    meta = Meta()
                    meta.line = 1
                    meta.column = 1
                    meta.start_pos = 1
                    meta.end_pos = 1
                    sentence = Tree(token, words, meta=meta)
                    result.append(sentence)
                    words = []
                result.append(node)
                continue

            words.append(node)

        if 0 == len(words):
            return result

        if not fill:
            result.extend(words)
            return result

        meta = Meta()
        meta.line = 1
        meta.column = 1
        meta.start_pos = 1
        meta.end_pos = 1
        sentence = Tree(token, words, meta=meta)
        result.append(sentence)
        return result
