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

# pylint: disable=C0116
# pylint: disable=R0903
# pylint: disable=W0212
# type: ignore

"""asd_ste100_9_pass2_transformer_rules"""

from typing import Callable

from lark import Tree

from biz.dfch.ste100parser.token import Token

RuleType = tuple[list[Token], Callable[[..., Tree], Tree | list[Tree]], bool]


class AsdSte1009Pass2TransformerRules:
    """
    Rules for TextTransformer start.

    These rules remove NEWLINE and LINEBREAK between different rules.
    """

    @classmethod
    def get_rules_start(cls) -> list[RuleType]:
        _ = Token.start.name

        return [
        ]
