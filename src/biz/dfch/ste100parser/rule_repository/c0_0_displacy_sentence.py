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
Displays a spaCy sentence with displacy.
"""

from spacy import displacy
from spacy.tokens import Span

from ..rule_registry import rule
from ..rule_registry import Rule
from ..rule_registry import RuleContext
from ..rule_registry import RulePriority
from ..rule_registry import RuleResult

from ..token_registry import TokenRegistry

from ..serializer.token_base import TokenBase
from ..serializer.token_base import Sentence


@rule("C0.0", token_types=[Sentence], priority=RulePriority.HIGHEST)
class DisplacySentence(Rule):
    """
    Displays a spaCy sentence with displacy.
    """

    _registry: TokenRegistry

    def __init__(self) -> None:
        self._registry = TokenRegistry.Factory.get_instance()

    def examine(
        self,
        token: TokenBase,
        context: RuleContext
    ) -> list[RuleResult]:
        super().examine(token, context)

        result: list[RuleResult] = []

        record = context.token_registry.get_or_default_ste100(token)
        assert record is not None
        assert isinstance(record.spacy, Span), type(record.spacy)

        for t in record.spacy:
            print(f"'{t.text}' [{t.pos_}] [{t.dep_}]")

        displacy.render(record.spacy, style="dep", jupyter=True)

        return result
