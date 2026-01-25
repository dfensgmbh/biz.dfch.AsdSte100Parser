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

# pylint: disable=C0115
# pylint: disable=C0116

"""test_case_text_base"""

from biz.dfch.ste100parser import GrammarType, Parser
from biz.dfch.ste100parser.transformer import ContainerTransformer
from biz.dfch.ste100parser.transformer import TextTransformer
from biz.dfch.ste100parser.transformer import TokenConverter

from tests.test_case_base import TestCaseBase


class TestCaseTextBase(TestCaseBase):

    _parser = None

    pass1_transformer: ContainerTransformer
    transformer: TextTransformer
    converter: TokenConverter

    @classmethod
    def setUpClass(cls) -> None:
        if cls._parser is None:
            cls._parser = Parser(GrammarType.CONTAINER)

    def setUp(self):
        """Initialize fresh transformer and converter for every test."""
        self.pass1_transformer = ContainerTransformer()
        # self.transformer = TextTransformer(log=True)
        self.transformer = TextTransformer()
        self.converter = TokenConverter()

    def invoke(self, value: str):
        return self._parser.invoke(value)  # type: ignore

    def transform(self, parse_tree):
        pass1 = self.pass1_transformer.transform(parse_tree)
        return self.transformer.transform(pass1)  # type: ignore
