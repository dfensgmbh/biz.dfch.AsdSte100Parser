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

from biz.dfch.ste100parser.token_registry import TokenRegistry
from biz.dfch.ste100parser.serializer.token_base import Sentence
from biz.dfch.ste100parser.serializer.token_base import Span


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
