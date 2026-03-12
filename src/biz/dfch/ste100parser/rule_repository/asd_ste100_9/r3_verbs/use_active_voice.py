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
R3.6: Use the active voice. In descriptive writing, you can use the passive
voice only when the agent is unknown.
"""

from spacy.tokens import Span

from ....rule_registry import rule
from ....rule_registry import RuleBase
from ....rule_registry import RuleContext
from ....rule_registry import RuleResult
from ....rule_registry import RuleSeverity

from ....serializer.token_base import Sentence
from ....serializer.token_base import Paragraph
from ....serializer.token_base import ProcItem

from ..ste100_rules import Ste100Rules
from ..rule_id import RuleId


@rule(RuleId.R3_6, token_types=[Sentence])
class UseActiveVoice(RuleBase):
    """
    Use the active voice. In descriptive writing, you can use the passive
    voice only when the agent is unknown.
    """

    def examine(
        self,
        token: Sentence,
        context: RuleContext
    ) -> list[RuleResult]:
        super().examine(token, context)

        result: list[RuleResult] = []

        record = context.token_registry.get_or_default_ste100(token)
        assert record is not None
        assert isinstance(record.spacy, Span), type(record.spacy)

        words = [
            t.text for t
            in context.text_utils.get_passive_tokens(
                record.spacy)
        ]
        if not words:
            return []

        prefix = "Unknown"
        severity = RuleSeverity.WARNING
        container = context.text_utils.find_ste100_container(token)
        if isinstance(container, Paragraph):
            prefix = "Descriptive"
            severity = RuleSeverity.WARNING
        elif isinstance(container, ProcItem):
            prefix = "Procedural"
            severity = RuleSeverity.ERROR

        message = f"{prefix}: [{words}] {Ste100Rules.R3_6}"
        result.append(RuleResult(
            rule_id=self.rule_id,
            token=token,
            severity=severity,
            message=message,
            suggestion="",
        ))
        return result
