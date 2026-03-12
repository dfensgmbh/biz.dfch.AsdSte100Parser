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

"""Rule repository."""

# flake8: noqa: E501
# pylint: disable=C0301

from enum import StrEnum


class Ste100Rules(StrEnum):
    """These are the rules from ASD-STE100 Issue 9."""

    # Words
    R1_1 = "Use words that are: Approved in the dictionary, Technical nouns, Technical verbs."

    # Multi-word nouns

    # Verbs
    R3_6 = "Use the active voice. In descriptive writing, you can use the passive voice only when the agent is unknown."

    # Sentences

    # Procedural writing
    R5_3 = "Write instructions in the imperative (command) form."

    # Descriptive writing

    # Safety instructions

    # Punctuation and word count
    R8_1 = "The semicolon (;) is not permitted in STE because it lets you write very long sentences. It is also not easy to use correctly. As an alternative to the semicolon, always write two different sentences."

    # Writing Practices
