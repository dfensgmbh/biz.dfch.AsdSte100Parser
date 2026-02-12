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

"""test_spacy"""

import unittest

import spacy


class TestSpacy(unittest.TestCase):

    nlp: spacy.language.Language

    def setUp(self) -> None:

        self.nlp = spacy.load("en_core_web_sm")

    def test_spacy(self):
        text = """ASD-STE100 Simplified Technical English (STE for short) """ \
            """is a controlled natural language and an international """ \
            """standard to write technical documentation."""
        doc = self.nlp(text)
        print([(token.text, token.pos_, token.dep_) for token in doc])
