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

"""grammar_type"""

from enum import StrEnum


class GrammarType(StrEnum):
    """STE100 defined grammars."""

    DEFAULT = "default.lark"
    NUMBER = "number.lark"
    INT = "integer.lark"
    FP = "fp.lark"
    WORD = "word.lark"
    CONTAINER = "container.lark"
