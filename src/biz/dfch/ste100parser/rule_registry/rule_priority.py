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
    HIGHEST = 1023
    HIGHER = 768
    MEDIUM = 512
    MEDIUM_HIGH = MEDIUM + 128
    MEDIUM_LOW = MEDIUM - 128
    LOWER = 256
    LOWEST = 0
    DEFAULT = MEDIUM_LOW
