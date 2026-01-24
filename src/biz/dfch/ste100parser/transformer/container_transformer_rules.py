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

"""container_transformer_rules"""

from lark import Tree
from lark.tree import Meta

from biz.dfch.ste100parser.token import Token


class ContainerTransformerRules:
    """
    Rules for ContainerTransformer start.

    These rules removed NEWLINE between different rules.
    """

    @classmethod
    def get_rules(cls):
        return [
            (
                [Token.NEWLINE, Token.NEWLINE, Token.heading],
                lambda n1, n2, h: h,
                True,
            ),
            (
                [Token.NEWLINE, Token.cite],
                lambda n, c: c,
                True,
            ),
            (
                [Token.NEWLINE, Token.heading],
                lambda n, h: h,
                True,
            ),
            (
                [Token.NEWLINE, Token.NEWLINE, Token.paragraph],
                lambda n1, n2, p: p,
                True,
            ),
            (
                [Token.heading, Token.NEWLINE],
                lambda h, n1: h,
                True,
            ),
            (
                [Token.cite, Token.NEWLINE],
                lambda c, n1: c,
                True,
            ),
            (
                [Token.proc_item, Token.NEWLINE, Token.NEWLINE, Token.paragraph],  # noqa: E501
                lambda proc, n1, n2, para: [proc, para],
                False,
            ),
            (
                [Token.proc_item, Token.NEWLINE, Token.NOTE],
                lambda proc, n, note: [proc, note],
                False,
            ),
            (
                [Token.proc_item, Token.NEWLINE, Token.paragraph],
                lambda proc, n, para: [proc, para],
                False,
            ),
            (
                [Token.paragraph, Token.NEWLINE, Token.proc_item],
                lambda para, n, proc: [para, proc],  # noqa: E501
                True,
            ),
            (
                [Token.paragraph, Token.NEWLINE, Token.paragraph],
                cls.process_paragraph_newline_paragraph,
                True,
            ),
            (
                [Token.paragraph, Token.paragraph],
                cls.process_paragraph_paragraph,  # noqa: E501
                True,
            ),
            (
                [Token.paragraph, Token.NEWLINE, Token.NEWLINE],
                lambda para, n1, n2: para,  # noqa: E501
                False,
            ),
            (
                [Token.proc_item, Token.NEWLINE, Token.NEWLINE],
                lambda proc, n1, n2: proc,  # noqa: E501
                False,
            ),
            (
                [Token.NOTE, Token.NEWLINE, Token.NEWLINE],
                lambda note, n1, n2: note,  # noqa: E501
                False,
            ),
        ]

    @classmethod
    def process_paragraph_newline_paragraph(
        cls,
        para1: Tree,
        newline: Tree,
        para2: Tree
    ) -> Tree:

        assert isinstance(newline, Tree)

        return cls.process_paragraph_paragraph(para1, para2)

    @classmethod
    def process_paragraph_paragraph(
        cls,
        para1: Tree,
        para2: Tree
    ) -> Tree:
        assert isinstance(para1, Tree)
        assert isinstance(para2, Tree)

        meta = Meta()
        meta.line = para1.meta.line
        meta.column = para1.meta.column
        meta.start_pos = para1.meta.start_pos
        meta.end_pos = para2.meta.end_pos

        result = Tree(
            Token.paragraph.name,
            para1.children + para2.children,
            meta=para1.meta,
        )

        return result
