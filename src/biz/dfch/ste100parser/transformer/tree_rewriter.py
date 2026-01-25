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
# pylint: disable=R0903
# pylint: disable=W0212
# type: ignore

"""tree_rewriter"""

from lark import Tree


class TreeRewriter:
    """Rewrites a Lark Tree based on specified rules."""

    def invoke(self, children: list, rules: list) -> list:
        """Rewrites the children based ony rules."""

        assert isinstance(children, list)
        assert isinstance(rules, list)

        i = 0
        while i < len(children):
            for pattern, replacer, do_again in rules:
                pattern_length = len(pattern)

                if i + pattern_length > len(children):
                    continue

                segment = children[i:i + pattern_length]

                if all(
                    isinstance(node, Tree) and token.name == node.data
                    for node, token in zip(segment, pattern)
                ):
                    new_segment = replacer(*segment)
                    if isinstance(new_segment, list):
                        children[i:i + pattern_length] = new_segment
                    else:
                        children[i:i + pattern_length] = [new_segment]

                    if not do_again:
                        i += 1
                    break
            else:
                i += 1

        return children
