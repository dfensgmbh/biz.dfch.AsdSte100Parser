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

from biz.dfch.asdste100vocab import Vocab
from biz.dfch.asdste100vocab import Word
from biz.dfch.asdste100vocab import WordCategory
from biz.dfch.asdste100vocab import WordSource
from biz.dfch.asdste100vocab import WordStatus
from biz.dfch.asdste100vocab import WordType

from biz.dfch.ste100parser import GrammarType
from biz.dfch.ste100parser import Inspector
from biz.dfch.ste100parser import Parser
from biz.dfch.ste100parser import ParserAction
from biz.dfch.ste100parser import Ste100Doc
from biz.dfch.ste100parser.serializer.text_interpreter import TextInterpreter

from biz.dfch.ste100parser.serializer.token_base import TokenBase

from biz.dfch.ste100parser.rule_registry import RuleRegistry
from biz.dfch.ste100parser.rule_registry import RuleContext
from biz.dfch.ste100parser.rule_registry import TextUtils

from biz.dfch.ste100parser.token_registry import TokenRegistry


class TestDoNotUseSemicolon(unittest.TestCase):

    RULE_PACKAGE_PATH = "biz.dfch.ste100parser.rule_repository"
    parser: Parser
    vocab: Vocab
    interpreter: TextInterpreter
    inspector: Inspector
    token_registry: TokenRegistry
    rule_context: RuleContext
    rule_registry: RuleRegistry

    def setUp(self) -> None:
        self.parser = Parser(GrammarType.ASD_STE100_9)

        self.vocab = Vocab()
        self.vocab.append(word=Word(
            name="wombat",
            status=WordStatus.APPROVED,
            type_=WordType.TECHNICAL_NOUN,
            source=WordSource.STE100_9,
            category=WordCategory.ANIMALS_PLANTS,
        ))

        self.interpreter = TextInterpreter(vocab=self.vocab)
        self.inspector = Inspector()

        self.token_registry = TokenRegistry.Factory.get_instance()
        self.rule_context = RuleContext(self.vocab, self.token_registry, TextUtils())
        self.rule_registry = RuleRegistry()
        self.rule_registry.install_rules(self.RULE_PACKAGE_PATH)

    def _process_token(self, token: TokenBase, level: int) -> bool:
        _ = level
        print(f"[{type(token).__name__}] Processing token '{token.text}' ...")
        rules = self.rule_registry.get_rules(token)
        for rule in rules:
            print(
                f"Processing rule '{rule.rule_id}' [{rule.priority}] [{type(token).__name__}] ...")
            test_results = rule.examine(token, self.rule_context)
            for test_result in test_results:
                print(
                    f"[{test_result.severity}] {test_result.rule_id}: '{test_result.message}'")
        return True

    def test_sentence_with_semicolon(self):
        text = """The first sentences stops with a semicolon; the last sentence stops with a dot."""

        tree = self.parser.invoke(text, action=ParserAction.PASS2)

        tokens = self.interpreter.invoke(tree)
        doc = Ste100Doc(tokens)
        structure = self.inspector.ste100doc(doc)
        print(structure)

        doc.visit(func=self._process_token)

    def test_imperative_in_descriptive(self):
        text = """Close the door.
"""

        tree = self.parser.invoke(text, action=ParserAction.PASS2)

        tokens = self.interpreter.invoke(tree)
        doc = Ste100Doc(tokens)
        structure = self.inspector.ste100doc(doc)
        print(structure)

        doc.visit(func=self._process_token)

    def test_imperative_in_procedure(self):
        text = """
A) Close the door."""

        tree = self.parser.invoke(text, action=ParserAction.PASS2)

        tokens = self.interpreter.invoke(tree)
        doc = Ste100Doc(tokens)
        structure = self.inspector.ste100doc(doc)
        print(structure)

        doc.visit(func=self._process_token)

    def test_sentence_without_semicolon(self):
        text = """This sentence does not have a semicolon and stops with a dot."""

        tree = self.parser.invoke(text, action=ParserAction.PASS2)

        tokens = self.interpreter.invoke(tree)
        doc = Ste100Doc(tokens)
        structure = self.inspector.ste100doc(doc)
        print(structure)

        doc.visit(func=self._process_token)
