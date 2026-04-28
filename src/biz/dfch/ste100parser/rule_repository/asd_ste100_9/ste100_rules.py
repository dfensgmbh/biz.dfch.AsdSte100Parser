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
    R4_3 = "Use a vertical list for complex texts."
    R4_3_SUGGESTION = (
        "When you make a vertical list: "
        "Put a colon (:) at the end of the first sentence, before the first item in the vertical list. "
        "Identify each item in the vertical list with a number, letter, punctuation mark, or symbol. "
        "Start each item in the vertical list with an uppercase letter. "
        "Where applicable, use an article before the noun that is the subject of each item in the vertical list. "
        "Put a period at the end of an item in the vertical list if it is a full sentence. "
        "Do not put a period at the end of an item in the vertical list if it is not a full sentence. "
        "Do not put a comma or a semicolon at the end of an item in the vertical list. "
        "Put a period at the end of the last item in the vertical list."
    )

    R4_3_SUGGESTION_01_START_COLON = "When you make a vertical list, put a colon (:) at the end of the first sentence, before the first item in the vertical list."
    R4_3_SUGGESTION_02_IDENTIFY = "When you make a vertical list, identify each item in the vertical list with a number, letter, punctuation mark, or symbol. "
    R4_3_SUGGESTION_03_UPPERCASE = "When you make a vertical list, start each item in the vertical list with an uppercase letter. "
    R4_3_SUGGESTION_04_ARTICLE = "When you make a vertical list, where applicable, use an article before the noun that is the subject of each item in the vertical list. "
    R4_3_SUGGESTION_05_PERIOD = "When you make a vertical list, put a period at the end of an item in the vertical list if it is a full sentence. "
    R4_3_SUGGESTION_06_NO_PERIOD = "When you make a vertical list, do not put a period at the end of an item in the vertical list if it is not a full sentence. "
    R4_3_SUGGESTION_07_NO_COMMA_OR_SEMICOLON = "When you make a vertical list, do not put a comma or a semicolon at the end of an item in the vertical list. "
    R4_3_SUGGESTION_08_END_PERIOD = "When you make a vertical list, put a period at the end of the last item in the vertical list."
    R4_3_SUGGESTION_09_SAME_MARKER = "When you make a vertical list, use the same marker."
    R4_3_SUGGESTION_10_SAME_INDENT = "When you make a vertical list, use the same indentation and do not make nested lists."

    # Procedural writing
    R5_3 = "Write instructions in the imperative (command) form."

    # Descriptive writing
    R6_6 = "[{count}] Make sure that no paragraph has more than six sentences."
    R6_6_SUGGESTION = (
        "Paragraphs divide a text into logical units and help keep the reader's attention. "
        "If paragraphs are too long, they cannot have this function. "
        "Do not put different topics in the same paragraph. "
        "If a paragraph has more than six sentences, divide it into two smaller paragraphs. "
        "This structure will make your text easier to read."
    )

    # Safety instructions

    # Punctuation and word count
    R8_1 = "The semicolon (;) is not permitted in STE because it lets you write very long sentences. It is also not easy to use correctly. As an alternative to the semicolon, always write two different sentences."

    # Writing Practices
