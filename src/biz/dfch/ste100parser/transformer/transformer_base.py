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

# pylint: disable=C0116
# type: ignore

"""containers_transformer"""

from dataclasses import dataclass

from lark import Transformer, Tree

from ..token import Token
from ..token_metrics import TokenMetrics

__all__ = [
    "TransformerBase",
]


@dataclass
class TransformerConfiguration():
    """TransformerConfiguration"""

    log: bool = False


class TransformerBase(Transformer):
    """TransformerBase"""

    _cfg: TransformerConfiguration
    _metrics: TokenMetrics | None

    def __init__(
        self,
        metrics: TokenMetrics | None = None,
        cfg: TransformerConfiguration = TransformerConfiguration(),
        log: bool = False,
        visit_tokens: bool = True
    ) -> None:

        super().__init__(visit_tokens)

        assert isinstance(cfg, TransformerConfiguration)
        self._cfg = cfg
        if log:
            self._cfg.log = log

        if isinstance(metrics, TokenMetrics):
            self._metrics = metrics
        else:
            self._metrics = TokenMetrics()

    @property
    def metrics(self) -> TokenMetrics:
        return self._metrics

    def print(self, children, data: str = '') -> None:
        """Prints the token and its children."""

        if not self._cfg.log:
            return

        print(f"#{len(children)} [{data}]: '{children}'.")
        # for i, child in enumerate(children):
        #     print(f"#{i}: '{child}' [{type(child)}]")

    def __default__(self, data, children, meta):
        # data = the rule name (e.g., "squote", "bold", "emph")
        # children = the list of children
        # meta = metadata (line/column info)

        self.print(f"__default__: '{data}' [{meta}].")

        result = Tree(data=data, children=children, meta=meta)
        self._metrics.append(Token.default)

        return result
