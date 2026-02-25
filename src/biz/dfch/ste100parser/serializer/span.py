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

# pylint: disable=C0103
# pylint: disable=C0116
# pylint: disable=W0212

"""Span class."""

from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class Span:
    """
    A `Span` represents the location and length of a textual object.

    Attributes:
        line (int): The line number where the span starts.
        column (int): The column number on the specified line where the span
            starts.
        start_pos (int): The starting position of the span within its context
            or container.
        end_pos (int): The ending position of the span within its context or
            container.
    """

    line: int
    column: int
    start_pos: int
    end_pos: int

    @staticmethod
    def default() -> Span:
        return Span(
            line=0,
            column=1,
            start_pos=1,
            end_pos=1,
        )

    def __str__(self) -> str:
        return f"[{self.line}:{self.column}] @ " \
            f"[{self.start_pos}:{self.end_pos}]"

    def __repr__(self) -> str:
        return str(self)
