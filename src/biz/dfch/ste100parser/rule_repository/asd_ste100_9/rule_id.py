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

"""STE100 rule ids."""

from enum import StrEnum


class RuleId(StrEnum):
    """This class gives the short identification of STE100 rule names."""

    # Words
    R1_1 = "R1.1"
    R1_2 = "R1.2"
    R1_3 = "R1.3"
    R1_4 = "R1.4"
    R1_5 = "R1.5"
    R1_6 = "R1.6"
    R1_7 = "R1.7"
    R1_8 = "R1.8"
    R1_9 = "R1.9"
    R1_10 = "R1.10"
    R1_11 = "R1.11"
    R1_12 = "R1.12"
    R1_13 = "R1.13"
    R1_14 = "R1.14"

    # Multi-word nouns
    R2_1 = "R2.1"
    R2_2 = "R2.2"

    # Verbs
    R3_1 = "R3.1"
    R3_2 = "R3.2"
    R3_3 = "R3.3"
    R3_4 = "R3.4"
    R3_5 = "R3.5"
    R3_6 = "R3.6"
    R3_7 = "R3.7"

    # Sentences
    R4_1 = "R4.1"
    R4_2 = "R4.2"
    R4_3 = "R4.3"
    R4_4 = "R4.4"
    R4_5 = "R4.5"

    # Procedural writing
    R5_1 = "R5.1"
    R5_2 = "R5.2"
    R5_3 = "R5.3"
    R5_4 = "R5.4"
    R5_5 = "R5.5"

    # Descriptive writing
    R6_1 = "R6.1"
    R6_2 = "R6.2"
    R6_3 = "R6.3"
    R6_4 = "R6.4"
    R6_5 = "R6.5"
    R6_6 = "R6.6"

    # Safety instructions
    R7_1 = "R7.1"
    R7_2 = "R7.2"
    R7_3 = "R7.3"

    # Punctuation and word count
    R8_1 = "R8.1"
    R8_2 = "R8.2"
    R8_3 = "R8.3"
    R8_4 = "R8.4"
    R8_5 = "R8.5"
    R8_6 = "R8.6"
    R8_7 = "R8.7"

    # Writing Practices
    R9_1 = "R9.1"
    R9_2 = "R9.2"
    R9_3 = "R9.3"
    R9_4 = "R9.4"

    GR_1 = "GR-1"
    GR_2 = "GR-2"
    GR_3 = "GR-3"
    GR_4 = "GR-4"
    GR_5 = "GR-5"
    GR_6 = "GR-6"
    GR_7 = "GR-7"
    GR_8 = "GR-8"
