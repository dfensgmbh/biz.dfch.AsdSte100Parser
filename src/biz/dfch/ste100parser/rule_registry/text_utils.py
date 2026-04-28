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

# pylint: disable=R0903

from spacy.tokens import Span, Token

from ..serializer.token_base import (
    Paragraph,
    ProcItem,
    Sentence,
    TokenBase
)


class TextUtils:
    """SpaCy text processing methods."""

    @staticmethod
    def is_imperative_form(sent: Span) -> bool:
        """Examine if a sentence is in imperative form."""

        root = sent.root
        if root.pos_ != "VERB":
            return False

        if root.morph.get("VerbForm", []) != ["Inf"]:
            return False

        if any(t.dep_ == "nsubj" for t in sent):
            return False

        return True

    @staticmethod
    def find_ste100_container(token: TokenBase) -> TokenBase | None:
        """
        Find the parent of the token that is either `Paragraph`, `ProcItem`
        or `None`.
        """
        current = token.parent

        while current is not None:
            if isinstance(current, (Paragraph, ProcItem)):
                return current
            current = current.parent

        return None

    @staticmethod
    def find_sentence(token: TokenBase) -> Sentence | None:
        """
        Find the enclosing sentence of the token.
        """
        current = token.parent

        while current is not None:
            if isinstance(current, Sentence):
                return current
            current = current.parent

        return None

    @staticmethod
    def get_passive_tokens(sent: Span) -> list[Token]:
        """
        Examines if the sentence is in passive voice. Then the list contains
        the tokens that are in passive voice.
        If there is no agent, then a passive voice is permitted.
        """
        result: list[Token] = []

        verbs = [t for t in sent if t.pos_ == "VERB"]
        for verb in verbs:
            tokens: list[Token] = [
                t for t in verb.children
                if t.dep_ in ("nsubjpass", "auxpass")
            ]
            if not tokens:
                continue
            result.extend(tokens)
            result.append(verb)

        return sorted(result, key=lambda t: t.i)

    @staticmethod
    def is_complete_sentence(sent: Span) -> bool:
        """
        Examine if the sentence `sent` is a grammatically correct and full
        sentence.

        It does not examine if the punctuation of the sentence is correct.
        """

        assert isinstance(sent, Span), type(sent)

        # First, examine if the sentence is in imperative form.
        # Then, we identify the sentence as complete.
        if TextUtils.is_imperative_form(sent):
            return True

        # Then, we examine if there is a verb.

        root = sent.root
        if root.pos_.lower() in ("verb", "aux"):
            return any(
                e for e
                in sent
                if e.head == root
                and e.dep_.lower() in ("nsubj", "nsubjpass")
            )

        return False

    @staticmethod
    def has_noun_article(sent: Span) -> bool:
        """
        Examine if the noun of the sentence `sent` has an article.
        """

        assert isinstance(sent, Span), type(sent)

        # First, find noun.

        root = sent.root
        print("Sentence root: ", (root, root.pos_, root.dep_))

        if root.pos_.lower() in ("noun"):
            noun = root
        elif root.pos_.lower() in ("aux", "verb"):
            nouns = [
                e for e
                in sent
                if e.head == root
                and e.pos_.lower() in ("noun")
                and e.dep_.lower() in ("nsubj", "nsubjpass")
            ]
            if 1 != len(nouns):
                print("No single sentence noun found: ", nouns)
                return False
            noun = nouns[0]
        else:
            print("No sentence correct root found.")
            return False

        # Then, find if there is an article for that noun.
        print("Sentence noun: ", (noun, noun.pos_, noun.dep_))
        result = any(
            e for e
            in sent
            if noun == e.head
            and e.pos_.lower() in ("det")
        )

        return result
