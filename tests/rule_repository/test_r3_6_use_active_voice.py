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

from parameterized import parameterized

from biz.dfch.ste100parser import ParserAction, Ste100Doc
from biz.dfch.ste100parser.rule_repository import RuleId

from .test_rule_base import TestRuleBase


class TestUseActiveVoice(TestRuleBase):

    @parameterized.expand([
        ("passive", """The safety procedures are given by the manufacturer.
""", 1),
        ("active", """The manufacturer gives the safety procedures.
""", 0),
        ("passive", """The main gear leg is held by the side stay.
""", 1),
        ("active", """The side stay holds the main gear leg.
""", 0),
        ("passive_no_agent", """The dimensions are given in the table.
""", 1),
        ("passive_no_agent", """The main gear leg is held in its position.
""", 1),
        # This will find the passive voice, and this is grammatically correct.
        # However, it will not find that the agent is unknown.
        #         ("passive_unknown_agent1", """During transmission, the data was corrupted.
        # """, 0),
        ("passive_unknown_agent2", """During transmission, something corrupted the data.
""", 0),
        # This will find the active voice, and this is grammatically correct.
        # However, it will not find that the agent is incorrect.
        #         ("passive_incorrect_agent", """Transmission corrupted the data.
        # """, 1),
        ("passive", """The circuits are connected by a switching relay.
""", 1),
        ("active", """A switching relay connects the circuits.
""", 0),
        ("passive", """The door was opened by him.
""", 1),
        ("active", """He opens the door.
""", 0),
        ("passive_complex", """The volume control can be adjusted.
""", 1),
        ("active_complex_proc", """Adjust the volume control.
""", 0),
        ("active_complex_desc", """You can adjust the volume control.
""", 0),
        ("passive_complex", """The oil temperature must be adjusted before the start of the test.
""", 1),
        ("active_complex_proc", """Before you start the test, adjust the oil temperature.
""", 0),
        ("active_complex_desc", """Before the start of the test, the operator must adjust the oil temperature.
""", 0),
        ("passive_complex", """The valve will be adjusted during the test.
""", 1),
        ("active_complex_proc", """During the test, adjust the valve.
""", 0),
        ("active_complex_desc", """You will adjust the valve during the test.
""", 0),
        ("passive_complex", """The component is to be installed before you do the test.
""", 1),
        ("active_complex_proc", """Before you do the test, install the component.
""", 0),
        ("active_complex_desc", """Before the test, the operator must install the component.
""", 0),
    ])
    def test(self, _, value, expected) -> None:

        tree = self.parser.invoke(value, action=ParserAction.PASS2)
        tokens = self.interpreter.invoke(tree)
        doc = Ste100Doc(tokens)
        structure = self.inspector.ste100doc(doc)
        print(structure)

        doc.visit(func=self._process_token)

        result = self.rule_results
        self.assertEqual(expected, len(
            [r for r in result if r.rule_id == RuleId.R3_6]), result)

    def test_active_voice(self):
        text = """He opens the door.
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
            [r for r in result if r.rule_id == RuleId.R3_6]), result)

    def test_passive_voice(self):
        text = """The door was opened by him.
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
            [r for r in result if r.rule_id == RuleId.R3_6]), result)

    def test_agent(self):
        text = """On the ground, the valve can be opened with the override handle.
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
            [r for r in result if r.rule_id == RuleId.R3_6]), result)
