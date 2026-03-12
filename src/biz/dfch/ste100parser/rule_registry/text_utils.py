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
        """Examines if a sentence is in imperative form."""

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
        Find the next sentence of the token.
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
    def get_numeric_tokens(sent: Span) -> list[Token]:
        pass