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

"""test_text_interpreter tests."""

# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116
# pylint: disable=C0301

import unittest

from biz.dfch.ste100parser import GrammarType
from biz.dfch.ste100parser import Parser
from biz.dfch.ste100parser.serializer.sentencizer import Sentencizer


class TestSentencizer(unittest.TestCase):
    def test_init_succeeds(self):

        sut = Sentencizer()

        self.assertIsNotNone(sut)
