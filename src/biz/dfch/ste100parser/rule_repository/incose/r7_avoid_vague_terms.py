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
R7 - /ACCURACY/AVOIDVAGUETERMS

Avoid the use of vague terms.
"""

from spacy.tokens import Span

from biz.dfch.asdste100vocab import (
    Vocab,
    Word,
    WordCategory,
    WordNote,
    WordStatus,
    WordType,
)

from biz.dfch.ste100parser.rule_registry import (
    RuleBase,
    RuleContext,
    RuleResult,
    RuleResultSeverity,
    rule,
)
from biz.dfch.ste100parser.serializer.token_base import Sentence


@rule("R7 - /ACCURACY/AVOIDVAGUETERMS", token_types=[Sentence])
class AccuracyAvoidVagueTerms(RuleBase):
    """
    Avoid the use of vague terms.
    """

    _vocab: Vocab

    def __init__(self) -> None:
        super().__init__()

        self._vocab = Vocab(use_ste100=False)
        self._vocab.append(Word(
            name="some",
            status=WordStatus.REJECTED,
            type_=WordType.ADVERB,
            category=WordCategory.DEFAULT,
            source="INCOSE_REQ",
            note=WordNote(
                value="R7 - /ACCURACY/AVOIDVAGUETERMS"
            ),
        ))
        self._vocab.append(Word(
            name="usually",
            status=WordStatus.REJECTED,
            type_=WordType.ADVERB,
            category=WordCategory.DEFAULT,
            source="INCOSE_REQ",
            note=WordNote(
                value="R7 - /ACCURACY/AVOIDVAGUETERMS"
            ),
            ste_example=[
                r"The Flight_Information_System must have an Availability "
                "of greater than xx% over a period of greater than yy "
                "hours.",
            ],
            nonste_example=[
                r"The Flight_Information_System shall usually be on line.",
            ]
        ))

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

        for t in record.spacy:
            if t.lemma_.lower() not in [
                w.name.lower()
                for w in self._vocab
            ]:
                continue

            result.append(RuleResult(
                rule_id="R7 - /ACCURACY/AVOIDVAGUETERMS",
                token=token,
                severity=RuleResultSeverity.OK,
                message="Avoid the use of vague terms.",
                suggestion="",
            ))

        return result
