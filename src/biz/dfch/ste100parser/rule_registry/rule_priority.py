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

"""RulePriority class."""

from enum import IntEnum


class RulePriority(IntEnum):
    """The execution priority of a `Rule`."""

    LOWEST = -0x7F
    LOWER = -0x55
    MEDIUM_LOW = -0x2B
    MEDIUM = 0x00
    MEDIUM_HIGH = 0x2B
    HIGHER = 0x55
    HIGHEST = 0x7F

    DEFAULT = MEDIUM
