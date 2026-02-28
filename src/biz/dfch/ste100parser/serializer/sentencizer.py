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

from typing import cast

from lark import Tree
from lark.tree import Meta

from spacy.tokens import Doc, Span

from biz.dfch.asdste100vocab import Vocab

from ..ste100doc import Ste100Doc
from ..token_registry import TokenRegistry
from ..serializer.token_base import TokenBase
from ..serializer.token_base import Paragraph
from ..serializer.token_base import ListToken
from ..serializer.token_base import Sentence
from ..token import Token
from ..token_map import TokenMap

from ..nlp.spacy_nlp import SpacyNlp
from ..inspector import Inspector

from .ste100_serializer import Ste100Serializer

from .text_interpreter import Exclude
from .text_interpreter import TextInterpreter


class Sentencizer:
    """
    Identify sentences in a list of text tokens.

    This is our approach to divide text into sentences. We identify parentheses
    first and then process block tokens.
    """

    _nlp: SpacyNlp
    _vocab: Vocab
    _interpreter: TextInterpreter
    _inspector: Inspector
    _serializer: Ste100Serializer
    _token_registry: TokenRegistry

    def __init__(self) -> None:

        self._nlp = SpacyNlp.Factory.get_instance()
        self._vocab = Vocab()
        self._interpreter = TextInterpreter()
        self._inspector = Inspector()
        self._serializer = Ste100Serializer()
        self._token_registry = TokenRegistry.Factory.get_instance()

    @staticmethod
    def get_child_of_container(
        token: TokenBase,
        container_token: TokenBase,
    ) -> TokenBase | None:
        assert isinstance(token, TokenBase), type(token)
        assert isinstance(container_token, TokenBase), type(container_token)

        while token.parent is not None:
            if token.parent is container_token:
                return token
            token = token.parent

        return None

    def create_spacy_doc(
        self,
        nlp: SpacyNlp,
        ste100doc: Ste100Doc,
        words: list[str],
        spaces: list[bool],
        source: list[TokenBase]
    ) -> Doc:

        spacy_doc = Doc(nlp.vocab, words=words, spaces=spaces)
        spacy_doc._.ste100_doc = ste100doc
        for spacy_token, ste_token in zip(spacy_doc, source, strict=True):
            spacy_token._.ste100_token = ste_token
        spacy_doc = nlp(spacy_doc)

        return spacy_doc

    def _extract_sentence(
        self,
        sent: Span,
        container: ListToken,
        token_map: TokenMap,
        *,
        token_count: int,
        sentence_count: int,
    ) -> Sentence:
        assert isinstance(sent, Span), type(sent)
        assert isinstance(container, ListToken), type(container)
        assert isinstance(token_map, TokenMap), type(token_map)
        assert isinstance(token_count, int), type(token_count)
        assert isinstance(sentence_count, int), type(sentence_count)

        sent_text_tokens = []
        for j, token in enumerate(sent):
            token_count += 1
            ste_token = cast(TokenBase, token._.ste100_token)
            sent_text_tokens.append(ste_token)
            sent_container = ste_token.parent
            # In Python v3.11 we cannot use f-strings with tuples.
            # This is why we create the `token_info` first.
            token_info = (
                token.text,
                token.pos_,
                token.dep_,
                type(ste_token).__name__,
                type(sent_container).__name__,
            )
            print(
                f"[{sentence_count}/{j}/{token_count}] "
                f"{token_info} "
                f"[i:{token_map[ste_token]:02}]"
                f"[p:{token_map[sent_container]:02}]"
            )

        sent_start = self.get_child_of_container(
            sent_text_tokens[0], container)
        assert sent_start is not None
        print(
            f"Container '{container.text}' "
            f"[{type(container).__name__}] "
            f"[i:{token_map[container]:02}] "
            f"[p:{token_map[container.parent]:02}]"
        )
        print(
            f"SentStart '{sent_start.text}' "
            f"[{type(sent_start).__name__}] "
            f"[i:{token_map[sent_start]:02}] "
            f"[p:{token_map[sent_start.parent]:02}]"
        )
        print(
            f"SentEnd '{sent_text_tokens[-1].text}' "
            f"[{type(sent_text_tokens[-1]).__name__}] "
            f"[i:{token_map[sent_text_tokens[-1]]:02}] "
            f"[p:{token_map[sent_text_tokens[-1].parent]:02}]"
        )

        sentence = Sentence(sent_start.span, container, [])
        assert not self._token_registry.get_or_default_ste100(
            sentence), sentence
        assert not self._token_registry.get_or_default_spacy(sent), sent
        _ = self._token_registry.add_or_update(ste100=sentence, spacy=sent)

        first = token_map[sent_start]
        last = token_map[sent_text_tokens[-1]]
        container.tokens.insert(
            container.tokens.index(sent_start),
            sentence
        )
        to_be_removed = []
        for t in container.tokens:
            assert isinstance(t, TokenBase), type(t)

            if token_map[t] == token_map[sentence]:
                continue
            if token_map[t.parent] == token_map[sentence]:
                continue

            if not first <= token_map[t] <= last:
                print(
                    f"Skip '{t.text}' "
                    f"[{type(t).__name__}] "
                    f"[i:{token_map[t]:02}] "
                    f"[p:{token_map[t.parent]:02}]"
                )
                continue

            print(
                f"Token '{t.text}' "
                f"[{type(t).__name__}] "
                f"[i:{token_map[t]:02}] "
                f"[p:{token_map[t.parent]:02}]"
            )

            # Change parent of token to new sentence.
            t.parent = sentence
            sentence.tokens.append(t)
            to_be_removed.append(t)

        # Remove token from existing parent container.
        for t in to_be_removed:
            container.tokens.remove(t)

        return sentence

    def _extract_sentences(self, tree: Tree) -> Ste100Doc:
        """
        Find sentences in the children of a lark Tree.

        :param tree: A lark Tree with tokens as children. The Tree must not be
        of type `Parentheses`.
        :type tree: Tree
        :return: An STE100 document that contains identified sentences.
        :rtype: Doc
        """
        assert isinstance(tree, Tree), type(tree)

        # STE100 tokens from tree.
        ste100doc = Ste100Doc(self._interpreter.invoke(tree))
        # At this time there must be only one token that is the container token.
        assert 1 == len(ste100doc), len(ste100doc)
        container = ste100doc[0]
        assert isinstance(container, ListToken), type(container)
        # Create initial token map. We move tokens into sentences with this map.
        token_map = TokenMap()
        ste100_structure = self._inspector.ste100doc(ste100doc, token_map)
        print(ste100_structure)

        # I extract text tokens for spaCy with whitespace information and
        # create the spaCy document.
        extract = self._interpreter.extract_words(
            list(ste100doc),
            exclude=Exclude.PAREN,
        )
        doc = self.create_spacy_doc(
            self._nlp,
            ste100doc,
            words=extract[0],
            spaces=extract[1],
            source=extract[2],
        )
        assert len(extract[0]) == len(doc), f"{len(extract[0])}/{len(doc)}"

        token_count = -1
        for i, sent in enumerate(doc.sents):
            _ = self._extract_sentence(
                sent,
                container,
                token_map,
                token_count=token_count,
                sentence_count=i,
            )

        ste100_structure = self._inspector.ste100doc(ste100doc, token_map)
        print(ste100_structure)

        return ste100doc

    def invoke(self, children: list[Tree], meta: Meta) -> list[Tree]:
        """Find sentences inside a container token and rewrite the lark tree."""
        assert isinstance(children, list), type(children)

        # I simulate that the contents of these children is inside a
        # paragraph.
        # DFTODO - maybe I should move the root token Tree into the
        # `_extract_sentences` method and accept list[Tree] and return
        # `Ste100Doc` or `list[TokenBase]`?
        temp_tree = Tree(Token.paragraph.name, children, meta=meta)
        temp_ste100doc = self._extract_sentences(temp_tree)
        assert 1 == len(temp_ste100doc), len(temp_ste100doc)
        temp_root = temp_ste100doc[0]
        assert isinstance(temp_root, Paragraph), type(temp_root)

        ste100doc = Ste100Doc(temp_root.tokens)
        result = self._serializer.to_lark_tree(ste100doc)
        # Remove all empty sentences.
        # DFTODO - Why are there empty sentences in the first place?
        # Are these line breaks?
        for i in reversed(range(len(result))):
            sent = result[i]
            if 0 == len(sent.children):
                continue
            if sent.data != Token.sentence.name:
                result.remove(sent)
                continue

        return result
