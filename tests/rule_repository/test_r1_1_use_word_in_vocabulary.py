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


class TestUseWordInVocabulary(TestRuleBase):
    def test_approved_word(self):
        text = """Do the "test (1)" at full (100 units) speed."""

        expected = 0

        tree = self.parser.invoke(text, action=ParserAction.PASS2)

        tokens = self.interpreter.invoke(tree)
        doc = Ste100Doc(tokens)
        structure = self.inspector.ste100doc(doc)
        print(structure)

        doc.visit(func=self._process_token)

        result = self.rule_results
        self.assertEqual(expected, len(
            [r for r in result if r.rule_id == RuleId.R1_1]), result)
