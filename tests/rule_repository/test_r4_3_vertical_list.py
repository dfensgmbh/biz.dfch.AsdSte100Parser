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

# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116

from biz.dfch.ste100parser import ParserAction, Ste100Doc
from biz.dfch.ste100parser.rule_registry import RuleResult
from biz.dfch.ste100parser.rule_registry import RuleSeverity
from biz.dfch.ste100parser.rule_repository import RuleId
from biz.dfch.ste100parser.rule_repository import Ste100Rules

from .test_rule_base import TestRuleBase


class TestVerticalList(TestRuleBase):

    def _act(self, text: str) -> list[RuleResult]:
        assert isinstance(text, str), type(str)
        assert text.strip()

        tree = self.parser.invoke(text, action=ParserAction.PASS2)
        tokens = self.interpreter.invoke(tree)
        doc = Ste100Doc(tokens)
        structure = self.inspector.ste100doc(doc)
        print(structure)

        doc.visit(func=self._process_token)

        return self.rule_results

    def _get_errors(self, result: list[RuleResult]) -> list[RuleResult]:
        errors = [
            r for r
            in result
            if r.rule_id == RuleId.R4_3
            and RuleSeverity.ERROR == r.severity
        ]
        return errors

    def test_correct_list(self):
        text = """This is a sentence that starts a vertical list:
  * Vertical list item one (1)
  * This is the vertical list item two (2).
  * Last vertical list item (3).
"""
        expected = 0

        result = self._act(text)
        errors = self._get_errors(result)

        self.assertEqual(expected, len(errors), [e.suggestion for e in errors])

    def test_start_missing_colon(self):
        text = """This is a sentence that starts a vertical list.
  * This is the first and last vertical list item (1).
"""

        expected = 1

        result = self._act(text)
        errors = self._get_errors(result)

        self.assertEqual(expected, len(errors), [e.suggestion for e in errors])

        error = errors[0]
        self.assertEqual(
            Ste100Rules.R4_3_SUGGESTION_01_START_COLON, error.suggestion)

    def test_missing_uppercase(self):
        text = """This is a sentence that starts a vertical list:
  * this list item does not start with an upper case character.
"""

        expected = 1

        result = self._act(text)
        errors = self._get_errors(result)

        self.assertEqual(expected, len(errors), [e.suggestion for e in errors])

        error = errors[0]
        self.assertEqual(
            Ste100Rules.R4_3_SUGGESTION_03_UPPERCASE, error.suggestion)

    def test_noun_missing_article(self):
        text = """The report must include:
  * Photograph of the unit.
"""

        expected = 1

        result = self._act(text)
        errors = self._get_errors(result)

        self.assertEqual(expected, len(errors), [e.suggestion for e in errors])

        error = errors[0]
        self.assertEqual(
            Ste100Rules.R4_3_SUGGESTION_04_ARTICLE, error.suggestion)

    def test_noun_with_article(self):
        text = """If the Ram Air Turbine (RAT) is retracted:
  * The photograph of the unit.
"""

        expected = 0

        result = self._act(text)
        errors = self._get_errors(result)

        self.assertEqual(expected, len(errors), [e.suggestion for e in errors])

    def test_imperative_stop_with_period(self):
        text = """If the Ram Air Turbine (RAT) is retracted:
  * Remove the tag.
  * Open the isolating valves.
"""

        expected = 1

        result = self._act(text)
        errors = self._get_errors(result)

        self.assertEqual(expected, len(errors), [e.suggestion for e in errors])

        error = errors[0]
        self.assertEqual(
            Ste100Rules.R4_3_SUGGESTION_04_ARTICLE, error.suggestion)

    def test_imperative_stop_without_period(self):
        text = """If the Ram Air Turbine (RAT) is retracted:
  * Remove the tag
  * Open the isolating valves.
"""

        expected = 1

        result = self._act(text)
        errors = self._get_errors(result)

        self.assertEqual(expected, len(errors), [e.suggestion for e in errors])

        error = errors[0]
        self.assertEqual(
            Ste100Rules.R4_3_SUGGESTION_04_ARTICLE, error.suggestion)

    def test_complete_stop_with_period(self):
        text = """When the landing gear retracts:
  * The roller moves out of the slot.
  * The second roller keeps the door operating bar in position.
"""

        expected = 1

        result = self._act(text)
        errors = self._get_errors(result)

        self.assertEqual(expected, len(errors), [e.suggestion for e in errors])

        error = errors[0]
        self.assertEqual(
            Ste100Rules.R4_3_SUGGESTION_04_ARTICLE, error.suggestion)

    def test_complete_stop_without_period(self):
        text = """When the landing gear retracts:
  * The roller moves out of the slot
  * The second roller keeps the door operating bar in position.
"""

        expected = 1

        result = self._act(text)
        errors = self._get_errors(result)

        self.assertEqual(expected, len(errors), [e.suggestion for e in errors])

        error = errors[0]
        self.assertEqual(
            Ste100Rules.R4_3_SUGGESTION_04_ARTICLE, error.suggestion)

    def test_stop_with_comma(self):
        text = """This is a sentence that starts a vertical list:
  * List item with a comma,
  * This is the last list item (2).
"""

        expected = 1

        result = self._act(text)
        errors = self._get_errors(result)

        self.assertEqual(expected, len(errors), [e.suggestion for e in errors])

        error = errors[0]
        self.assertEqual(
            Ste100Rules.R4_3_SUGGESTION_07_NO_COMMA_OR_SEMICOLON, error.suggestion)

    def test_stop_with_semicolon(self):
        text = """This is a sentence that starts a vertical list:
  * List item with a semicolon;
  * This is the last list item (2).
"""

        expected = 1

        result = self._act(text)
        errors = self._get_errors(result)

        self.assertEqual(expected, len(errors), [e.suggestion for e in errors])

        error = errors[0]
        self.assertEqual(
            Ste100Rules.R4_3_SUGGESTION_07_NO_COMMA_OR_SEMICOLON, error.suggestion)

    def test_last_item_missing_period(self):
        text = """This is a sentence that starts a vertical list:
  * This last vertical list item (1) does not stop with a period
"""

        expected = 1

        result = self._act(text)
        errors = self._get_errors(result)

        self.assertEqual(expected, len(errors), [e.suggestion for e in errors])

        error = errors[0]
        self.assertEqual(
            Ste100Rules.R4_3_SUGGESTION_08_END_PERIOD, error.suggestion)

    def test_not_same_marker(self):
        text = """This is a sentence that starts a vertical list:
  * Vertical list item one (1)
  - Last vertical list item (3).
"""

        expected = 1

        result = self._act(text)
        errors = self._get_errors(result)

        self.assertEqual(expected, len(errors), [e.suggestion for e in errors])

        error = errors[0]
        self.assertEqual(
            Ste100Rules.R4_3_SUGGESTION_09_SAME_MARKER, error.suggestion)

    def test_not_same_indent(self):
        text = """This is a sentence that starts a vertical list:
  * Vertical list item one (1)
    * This is the nested vertical list item 1.1.
    * This is the nested vertical list item 1.2.
  * Last vertical list item (3).
"""

        expected = 1

        result = self._act(text)
        errors = self._get_errors(result)

        self.assertEqual(expected, len(errors), [e.suggestion for e in errors])

        error = errors[0]
        self.assertEqual(
            Ste100Rules.R4_3_SUGGESTION_10_SAME_INDENT, error.suggestion)
