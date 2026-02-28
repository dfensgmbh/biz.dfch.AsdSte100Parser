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

# flake8: noqa: E501
# pylint: disable=C0115
# pylint: disable=C0301
# pylint: disable=R0903

"""
Ste100 examples.
"""

from enum import StrEnum


class Ste100Examples:
    class R5DOT3(StrEnum):
        DESC_IMP1_STE = "Set the switch to ON."
        DESC_IMP2_STE = "Remove the four bolts."
        DESC_IMP3_STE = "Increase the pressure to 60 psi."
        DESC_IMP4_STE = "Inflate the tires."
        DESC_IMP5_STE = "Install the new O-ring. "

        PROC_IMP1_STE = "A) Set the switch to ON."
        PROC_IMP2_STE = "A) Remove the four bolts."
        PROC_IMP3_STE = "A) Increase the pressure to 60 psi."
        PROC_IMP4_STE = "A) Inflate the tires."
        PROC_IMP5_STE = "A) Install the new O-ring. "

        PROC_IMP6_NONSTE = "A) The test can be continued."
        PROC_IMP6_STE = "Continue the test."

        PROC_IMP7_NONSTE = "A) Oil and grease are to be removed with a degreasing agent."
        PROC_IMP7_STE = "A) Remove oil and grease with a degreasing agent."

        PROC_IMP8A_NONSTE = "A) Before you remove the clamp, you must disconnect the hose."
        PROC_IMP8A_STE = "A) Before you remove the clamp, disconnect the hose."

        PROC_IMP8B_NONSTE = "A) Before you remove the clamp, you must disconnect the hose."
        PROC_IMP8B_STE = "WARNING: IF YOU MUST CUT THE WIRE, ALWAYS USE A PROTECTIVE MASK. PIECES OF WIRES CAN CAUSE INJURY."
