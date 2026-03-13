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

"""
rule_repository module.
"""

from biz.dfch.ste100parser import ParserAction, Ste100Doc
from biz.dfch.ste100parser.rule_repository import RuleId
from tests.rule_repository.test_rule_base import TestRuleBase


class TestUseMaxSixSentences(TestRuleBase):

    def test_six_sentences(self):
        text = """This is sentence one (first).
This is sentence two (2).
This is sentence three (3).
This is sentence four (4).
This is sentence five (5).
This is sentence six (6 and last).

"""
        expected = 0

        tree = self.parser.invoke(text, action=ParserAction.PASS2)

        tokens = self.interpreter.invoke(tree)
        doc = Ste100Doc(tokens)
        structure = self.inspector.ste100doc(doc)
        print(structure)

        doc.visit(func=self._process_token)

        result = self.rule_results
        self.assertEqual(expected, len(
            [r for r in result if r.rule_id == RuleId.R6_6]), result)

    def test_seven_sentences(self):
        text = """This is sentence one (first).
This is sentence two (2).
This is sentence three (3).
This is sentence four (4).
This is sentence five (5).
This is sentence six (6).
This is sentence seven (7 and last).

"""
        expected = 1

        tree = self.parser.invoke(text, action=ParserAction.PASS2)

        tokens = self.interpreter.invoke(tree)
        doc = Ste100Doc(tokens)
        structure = self.inspector.ste100doc(doc)
        print(structure)

        doc.visit(func=self._process_token)

        result = self.rule_results
        self.assertEqual(expected, len(
            [r for r in result if r.rule_id == RuleId.R6_6]), result)

    def test_six_sentences_and_list(self):
        text = """This is sentence one (first).
This is sentence two (2).
This is sentence three (3).
This is sentence four (4).
This is sentence five (5).
This is sentence six (6) that starts a list:
  * This is the first list item.
  * This is the second list item.
  * This is the last list item.

"""
        expected = 1

        tree = self.parser.invoke(text, action=ParserAction.PASS2)

        tokens = self.interpreter.invoke(tree)
        doc = Ste100Doc(tokens)
        structure = self.inspector.ste100doc(doc)
        print(structure)

        doc.visit(func=self._process_token)

        result = self.rule_results
        self.assertEqual(expected, len(
            [r for r in result if r.rule_id == RuleId.R6_6]), result)

    def test_six_sentences_and_note(self):
        """A note is not part of a paragraph. Thus it does not add to the sentence count."""
        text = """This is sentence one (first).
This is sentence two (2).
This is sentence three (3).
This is sentence four (4).
This is sentence five (5).
This is sentence six (6 and last), and a note follows this sentence.
NOTE: This is a note in a paragraph.

"""
        expected = 0

        tree = self.parser.invoke(text, action=ParserAction.PASS2)

        tokens = self.interpreter.invoke(tree)
        doc = Ste100Doc(tokens)
        structure = self.inspector.ste100doc(doc)
        print(structure)

        doc.visit(func=self._process_token)

        result = self.rule_results
        self.assertEqual(expected, len(
            [r for r in result if r.rule_id == RuleId.R6_6]), result)

    def test_six_sentences_and_colon_is_sentence_terminator(self):
        """A note is not part of a paragraph. Thus it does not add to the sentence count."""
        text = """This is sentence one (first).
This is sentence two (2) that stops with a colon:
This is sentence three (3).
This is sentence four (4).
This is sentence five (5).
This is sentence six (6 and last), and a note follows this sentence.

"""
        expected = 0

        tree = self.parser.invoke(text, action=ParserAction.PASS2)

        tokens = self.interpreter.invoke(tree)
        doc = Ste100Doc(tokens)
        structure = self.inspector.ste100doc(doc)
        print(structure)

        doc.visit(func=self._process_token)

        result = self.rule_results
        self.assertEqual(expected, len(
            [r for r in result if r.rule_id == RuleId.R6_6]), result)
