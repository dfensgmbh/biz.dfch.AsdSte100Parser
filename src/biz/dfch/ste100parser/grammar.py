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

"""STE100 grammar."""

GRAMMAR = """
start: sentence (SPACE sentence)*
sentence: word COMMA? (SPACE word)* EOS_MID
first_word: characters_upper characters_lower*
word: characters+ | int | fp
characters_upper: "A".."Z"
characters_lower: "a".."z"
characters: ( characters_upper | characters_lower )+
SPACE: " "
hyphen: "-"
EOS: "." | "!" | "?"
EOS_MID: EOS | ":"
COMMA: ","

digit: "0" .. "9"
uint: digit+
int: "-"? uint
fp: ("0" | int) "." uint
"""
