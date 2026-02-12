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
# pylint: disable=C0301

"""test_sentence"""

import os
import unittest

from parameterized import parameterized
import spacy


@unittest.skipIf(os.getenv('GITHUB_ACTIONS') == 'true', "Do not do these tests on Github.")
class TestSentenceTrf(unittest.TestCase):

    nlp: spacy.language.Language

    def setUp(self) -> None:

        self.nlp = spacy.load("en_core_web_trf")

    def test_one_simple_sentence(self):
        text = """This is a simple sentence."""

        doc = self.nlp(text)

        self.assertEqual(1, len(list(doc.sents)))

    def test_two_simple_sentences(self):
        text = """This is a simple sentence. And this is another simple sentence."""

        doc = self.nlp(text)

        self.assertEqual(2, len(list(doc.sents)))

    def test_sentence_with_abbreviation_at_end(self):
        text = """The store opens at 9 a.m."""

        doc = self.nlp(text)

        self.assertEqual(1, len(list(doc.sents)))

    @parameterized.expand([
        ("abbrev_noun", "The store opens at 9 a.m. The store closes at 4 p.m.", 2),
        ("abbrev_cconj_noun", "The store opens at 9 a.m. And the store closes at 4 p.m.", 2),
        ("abbrev_pron", "The store opens at 9 a.m. It closes at 4 p.m.", 2),
        ("propn_pron_pl", "London is the capital of the U.K. They have the Tower of London.", 2),
        ("propn_pron_sg", "London is the capital of the U.K. It has the Tower of London.", 2),
        ("propn_propn", "London is the capital of the U.K. London has the Tower of London.", 2),
        ("propn_cconj_pron_but", "London is the capital of the U.K. But it is not the capital of Scotland.", 2),
        ("propn_cconj_pron_and", "London is the capital of the U.K. And, it has the Tower of London.", 2),
        ("propn_propn_uk", "London is the capital of the U.K. The U.K. has many inhabitants.", 2),
        ("propn_cconj_propn", "London is the capital of the U.K. And the U.K. has many inhabitants.", 2),
    ])
    def test_sentences_correct(self, name, text, expected):

        doc = self.nlp(text)

        self.assertEqual(expected, len(list(doc.sents)), name)
        print([(token.text, token.pos_, token.dep_) for token in doc])

    @parameterized.expand([
        ("abbrev_cconj_pron", "The store opens at 9 a.m. And it closes at 4 p.m.", 1),
        ("propn_cconj_pron1_pl", "London is the capital of the U.K. And they have the Tower of London.", 1),
        ("propn_cconj_pron1_sg", "London is the capital of the U.K. And it has the Tower of London.", 1),
        ("propn_adv1", "London is the capital of the U.K. Very often, it is rainy there.", 1),
        ("propn_adv2", "London is the capital of the U.K. Very often, it rains there.", 1),
        ("propn_det_propn", "London is the capital of the U.K. The U.K. is very rainy.", 1),
        ("propn_cconj_propn", "London is the capital of the U.K. And the U.K. is very rainy.", 1),
    ])
    def test_sentence_incorrect(self, name, text, expected):

        doc = self.nlp(text)

        self.assertEqual(expected, len(list(doc.sents)), name)
        print([(token.text, token.pos_, token.dep_) for token in doc])
