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
R4.3: Use a vertical list for complex texts.
"""

from spacy.tokens import Span

from biz.dfch.ste100parser import Char

from ....rule_registry import rule
from ....rule_registry import RuleBase
from ....rule_registry import RuleContext
from ....rule_registry import RuleResult
from ....rule_registry import RulePriority
from ....rule_registry import RuleSeverity
from ....rule_registry import TextUtils
from ....serializer.token_base import ListItem, Sentence, ListToken, TokenBase

from ..rule_id import RuleId
from ..ste100_rules import Ste100Rules


@rule(RuleId.R4_3, token_types=[ListItem], priority=RulePriority.HIGHER)
class UseVerticalListsForComplexTasks(RuleBase):
    """Use a vertical list for complex texts."""

    def _get_list_items(self, token: ListItem) -> list[ListItem]:
        """
        Find, if all ListItem tokens have the same indent and marker.
        """

        assert isinstance(token, ListItem), type(token)

        result: list[ListItem] = [token]

        parent = token.parent
        assert isinstance(parent, ListToken), type(parent)

        tokens = parent.tokens
        count = len(tokens)
        idx = tokens.index(token)
        assert idx < count, (idx, count)

        print(f"Parent contains '{count}' items. Item is at '{idx}'.")

        # Find all ListItem tokens before this token.
        i = idx - 1
        while i >= 0 and isinstance(tokens[i], ListItem):
            result.insert(0, tokens[i])  # type: ignore
            i -= 1

        # Find all ListItems tokens after this token.
        i = idx + 1
        while i < count and isinstance(tokens[i], ListItem):
            result.append(tokens[i])  # type: ignore
            i += 1

        # `result` now contains all items in the vertical list.
        return result

    def _examine_no_comma_or_semicolon(
        self,
        token: ListItem,
        context: RuleContext,
    ) -> list[RuleResult]:

        assert isinstance(token, ListItem), type(token)
        assert isinstance(context, RuleContext), type(context)

        rule_result = RuleResult(
            rule_id=self.rule_id,
            token=token,
            severity=RuleSeverity.OK,
            message=Ste100Rules.R4_3,
            suggestion=Ste100Rules.R4_3_SUGGESTION_07_NO_COMMA_OR_SEMICOLON,
        )
        result: list[RuleResult] = [rule_result]

        sent = token.tokens[0]
        assert isinstance(sent, Sentence), type(sent)

        record = context.token_registry.get_or_default_ste100(sent)
        assert record is not None
        spacy_sent = record.spacy
        assert isinstance(spacy_sent, Span), type(spacy_sent)

        last_token = spacy_sent[-1]
        no_comma_no_semicolon = last_token.text not in (
            Char.COMMA, Char.SEMICOLON)
        if no_comma_no_semicolon:
            rule_result.severity = RuleSeverity.OK
        else:
            rule_result.severity = RuleSeverity.ERROR

        return result

    def _examine_upper_case(
        self,
        token: ListItem,
        context: RuleContext,
    ) -> list[RuleResult]:

        assert isinstance(token, ListItem), type(token)
        assert isinstance(context, RuleContext), type(context)

        rule_result = RuleResult(
            rule_id=self.rule_id,
            token=token,
            severity=RuleSeverity.OK,
            message=Ste100Rules.R4_3,
            suggestion=Ste100Rules.R4_3_SUGGESTION_03_UPPERCASE,
        )
        result: list[RuleResult] = [rule_result]

        sent = token.tokens[0]
        assert isinstance(sent, Sentence), type(sent)

        record = context.token_registry.get_or_default_ste100(sent)
        assert record is not None
        spacy_sent = record.spacy
        assert isinstance(spacy_sent, Span), type(spacy_sent)

        first_token = spacy_sent[0]
        is_start_upper_case = first_token.text[0].isupper()
        if is_start_upper_case:
            rule_result.severity = RuleSeverity.OK
        else:
            print(f"List item does not start with uppercase: "
                  f"'{first_token.text}'.")
            rule_result.severity = RuleSeverity.ERROR

        return result

    def _examine_list_same_indent(
        self,
        token: ListItem,
        tokens: list[ListItem],
    ) -> list[RuleResult]:

        assert isinstance(token, ListItem), type(token)
        assert isinstance(tokens, list), type(tokens)

        rule_result = RuleResult(
            rule_id=self.rule_id,
            token=token,
            severity=RuleSeverity.OK,
            message=Ste100Rules.R4_3,
            suggestion=Ste100Rules.R4_3_SUGGESTION_09_SAME_MARKER,
        )
        result: list[RuleResult] = [rule_result]

        is_correct_format = all(
            e for e in tokens
            if token.indent == e.indent
        )
        if is_correct_format:
            rule_result.severity = RuleSeverity.OK
        else:
            rule_result.severity = RuleSeverity.ERROR

        return result

    def _examine_list_same_marker(
        self,
        token: ListItem,
        tokens: list[ListItem],
    ) -> list[RuleResult]:

        assert isinstance(token, ListItem), type(token)
        assert isinstance(tokens, list), type(tokens)

        rule_result = RuleResult(
            rule_id=self.rule_id,
            token=token,
            severity=RuleSeverity.OK,
            message=Ste100Rules.R4_3,
            suggestion=Ste100Rules.R4_3_SUGGESTION_09_SAME_MARKER,
        )
        result: list[RuleResult] = [rule_result]

        is_correct_format = all(
            e for e in tokens
            if token.indent == e.indent
            and token.marker == e.marker
        )
        if is_correct_format:
            rule_result.severity = RuleSeverity.OK
        else:
            rule_result.severity = RuleSeverity.ERROR

        return result

    def _examine_list_start_colon(
        self,
        token: ListItem,
        tokens: list[TokenBase],
        context: RuleContext,
    ) -> list[RuleResult]:

        assert isinstance(token, ListItem), type(token)
        assert isinstance(tokens, list), type(tokens)
        idx = tokens.index(token)
        assert 0 < idx

        i = idx - 1
        sent = tokens[i]
        assert isinstance(sent, Sentence), type(sent)

        record = context.token_registry.get_or_default_ste100(sent)
        assert record is not None
        spacy_sent = record.spacy
        assert isinstance(spacy_sent, Span), type(spacy_sent)

        last_token = spacy_sent[-1]

        rule_result = RuleResult(
            rule_id=self.rule_id,
            token=token,
            severity=RuleSeverity.OK,
            message=Ste100Rules.R4_3,
            suggestion=Ste100Rules.R4_3_SUGGESTION_01_START_COLON,
        )
        result: list[RuleResult] = [rule_result]

        if Char.COLON == last_token.text:
            rule_result.severity = RuleSeverity.OK
        else:
            rule_result.severity = RuleSeverity.ERROR

        return result

    def _examine_list_end_period(
        self,
        token: ListItem,
        context: RuleContext,
    ) -> list[RuleResult]:

        assert isinstance(token, ListItem), type(token)

        sent = token.tokens[-1]
        record = context.token_registry.get_or_default_ste100(sent)
        assert record is not None
        spacy_sent = record.spacy
        assert isinstance(spacy_sent, Span), type(spacy_sent)

        last_token = spacy_sent[-1]

        rule_result = RuleResult(
            rule_id=self.rule_id,
            token=token,
            severity=RuleSeverity.OK,
            message=Ste100Rules.R4_3,
            suggestion=Ste100Rules.R4_3_SUGGESTION_08_END_PERIOD,
        )
        result: list[RuleResult] = [rule_result]

        if Char.DOT == last_token.text:
            rule_result.severity = RuleSeverity.OK
        else:
            rule_result.severity = RuleSeverity.ERROR

        return result

    def _examine_article_noun(
        self,
        token: ListItem,
        context: RuleContext,
    ) -> list[RuleResult]:

        assert isinstance(token, ListItem), type(token)
        assert isinstance(context, RuleContext), type(context)

        result: list[RuleResult] = []

        for sent in [
            e for e
            in token.tokens
            if isinstance(e, Sentence)
        ]:
            record = context.token_registry.get_or_default_ste100(sent)
            assert record is not None
            spacy_sent = record.spacy
            assert isinstance(spacy_sent, Span), type(spacy_sent)

            rule_result = RuleResult(
                rule_id=self.rule_id,
                token=token,
                severity=RuleSeverity.OK,
                message=Ste100Rules.R4_3,
                suggestion=Ste100Rules.R4_3_SUGGESTION_04_ARTICLE,
            )

            has_article = TextUtils.has_noun_article(spacy_sent)
            if not has_article:
                rule_result.severity = RuleSeverity.WARNING

        return result

    def _examine_period(
        self,
        token: ListItem,
        context: RuleContext,
    ) -> list[RuleResult]:

        assert isinstance(token, ListItem), type(token)

        sent = token.tokens[-1]
        assert isinstance(sent, Sentence), type(sent)
        record = context.token_registry.get_or_default_ste100(sent)
        assert record is not None
        spacy_sent = record.spacy
        assert isinstance(spacy_sent, Span), type(spacy_sent)

        is_imperative = TextUtils.is_imperative_form(spacy_sent)
        is_complete = TextUtils.is_complete_sentence(spacy_sent)

        # The sentence must stop with a period, when:
        # * The sentence is a complete sentence.
        # * The sentence is imperative form.
        # If not, the sentence must not stop with a period.

        last_token = spacy_sent[-1]
        is_period = Char.DOT == last_token.text

        rule_result1 = RuleResult(
            rule_id=self.rule_id,
            token=token,
            severity=RuleSeverity.OK,
            message=Ste100Rules.R4_3,
            suggestion=Ste100Rules.R4_3_SUGGESTION_05_PERIOD,
        )

        rule_result2 = RuleResult(
            rule_id=self.rule_id,
            token=token,
            severity=RuleSeverity.OK,
            message=Ste100Rules.R4_3,
            suggestion=Ste100Rules.R4_3_SUGGESTION_06_NO_PERIOD,
        )

        if is_imperative or is_complete:
            if not is_period:
                rule_result1.severity = RuleSeverity.ERROR
        else:
            if is_period:
                rule_result2.severity = RuleSeverity.ERROR

        result: list[RuleResult] = [rule_result1, rule_result2]

        return result

    def examine(
        self,
        token: ListItem,
        context: RuleContext,
    ) -> list[RuleResult]:
        """
        We examine these conditions:
          * R4_3_SUGGESTION_1_START_COLON
          * R4_3_SUGGESTION_2_IDENTIFY
          * R4_3_SUGGESTION_3_UPPERCASE
          * R4_3_SUGGESTION_4_ARTICLE
          * R4_3_SUGGESTION_5_PERIOD
          * R4_3_SUGGESTION_6_NO_PERIOD
          * R4_3_SUGGESTION_7_NO_COMMA_OR_SEMICOLON
          * R4_3_SUGGESTION_8_END_PERIOD
          * R4_3_SUGGESTION_9_SAME_MARKER_INDENT.
        """

        super().examine(token, context)

        assert isinstance(token, ListItem)

        result: list[RuleResult] = []

        parent = token.parent
        assert isinstance(parent, ListToken), type(parent)
        tokens = parent.tokens

        list_items = self._get_list_items(token)
        print(f"List contains '{len(list_items)}' items.")

        # Examine if this ListItem is the first item in the list.
        is_first_item = list_items[0] is token
        if is_first_item:
            print("ListItem is start of list.")
            # Examine if the sentence that introduces the list stops with a
            # COLON.
            result.extend(self._examine_list_start_colon(
                token,
                tokens,
                context,
            ))

            # Examine if all items in the list have the same marker and
            # indentation.
            result.extend(self._examine_list_same_indent(
                token,
                list_items,
            ))

        # Examine if the ListItem starts with upper case.
        result.extend(self._examine_upper_case(
            token,
            context
        ))

        # Examine if the ListItem stops with a comma or semicolon.
        result.extend(self._examine_no_comma_or_semicolon(
            token,
            context
        ))

        # Show that each item in the list has a correct marker.
        # NOTE: The STE100 parser and grammar make sure, that is correct.
        result.append(RuleResult(
            rule_id=self.rule_id,
            token=token,
            severity=RuleSeverity.OK,
            message=Ste100Rules.R4_3,
            suggestion=Ste100Rules.R4_3_SUGGESTION_02_IDENTIFY,
        ))

        # Examine if the noun in each sentence of the ListItem has an article.
        result.extend(self._examine_article_noun(
            token,
            context,
        ))

        # Examine if this ListItem is the last item in the list.
        is_last_item = list_items[-1] is token
        if is_last_item:
            print("ListItem is end of list.")
            result.extend(self._examine_list_end_period(
                token,
                context,
            ))
        else:
            # Examine if the last sentence of the ListItem stops with a period.
            result.extend(self._examine_period(
                token,
                context,
            ))

        return result
