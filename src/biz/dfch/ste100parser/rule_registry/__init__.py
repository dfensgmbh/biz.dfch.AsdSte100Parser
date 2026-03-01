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

"""rules module."""

from .rule import rule
from .rule import Rule
from .rule_context import RuleContext
from .rule_priority import RulePriority
from .rule_registry import RuleRegistry
from .test_result import TestResult
from .test_result_severity import TestResultSeverity
from .text_utils import TextUtils

__all__ = [
    "rule",
    "Rule",
    "RuleContext",
    "RulePriority",
    "RuleRegistry",
    "TestResult",
    "TestResultSeverity",
    "TextUtils",
]
