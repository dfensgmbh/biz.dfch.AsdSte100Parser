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
Make sure that no paragraph has more than six sentences.
"""

from biz.dfch.ste100parser.rule_registry import (
    rule,
    RuleBase,
    RuleContext,
    RuleResult,
    RuleSeverity,
)
from biz.dfch.ste100parser.serializer.token_base import ListItem
from biz.dfch.ste100parser.serializer.token_base import Paragraph
from biz.dfch.ste100parser.serializer.token_base import Sentence
from biz.dfch.ste100parser.serializer.token_base import TokenBase

from ..rule_id import RuleId
from ..ste100_rules import Ste100Rules


@rule(RuleId.R6_6, token_types=[Paragraph])
class UseMaxSixSentences(RuleBase):
    """
    Make sure that no paragraph has more than six sentences.
    """

    def examine(
        self,
        token: Paragraph,
        context: RuleContext,
    ) -> list[RuleResult]:
        super().examine(token, context)

        max_sentences: int = 6

        result: list[RuleResult] = []

        count: int = 0
        previous_token: TokenBase = token

        for current_token in token.tokens:
            # Count each sentence in a paragraph as one sentence.
            if isinstance(current_token, Sentence):
                count += 1
                previous_token = current_token

            # Count a vertical list in a paragraph as one sentence.
            if (
                isinstance(current_token, ListItem) and
                isinstance(previous_token, Sentence)
            ):
                count += 1
                previous_token = current_token

        if max_sentences >= count:
            return result

        result.append(RuleResult(
            rule_id=self.rule_id,
            token=token,
            severity=RuleSeverity.ERROR,
            message=Ste100Rules.R6_6.format(count=count),
            suggestion=Ste100Rules.R6_6_SUGGESTION,
        ))

        return result
