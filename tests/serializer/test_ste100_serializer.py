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

"""test_ste100_serializer tests."""

# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116
# pylint: disable=C0301

import unittest

from biz.dfch.ste100parser.ste100doc import Ste100Doc
from biz.dfch.ste100parser.serializer.ste100_serializer import Ste100Serializer
from biz.dfch.ste100parser.serializer.token_base import TokenBase
from biz.dfch.ste100parser.serializer.token_base import TokenRoot
from biz.dfch.ste100parser.serializer.token_base import Paragraph
from biz.dfch.ste100parser.serializer.token_base import Sentence
from biz.dfch.ste100parser.serializer.token_base import Text
from biz.dfch.ste100parser.serializer.token_base import Word
from biz.dfch.ste100parser.serializer.token_base import Ws
from biz.dfch.ste100parser.serializer.token_base import Punct
from biz.dfch.ste100parser.serializer.text_interpreter import Span
from biz.dfch.ste100parser.serializer.text_interpreter import TextInterpreter
from biz.dfch.ste100parser.inspector import Inspector


class TestSte100Serializer(unittest.TestCase):

    def test_sth(self) -> None:

        inspector = Inspector()

        root = TokenRoot(Span.default(), None, [])  # type: ignore
        para = Paragraph(Span.default(), root, [])  # type: ignore

        tokens: list[TokenBase] = []
        sentence = Sentence(Span.default(), para, tokens)
        tokens.append(Word(Span.default(), sentence, "This"))
        tokens.append(Ws(Span.default(), sentence, " "))
        tokens.append(Word(Span.default(), sentence, "is"))
        tokens.append(Ws(Span.default(), sentence, " "))
        tokens.append(Word(Span.default(), sentence, "a"))
        tokens.append(Ws(Span.default(), sentence, " "))
        tokens.append(Word(Span.default(), sentence, "sentence"))
        tokens.append(Punct(Span.default(), sentence, "."))

        para.tokens.append(sentence)
        root.tokens.append(para)

        sut = Ste100Serializer()
        doc = Ste100Doc([root])

        structure = inspector.ste100doc(doc)
        print(structure)

        trees = sut.to_lark_tree(doc)
        for tree in trees:
            print(tree.pretty())

        interpreter = TextInterpreter()
        new_tokens = interpreter.invoke(trees)
        new_doc = Ste100Doc(new_tokens)
        structure = inspector.ste100doc(new_doc)
        print(structure)
