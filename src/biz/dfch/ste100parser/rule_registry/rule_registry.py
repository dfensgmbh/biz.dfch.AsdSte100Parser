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

"""RuleRegistry class."""

from collections import defaultdict
import importlib
import inspect
import pkgutil

from ..serializer.token_base import TokenBase

from .rule_base import RuleBase


class RuleRegistry:
    """Install rules from a package."""

    _rules: dict[type, list[RuleBase]]

    def __init__(self) -> None:

        self._rules = defaultdict(list)

    def install_rules(self, path: str):
        """Install `Rule` classes from specified `path`."""

        assert isinstance(path, str), type(path)
        assert path.strip()

        package = importlib.import_module(path)
        for _, name, _ in pkgutil.walk_packages(package.__path__):
            full_name = f"{path}.{name}"
            print(f"Import module '{full_name}'.")
            module = importlib.import_module(full_name)

            for _, t in inspect.getmembers(module, inspect.isclass):
                if not issubclass(t, RuleBase) or inspect.isabstract(t):
                    continue
                if not hasattr(t, 'token_types'):
                    continue
                instance = t()
                if instance.is_disabled:
                    continue
                for type_ in instance.token_types:
                    print(
                        f"[{type_.__name__}] "
                        f"Installing rule '{instance.rule_id}: "
                        f"{t.__name__}' [{full_name}]"
                    )
                    self._rules[type_].append(instance)

    def get_rules(self, token: TokenBase) -> list[RuleBase]:
        """Get rules for specified `token`."""

        result = []

        for t, rules in self._rules.items():
            if not isinstance(token, t):
                continue
            result.extend(rules)

        return sorted(result, key=lambda e: e.priority, reverse=True)
