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
R8.1: You can use all standard English punctuation marks
but not the semicolon (;).
"""

from ..char import Char
from ..serializer.token_base import Punct

from ..rule_registry import rule
from ..rule_registry import Rule
from ..rule_registry import RuleContext
from ..rule_registry import RulePriority
from ..rule_registry import RuleResult
from ..rule_registry import RuleResultSeverity

from .ste100_rules import Ste100Rules

from .rule_id import RuleId


@rule(RuleId.R8_1, token_types=[Punct], priority=RulePriority.HIGHER)
class DoNotUseSemicolon(Rule):
    """
    You can use all standard English punctuation marks
    but not the semicolon (;).
    """

    def examine(self, token: Punct, context: RuleContext) -> list[RuleResult]:
        super().examine(token, context)

        result: list[RuleResult] = []

        if Char.SEMICOLON != token.text:
            return result

        result.append(RuleResult(
            rule_id=self.rule_id,
            token=token,
            severity=RuleResultSeverity.ERROR,
            message=Ste100Rules.R8_1,
            suggestion=""))

        return result
