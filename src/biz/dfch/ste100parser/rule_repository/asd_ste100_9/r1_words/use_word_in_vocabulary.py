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

from spacy.tokens import Span

from ....rule_registry import rule
from ....rule_registry import RuleBase
from ....rule_registry import RuleContext
from ....rule_registry import RuleResult

from ....serializer.token_base import Sentence
from ....serializer.token_base import Text
from ....serializer.token_base import TokenBase

from ..rule_id import RuleId


@rule(RuleId.R1_1, token_types=[Text])
class UseWordsInTheVocabulary(RuleBase):
    """
    Use words that are:
      * Approved in the dictionary
      * Technical nouns
      * Technical verbs.
    """

    def examine(
        self,
        token: TokenBase,
        context: RuleContext
    ) -> list[RuleResult]:
        super().examine(token, context)

        result: list[RuleResult] = []

        sent = context.text_utils.find_sentence(token)
        assert sent is not None, f"No sent for:'{token.text}' [{type(token)}]"
        assert isinstance(sent, Sentence), type(sent)

        record = context.token_registry.get_or_default_ste100(sent)
        assert record is not None, f"No record for: [{sent.text}]"
        assert isinstance(record.spacy, Span), type(record.spacy)

        idx = next((i for i, t in enumerate(sent.tokens) if t is token), None)
        length = len(sent.tokens)
        print(f"[{idx}/{length}] '{token.text}' [{type(token).__name__}]")
        print(f"[{len(record.spacy)}] "
              f"spacy: '{[t.text for t in record.spacy]}'")
        print(f"{[(t, t.idx) for t in record.spacy]}")
        print(f"sent: '{sent.span}'. t: '{token.span}'")
        print(f"sent: '{sent.text}'. t: '{token.text}'")

        for i, t in enumerate(record.spacy):
            pass

        return result
