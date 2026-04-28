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

import unittest
from parameterized import parameterized

from biz.dfch.ste100parser.nlp import SpacyNlp

from biz.dfch.ste100parser.rule_registry import TextUtils


class TestTextUtils(unittest.TestCase):

    nlp: SpacyNlp

    def setUp(self) -> None:
        self.nlp = SpacyNlp.Factory.get_instance()

    @parameterized.expand([
        ("no_verb", "The photograph of the unit"),
        ("aux_verb", "The photograph of the unit is visible."),
        ("verb", "The photograph of the unit creates a shadow."),
        ("pass", "The photograph was deleted."),
        ("past", "The operator has deleted the photograph."),
    ])
    def test_noun_with_article(self, rule, text):

        doc = self.nlp(text)
        sent = list(doc.sents)[0]

        result = TextUtils.has_noun_article(sent)
        self.assertTrue(result, (rule, text))

    @parameterized.expand([
        ("no_verb", "Photograph of the unit."),
        ("aux_verb", "Photograph of the unit is visible."),
        ("verb", "Photograph of the unit creates a shadow."),
        ("pass", "Photograph was deleted."),
        ("past", "Operator has deleted the photograph."),
    ])
    def test_noun_without_article(self, rule, text):

        doc = self.nlp(text)
        sent = list(doc.sents)[0]

        result = TextUtils.has_noun_article(sent)
        self.assertFalse(result, (rule, text))

    @parameterized.expand([
        ("no_imp", "The roller moves out of the slot.", False),
        ("imp", "Remove the tag.", True),
    ])
    def test_imperative_form(self, rule, text, expected):

        doc = self.nlp(text)
        sent = list(doc.sents)[0]

        result = TextUtils.is_imperative_form(sent)
        self.assertEqual(expected, result, (rule, text))

    @parameterized.expand([
        ("act", "Subject uses object.", False),
        ("pass", "Object is used by subject.", True),
    ])
    def test_passive_voice(self, rule, text, expected):

        doc = self.nlp(text)
        sent = list(doc.sents)[0]

        result = TextUtils.get_passive_tokens(sent)

        self.assertEqual(expected, any(result), (rule, text, result))

    @parameterized.expand([
        ("verb", "This creates a problem.", True),
        ("aux", "This is a complete sentence.", True),
        ("imp", "Remove the tag.", True),
        ("part", "the service cabinet", False),
        ("pass", "Message deleted.", True),
    ])
    def test_complete_sentence(self, rule, text, expected):

        doc = self.nlp(text)
        sent = list(doc.sents)[0]

        result = TextUtils.is_complete_sentence(sent)

        self.assertEqual(expected, result, (rule, text, result))
