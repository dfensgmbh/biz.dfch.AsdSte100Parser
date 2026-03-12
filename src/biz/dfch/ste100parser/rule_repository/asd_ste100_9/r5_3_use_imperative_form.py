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
R5.3: Write instructions in the imperative (command) form.
"""


from spacy.tokens import Span

from ...rule_registry import rule
from ...rule_registry import RuleBase
from ...rule_registry import RuleContext
from ...rule_registry import RuleResult
from ...rule_registry import RuleResultSeverity
from ...serializer.token_base import ProcItem, Sentence

from .rule_id import RuleId
from .ste100_rules import Ste100Rules


@rule(RuleId.R5_3, token_types=[Sentence])
class UseImperativeForm(RuleBase):
    """Write instructions in the imperative (command) form."""

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

        container = context.text_utils.find_ste100_container(token)
        if not isinstance(container, ProcItem):
            return result

        is_imperative = context.text_utils.is_imperative_form(record.spacy)
        if not is_imperative:
            return result

        result.append(RuleResult(
            rule_id=self.rule_id,
            token=token,
            severity=RuleResultSeverity.ERROR,
            message=Ste100Rules.R5_3,
            suggestion="",
        ))

        return result
