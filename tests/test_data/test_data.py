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

"""test_data"""

from enum import StrEnum


class TestData(StrEnum):
    """Test data file names."""

    SINGLE_PARAGRAPH = "single_paragraph.md"
    SINGLE_PARAGRAPH_WITH_LINEBREAK = "single_paragraph_with_linebreak.md"

    COMPLEX_HEADINGS_PARA_PROC_LIST = "complex_headings_para_proc_list.md"
    COMPLEX_HEADINGS_PROC_CITE_PARA_LIST = "complex_heading_proc_cite_para_list.md"

    LIST_IN_PARAGRAPH = "list_in_paragraph.md"
    LIST_IN_PROC = "list_in_proc.md"
