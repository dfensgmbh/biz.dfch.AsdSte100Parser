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

"""char enum."""

# pylint: disable=C0116
# type: ignore

from enum import StrEnum

__all__ = [
    "Char",
]


class Char(StrEnum):
    """Character definitions."""

    EMPTY = ''

    DQUOTE = '"'
    SQUOTE = "'"

    DOT = '.'
    QUESTION = '?'
    EXCLAMATION = '!'
    COMMA = '.'
    COLON = ':'

    PAREN_OPEN = '('
    PAREN_CLOSE = ')'

    STAR = '*'
    UNDER = '_'
    CODE = '`'
    BOLD_EMPH_OPEN = '*_'
    BOLD_EMPH_CLOSE = '_*'

    WS = r"[ \t]+"
    MULTIPLY = '*'
    SPACE = ' '
    TAB = '\t'
    NEWLINE = r"\r?\n"
    LF = "\n"
    TEXT = r"""[^"'*_`\s]+"""
    APOSTROPHE = r"""(?<=[A-Za-z0-9])'(?:s)?(?=[\s.,!?;:]|$)"""
    CHAR_LOWER_S = 's'
    YEAR_SHORT = r"""'\d{2}s?(?=[\s.,!?;:]|$)"""

    HASH = '#'
