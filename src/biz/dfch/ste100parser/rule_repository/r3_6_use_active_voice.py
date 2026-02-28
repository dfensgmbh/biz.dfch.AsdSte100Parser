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

"""
R1.1: Use words that are:
    * Approved in the dictionary
    * Technical nouns
    * Technical verbs.
"""

from spacy.tokens import Span, Token

from ..rule_registry import rule
from ..rule_registry import Rule
from ..rule_registry import RuleContext
from ..rule_registry import TestResult
from ..rule_registry import TestResultSeverity

from ..serializer.token_base import Sentence
from ..serializer.token_base import TokenBase
from ..serializer.token_base import Paragraph
from ..serializer.token_base import ProcItem

from .ste100_rules import Ste100Rules


class SpacyUtils:
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
    def find_container(token: TokenBase) -> TokenBase | None:
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
        """
        root = sent.root
        tokens = [
            t for t in root.children
            if t.dep_ in ("nsubjpass", "auxpass")
        ]
        if not tokens:
            return []
        tokens.append(root)

        return sorted(tokens, key=lambda t: t.i)


@rule("R5.3", token_types=[Sentence])
class UseImperativeForm(Rule):
    """Write instructions in the imperative (command) form."""

    def examine(
        self,
        token: Sentence,
        context: RuleContext
    ) -> list[TestResult]:
        super().examine(token, context)

        result: list[TestResult] = []

        record = context.token_registry.get_or_default_ste100(token)
        assert record is not None
        assert isinstance(record.spacy, Span), type(record.spacy)

        container = SpacyUtils.find_container(token)
        if not isinstance(container, ProcItem):
            return result

        is_imperative = SpacyUtils.is_imperative_form(record.spacy)
        if not is_imperative:
            return result

        result.append(TestResult(
            rule_id=self.rule_id,
            token=token,
            severity=TestResultSeverity.ERROR,
            message=Ste100Rules.R5_3,
            suggestion="",
        ))

        return result


@rule("R3.6", token_types=[Sentence])
class UseActiveVoice(Rule):
    """
    Use the active voice. In descriptive writing, you can use the passive
    voice only when the agent is unknown.
    """

    def examine(
        self,
        token: Sentence,
        context: RuleContext
    ) -> list[TestResult]:
        super().examine(token, context)

        result: list[TestResult] = []

        record = context.token_registry.get_or_default_ste100(token)
        assert record is not None
        assert isinstance(record.spacy, Span), type(record.spacy)

        words = [t.text for t in SpacyUtils.get_passive_tokens(record.spacy)]
        if not words:
            return []

        prefix = "Unknown"
        severity = TestResultSeverity.WARNING
        container = SpacyUtils.find_container(token)
        if isinstance(container, Paragraph):
            prefix = "Descriptive"
            severity = TestResultSeverity.WARNING
        elif isinstance(container, ProcItem):
            prefix = "Procedural"
            severity = TestResultSeverity.ERROR

        message = f"{prefix}: [{words}] {Ste100Rules.R3_6}"
        result.append(TestResult(
            rule_id=self.rule_id,
            token=token,
            severity=severity,
            message=message,
            suggestion="",
        ))
        return result
