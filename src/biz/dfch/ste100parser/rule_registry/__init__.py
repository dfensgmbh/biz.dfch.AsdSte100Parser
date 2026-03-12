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

from .rule_base import rule
from .rule_base import RuleBase
from .rule_context import RuleContext
from .rule_priority import RulePriority
from .rule_registry import RuleRegistry
from .rule_result import RuleResult
from .rule_result_severity import RuleResultSeverity
from .text_utils import TextUtils

__all__ = [
    "rule",
    "RuleBase",
    "RuleContext",
    "RulePriority",
    "RuleRegistry",
    "RuleResult",
    "RuleResultSeverity",
    "TextUtils",
]
