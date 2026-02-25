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

"""test_doc tests."""

# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116
# pylint: disable=C0301

import unittest

from biz.dfch.ste100parser import GrammarType
from biz.dfch.ste100parser import Parser
from biz.dfch.ste100parser import ParserAction
from biz.dfch.ste100parser.ste100doc import Ste100Doc


class TestDoc(unittest.TestCase):
    def test_sents(self):
        value = """This is the first sentence. This is the second sentence."""

        tree = Parser(GrammarType.ASD_STE100_9).invoke(
            value, action=ParserAction.PASS2)

        sut = Ste100Doc.from_parse_tree(tree)

        self.assertIsNotNone(sut)
        self.assertIsInstance(sut, Ste100Doc)

        print(f"#{len(sut)}")
        for token in sut:
            print(token)
