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

"""Token enum."""

# pylint: disable=C0103

from enum import StrEnum, auto

__all__ = [
    "Token",
]


class Token(StrEnum):
    """Token definitions."""

    default = auto()

    start = auto()
    inline = auto()

    squote = auto()
    dquote = auto()
    paren = auto()

    cite = auto()

    CODE = auto()
    bold = auto()
    emph = auto()
    bold_emph = auto()

    MULTIPLY = auto()

    WS = auto()
    SPACE = auto()

    NEWLINE = auto()
    LINEBREAK = auto()
    TEXT = auto()
    CHAR = auto()
    APOSTROPHE = auto()
    YEAR_SHORT = auto()

    proc_item = auto()
    PROC_STEP = auto()
    PROC_DELIMITER = auto()

    heading = auto()
    HEADING_LEVEL = auto()

    paragraph = auto()

    LIST_MARKER = auto()
    LIST_INDENT = auto()
    list_item = auto()

    NOTE = auto()
    WARNING = auto()
    CAUTION = auto()
    NOTE_OR_SAFETY_MARKER = auto()
