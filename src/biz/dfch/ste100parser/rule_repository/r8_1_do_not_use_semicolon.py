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
from ..serializer.token_base import Heading
from ..serializer.token_base import TokenRoot

from ..rule_registry import rule
from ..rule_registry import Rule
from ..rule_registry import RuleContext
from ..rule_registry import RulePriority
from ..rule_registry import TestResult
from ..rule_registry import TestResultSeverity


@rule("R8.1", token_types=[Punct], priority=RulePriority.HIGHER)
class DoNotUseSemicolon(Rule):
    """
    You can use all standard English punctuation marks
    but not the semicolon (;).
    """

    RULE = "The semicolon (;) is not permitted in STE because it lets you " \
        "write very long sentences. It is also not easy to use correctly. As " \
        "an alternative to the semicolon, always write two different sentences."

    def examine(self, token: Punct, context: RuleContext) -> list[TestResult]:
        super().examine(token, context)

        result: list[TestResult] = []

        if Char.SEMICOLON != token.text:
            return result

        result.append(TestResult(
            rule_id=self.rule_id,
            token=token,
            severity=TestResultSeverity.ERROR,
            message=self.RULE,
            suggestion=""))

        return result
