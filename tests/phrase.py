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

"""phrase"""

from enum import StrEnum


class Phrase(StrEnum):
    """Test phrases."""

    DQUOTE = '''"d quoted text"'''
    DQUOTE_START = '''"d quoted text" at the start.'''
    DQUOTE_END = '''This is "d quoted text"'''
    DQUOTE_DOT = """This is "d quoted text"."""
    DQUOTE_QUESTION = """This is "d quoted text"?"""
    DQUOTE_EXCL = """This is "d quoted text"!"""
    DQUOTE_COMMA = """This is "d quoted text","""
    DQUOTE_COLON = """This is "d quoted text":"""

    SQUOTE = """'s quoted text'"""
    SQUOTE_START = """'s quoted text' at the start."""
    SQUOTE_END = """This is 's quoted text'"""
    SQUOTE_DOT = """This is 's quoted text'."""
    SQUOTE_QUESTION = """This is 's quoted text'?"""
    SQUOTE_EXCL = """This is 's quoted text'!"""
    SQUOTE_COMMA = """This is 's quoted text',"""
    SQUOTE_COLON = """This is 's quoted text':"""
