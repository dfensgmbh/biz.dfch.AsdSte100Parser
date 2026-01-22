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

"""test_case_container_base"""

from biz.dfch.ste100parser import GrammarType, Parser
from biz.dfch.ste100parser.transformer import ContainerTransformer
from biz.dfch.ste100parser.transformer import TokenConverter
from tests.test_case_base import TestCaseBase


class TestCaseContainerBase(TestCaseBase):

    _parser = None

    transformer: ContainerTransformer
    converter: TokenConverter

    @classmethod
    def setUpClass(cls) -> None:
        if cls._parser is None:
            cls._parser = Parser(GrammarType.CONTAINER)

    def setUp(self):
        """Initialize fresh transformer and converter for every test."""
        # self.transformer = ContainerTransformer(log=True)
        self.transformer = ContainerTransformer()
        self.converter = TokenConverter()

    def invoke(self, value: str):
        return self._parser.invoke(value)  # type: ignore

    def transform(self, parse_tree):
        return self.transformer.transform(parse_tree)  # type: ignore
