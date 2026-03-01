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

"""test_token_registry"""

import unittest

from lark import Tree

from biz.dfch.ste100parser.grammar import GrammarType
from biz.dfch.ste100parser.inspector import Inspector
from biz.dfch.ste100parser.parser import Parser
from biz.dfch.ste100parser.parser import ParserAction
from biz.dfch.ste100parser.ste100doc import Ste100Doc
from biz.dfch.ste100parser.serializer.text_interpreter import TextInterpreter
from biz.dfch.ste100parser.serializer.token_base import Sentence
from biz.dfch.ste100parser.serializer.token_base import Span
from biz.dfch.ste100parser.token_registry import TokenRegistry
from biz.dfch.ste100parser.serializer.token_base import TokenBase


class TestTokenRegistry(unittest.TestCase):

    def test_singleton(self):

        sut1 = TokenRegistry.Factory.get_instance()
        sut2 = TokenRegistry.Factory.get_instance()

        self.assertEqual(sut1, sut2)

    def test_add_or_update(self):

        ste100_token = Sentence(Span.default(), None, [])  # type: ignore
        lark_token = Tree("sentence", [])

        sut = TokenRegistry.Factory.get_instance()
        sut.clear()

        record_is_none = sut.get_or_default_ste100(ste100_token)
        self.assertIsNone(record_is_none)

        record1 = sut.add_or_update(ste100=ste100_token, lark=lark_token)
        self.assertIsNotNone(record1)
        self.assertEqual(ste100_token, record1.ste100)
        self.assertEqual(lark_token, record1.lark)

        record2 = sut.add_or_update(lark=lark_token)
        self.assertIsNotNone(record2)
        self.assertEqual(ste100_token, record2.ste100)
        self.assertEqual(lark_token, record2.lark)

        self.assertEqual(record1, record2)

    def test_get(self):

        ste100_token = Sentence(Span.default(), None, [])  # type: ignore
        lark_token = Tree("sentence", [])

        sut = TokenRegistry.Factory.get_instance()
        sut.clear()

        record1 = sut.add_or_update(ste100=ste100_token, lark=lark_token)
        self.assertIsNotNone(record1)
        self.assertEqual(ste100_token, record1.ste100)
        self.assertEqual(lark_token, record1.lark)

        record2 = sut.get_or_default_lark(lark_token)
        self.assertIsNotNone(record2)
        assert record2 is not None
        self.assertEqual(ste100_token, record2.ste100)
        self.assertEqual(lark_token, record2.lark)

        self.assertEqual(record1, record2)

    def test_get_or_default(self):

        token = Sentence(Span.default(), None, [])  # type: ignore

        sut = TokenRegistry.Factory.get_instance()
        sut.clear()

        result1 = sut.get_or_default_ste100(token)
        result2 = sut.get_or_default_ste100(token)

        self.assertIsNone(result1)
        self.assertIsNone(result2)

    def test_token_is_in_registry(self):
        text = """This is a paragraph with 2 main sentences.
This is the 2nd sentence and this sentence has another sentence in parentheses (this is the "nested" sentence).
"""
        parser = Parser(GrammarType.ASD_STE100_9)
        tree = parser.invoke(text, action=ParserAction.PASS2)
        tokens = TextInterpreter().invoke(tree)
        ste100doc = Ste100Doc(tokens)
        self.assertIsNotNone(ste100doc)
        structure = Inspector().ste100doc(ste100doc)
        print(structure)

        print(f"height: {ste100doc.get_height()}")
        print(f"count : {ste100doc.get_count()}")

        sentences: list[Sentence] = []

        def func(token: TokenBase, level: int) -> bool:
            nonlocal sentences
            if isinstance(token, Sentence):
                sentences.append(token)
            return True

        ste100doc.visit(func)
        for sentence in sentences:
            print(sentence.text)
            token_registry = TokenRegistry.Factory.get_instance()
            record = token_registry.get_or_default_ste100(sentence)
            assert isinstance(record, TokenRegistry.Record), type(record)
            for t in list(record.spacy):
                print(f"'{t.text}' [{t.pos_}] [{t.dep_}]")
                record_t = token_registry.get_or_default_spacy(t)
