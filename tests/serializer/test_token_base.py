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

"""TokenBase, Token* tests."""

# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116
# pylint: disable=C0301

import unittest

from biz.dfch.ste100parser import GrammarType
from biz.dfch.ste100parser import Parser
from biz.dfch.ste100parser import ParserAction
from biz.dfch.ste100parser.ste100doc import Ste100Doc

from biz.dfch.ste100parser.serializer.token_base import TokenRoot
from biz.dfch.ste100parser.serializer.token_base import Paragraph
from biz.dfch.ste100parser.serializer.token_base import Sentence


class TestSentence(unittest.TestCase):
    def test_sents(self):
        text = """Do the "test '(1)'" at full (100 units) speed."""

        tree = Parser(GrammarType.ASD_STE100_9).invoke(
            text=text,
            action=ParserAction.PASS2
        )
        doc = Ste100Doc.from_parse_tree(tree)

        root = doc[0]
        assert isinstance(root, TokenRoot), type(root)
        para = root.tokens[0]
        assert isinstance(para, Paragraph), type(para)
        sut = para.tokens[0]
        assert isinstance(sut, Sentence), type(sut)

        print(f"text: '{sut.text}'")
        token_info = sut.token_info
        for i, ti in enumerate(token_info):
            print(f"[{i}]: '{ti.text}' [{type(ti.token).__name__}]")
