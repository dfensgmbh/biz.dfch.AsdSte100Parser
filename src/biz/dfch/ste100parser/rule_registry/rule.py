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

# pylint: disable=R0903

"""Rule class."""

from abc import ABC, abstractmethod
from typing import Generic
from typing import TypeVar


from .rule_context import RuleContext
from .rule_priority import RulePriority
from .test_result import TestResult

from ..serializer.token_base import TokenBase


def rule(
    rule_id: str,
    token_types: list[type],
    priority: int = RulePriority.DEFAULT,
    is_disabled: bool = False
):
    """This is the decorator for a rule."""
    def decorator(cls):
        cls.rule_id = rule_id
        cls.token_types = token_types
        cls.priority = priority
        cls.is_disabled = is_disabled
        return cls
    return decorator


T = TypeVar("T", bound=TokenBase)


class Rule(ABC, Generic[T]):
    """This is the base class for all rules."""
    rule_id: str
    token_types: list[type]
    priority: int
    is_disabled: bool

    @abstractmethod
    def examine(
        self,
        token: T,
        context: RuleContext
    ) -> list[TestResult]:
        """Examine the specified node and make sure it agrees to the rule."""

        assert isinstance(
            token, tuple(self.token_types)), f"{self.rule_id}: [{type(token)}]"
        assert isinstance(context, RuleContext), type(context)
