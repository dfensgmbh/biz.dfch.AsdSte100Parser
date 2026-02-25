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

"""test_inspector tests"""

import unittest

from biz.dfch.asdste100vocab import (
    Vocab,
    Word,
    WordCategory,
    WordStatus,
    WordType
)

from biz.dfch.ste100parser import GrammarType, Parser, ParserAction
from biz.dfch.ste100parser.inspector import Inspector
from biz.dfch.ste100parser.serializer.text_interpreter import TextInterpreter
from biz.dfch.ste100parser.ste100doc import Ste100Doc
from biz.dfch.ste100parser.token_map import TokenMap


class TestInspector(unittest.TestCase):

    def test_inspector_full(self):
        text = r"""*This* _is_ an *in-flight* *_text_* from the U.K. """ \
            r"""with (something in) parentheses. """ \
            r"""And here is another sentence """ \
            r"""(*which* does not make sense (sic!)). """

        vocab = Vocab(use_ste100=True)
        vocab.append(Word(
            name="U.K.",
            status=WordStatus.APPROVED,
            type_=WordType.NOUN,
            source="custom001",
            category=WordCategory.ROLES_GROUPS,
        ))
        vocab.append(Word(
            name="in-flight",
            status=WordStatus.APPROVED,
            type_=WordType.ADJECTIVE,
            source="custom001",
            category=WordCategory.VEHICLES_MACHINES,
        ))
        parser = Parser(GrammarType.ASD_STE100_9)
        tree = parser.invoke(text, action=ParserAction.PASS2)

        interpreter = TextInterpreter(vocab)
        tokens = interpreter.invoke(tree)
        # We start at Paragraph
        tokens = tokens[0].tokens  # type: ignore
        self.assertIsInstance(tokens, list)
        self.assertTrue(0 < len(tokens))
        print("#### 1")
        print(tokens)

        ste100doc = Ste100Doc(tokens)
        token_map = TokenMap()
        inspect = Inspector(show_nlp=True)
        print(inspect.ste100doc(ste100doc, token_map))
