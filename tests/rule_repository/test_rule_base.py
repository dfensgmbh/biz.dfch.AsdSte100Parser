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

import unittest

from biz.dfch.asdste100vocab import Vocab, Word, WordCategory, WordSource, WordStatus, WordType

from biz.dfch.ste100parser import GrammarType, Inspector, Parser
from biz.dfch.ste100parser.rule_registry import RuleContext, RuleRegistry, RuleResult, TextUtils
from biz.dfch.ste100parser.serializer.text_interpreter import TextInterpreter
from biz.dfch.ste100parser.serializer.token_base import TokenBase
from biz.dfch.ste100parser.token_registry import TokenRegistry


class TestRuleBase(unittest.TestCase):

    RULE_PACKAGE_PATH = "biz.dfch.ste100parser.rule_repository"

    rule_results: list[RuleResult]

    parser: Parser
    vocab: Vocab
    interpreter: TextInterpreter
    inspector: Inspector
    token_registry: TokenRegistry
    rule_context: RuleContext
    rule_registry: RuleRegistry

    def setUp(self) -> None:
        self.rule_results = []
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
        self.rule_context = RuleContext(
            self.vocab, self.token_registry, TextUtils())
        self.rule_registry = RuleRegistry()
        self.rule_registry.install_rules(self.RULE_PACKAGE_PATH)

    def _process_token(self, token: TokenBase, level: int) -> bool:
        _ = level
        print(f"[{type(token).__name__}] Processing token '{token.text}' ...")
        rules = self.rule_registry.get_rules(token)
        for rule in rules:
            print(
                f"Processing rule '{rule.rule_id}' [{rule.priority}] [{type(token).__name__}] ...")
            rule_results = rule.examine(token, self.rule_context)
            for test_result in rule_results:
                print(
                    f"[{test_result.severity}] {test_result.rule_id}: '{test_result.message}'")
            self.rule_results.extend(rule_results)
        return True
