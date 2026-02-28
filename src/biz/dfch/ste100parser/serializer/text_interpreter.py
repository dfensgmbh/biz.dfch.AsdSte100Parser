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

"""TextInterpreter class."""

from __future__ import annotations

from enum import auto, IntFlag

from lark import ParseTree, Tree, Discard
from lark.visitors import Interpreter

from biz.dfch.asdste100vocab import Vocab

from ..char import Char as Character
from ..note_or_safety_keyword import NoteOrSafetyKeyword
from ..token_registry import TokenRegistry

from .span import Span
from .token_base import TokenBase
from .token_base import TokenRoot
from .token_base import Paragraph
from .token_base import ProcItem
from .token_base import Sentence

from .token_base import NoteOrSafetyInstruction
from .token_base import Code
from .token_base import CodeBlock
from .token_base import Text
from .token_base import Word
from .token_base import Number
from .token_base import Char
from .token_base import Punct
from .token_base import Ws
from .token_base import LineBreak

from .token_base import Parentheses
from .token_base import Format
from .token_base import Quote
from .token_base import QuoteType

from .token_factory import TokenFactory
from .token_factory import from_lark_meta


class Exclude(IntFlag):
    """Define flags to word extraction."""
    NONE = 0
    HEADING = auto()
    PARA = auto()
    PROC = auto()
    PAREN = auto()
    PAREN_TOK = auto()
    PAREN_ALL = PAREN | PAREN_TOK
    SQUOTE = auto()
    SQUOTE_TOK = auto()
    DQUOTE = auto()
    DQUOTE_TOK = auto()
    CITE = auto()
    QUOTE = SQUOTE | DQUOTE | CITE
    QUOTE_TOK = SQUOTE_TOK | DQUOTE_TOK
    QUOTE_ALL = QUOTE | QUOTE_TOK
    BOLD = auto()
    EMPH = auto()
    BOLD_EMPH = auto()
    FORMAT = BOLD | EMPH | BOLD_EMPH
    LIST_ITEM = auto()
    NOTE = auto()
    SAFETY = auto()
    CODE = auto()
    CODE_TOK = auto()
    CODE_BLOCK = auto()
    CODE_ALL = CODE | CODE_BLOCK
    TEXT = auto()
    WORD = auto()
    NUMBER = auto()
    PLURAL = auto()
    APOSTROPHE = auto()
    YEAR_SHORT = auto()
    TEXT_SPECIAL = (
        PLURAL |
        APOSTROPHE |
        YEAR_SHORT)
    TEXT_ALL = TEXT_SPECIAL | TEXT | WORD | NUMBER
    LINEBREAK = auto()


class TextInterpreter(Interpreter):  # pylint: disable=R0904
    """This moves through the tree from top to bottom."""

    _parent: list[TokenBase]
    _vocab: Vocab
    _token_registry: TokenRegistry

    def __init__(self, vocab: Vocab | None = None) -> None:
        super().__init__()

        self._parent = []
        self._token_registry = TokenRegistry.Factory.get_instance()
        if vocab is None:
            self._vocab = Vocab(use_ste100=False)
        else:
            assert isinstance(vocab, Vocab), type(vocab)
            self._vocab = vocab

    def invoke(self, tree: ParseTree | list) -> list[TokenBase]:
        """
        Docstring for invoke

        :param tree: Description
        :type tree: ParseTree
        :return: Description
        :rtype: list[TokenBase]
        """
        assert isinstance(tree, (Tree, list)), type(tree)

        if isinstance(tree, Tree):
            visited: list[TokenBase] = self.visit(tree)
        else:
            assert isinstance(tree, list)
            visited: list[TokenBase] = []
            for child in tree:
                visited.extend(self.visit(child))

        result: list[TokenBase] = self.make_flat_list(visited)

        return result

    def make_flat_list(self, items: list) -> list[TokenBase]:
        """
        The result of a `visit` or `visit_children` operation is a list. Every
        user function in the interpreter returns a `list[TokenBase]`. This
        method flattens the result and returns a single list of `TokenBase`.

        :param items: This is a list of `TokenBase` items.
        :type items: list[TokenBase]
        :return: A flat list of `TokeBase` items.
        :rtype: list[TokenBase]
        """
        assert isinstance(items, list), type(items)

        result: list[TokenBase] = []

        for item in items:
            assert isinstance(item, (list, TokenBase))
            if isinstance(item, list):
                for nested_item in item:
                    assert isinstance(nested_item, TokenBase), type(nested_item)
                result.extend(item)
            else:
                result.append(item)

        return result

    def __default__(self, tree) -> list[TokenBase]:
        assert isinstance(tree, Tree), type(tree)

        if hasattr(tree.meta, "line"):
            span = from_lark_meta(tree.meta)
        else:
            span = Span.default()

        raise NotImplementedError(
            f"'{tree.data}' {span}"
        )

    def start(self, tree) -> list[TokenBase]:

        result = TokenFactory.TokenRoot(
            meta=tree.meta,
            tokens=[],
        )
        self._token_registry.add_or_update(ste100=result, lark=tree)
        self._parent.append(result)
        result.tokens = self._get_items(tree.children)

        return [result]

    def heading(self, tree) -> list[TokenBase]:
        assert isinstance(tree, Tree), type(tree)

        level_tree, *remaining = tree.children
        assert isinstance(level_tree, Tree), type(level_tree)
        assert 1 == len(level_tree.children), len(level_tree.children)
        level = level_tree.children[0]
        assert isinstance(level, str), type(level)
        assert level.isdigit(), level

        result = TokenFactory.Heading(
            meta=tree.meta,
            parent=self._parent[-1] if self._parent else None,  # type: ignore
            tokens=[],
            level=int(level),
        )
        self._token_registry.add_or_update(ste100=result, lark=tree)
        self._parent.append(result)
        result.tokens = self._get_items(remaining)
        self._parent.pop()

        return [result]

    def HEADING_LEVEL(self, _) -> list[TokenBase]:
        return Discard  # type: ignore

    def paragraph(self, tree) -> list[TokenBase]:
        assert isinstance(tree, Tree), type(tree)

        result = TokenFactory.Paragraph(
            meta=tree.meta,
            parent=self._parent[-1] if self._parent else None,  # type: ignore
            tokens=[],
        )
        self._token_registry.add_or_update(ste100=result, lark=tree)
        self._parent.append(result)
        result.tokens = self._get_items(tree.children)
        self._parent.pop()

        return [result]

    def sentence(self, tree) -> list[TokenBase]:
        assert isinstance(tree, Tree), type(tree)

        result = TokenFactory.Sentence(
            meta=tree.meta,
            parent=self._parent[-1] if self._parent else None,  # type: ignore
            tokens=[],
        )
        self._token_registry.add_or_update(ste100=result, lark=tree)
        self._parent.append(result)
        result.tokens = self._get_items(tree.children)
        self._parent.pop()

        return [result]

    def proc_item(self, tree) -> list[TokenBase]:
        assert isinstance(tree, Tree), type(tree)

        step_tree, delimiter_tree, *remaining = tree.children

        assert isinstance(step_tree, Tree)
        assert 1 == len(step_tree.children)
        step = step_tree.children[0]
        assert isinstance(step, str)

        assert isinstance(delimiter_tree, Tree)
        assert 1 == len(delimiter_tree.children)
        delimiter = delimiter_tree.children[0]
        assert isinstance(delimiter, str)

        print(
            f"[step '{step}'] ["
            f"delimiter '{delimiter}'] "
            f"[remaining #{len(remaining)}]"
        )

        result = TokenFactory.ProcItem(
            meta=tree.meta,
            parent=self._parent[-1] if self._parent else None,  # type: ignore
            tokens=[],
            step=step,
            delimiter=delimiter,
        )
        self._token_registry.add_or_update(ste100=result, lark=tree)
        self._parent.append(result)
        result.tokens = self._get_items(remaining)
        self._parent.pop()

        return [result]

    def list_item(self, tree) -> list[TokenBase]:
        assert isinstance(tree, Tree), type(tree)

        indent_tree, marker_tree, *remaining = tree.children

        assert isinstance(indent_tree, Tree)
        assert 1 == len(indent_tree.children)
        indent = indent_tree.children[0]
        assert isinstance(indent, str)
        assert indent.isdigit(), indent

        assert isinstance(marker_tree, Tree)
        assert 1 == len(marker_tree.children)
        marker = marker_tree.children[0]
        assert isinstance(marker, str)
        assert marker.isalnum() or marker in (
            Character.MULTIPLY, Character.HYPHEN), marker

        result = TokenFactory.ListItem(
            meta=tree.meta,
            parent=self._parent[-1],
            tokens=[],
            indent=int(indent),
            marker=marker,
        )
        self._token_registry.add_or_update(ste100=result, lark=tree)
        self._parent.append(result)
        result.tokens = self._get_items(remaining)
        self._parent.pop()

        return [result]

    def WARNING(self, tree) -> list[TokenBase]:
        return self._note_or_safety_instruction(
            tree, NoteOrSafetyKeyword.WARNING)

    def CAUTION(self, tree) -> list[TokenBase]:
        return self._note_or_safety_instruction(
            tree, NoteOrSafetyKeyword.CAUTION)

    def NOTE(self, tree) -> list[TokenBase]:
        return self._note_or_safety_instruction(
            tree, NoteOrSafetyKeyword.NOTE)

    def _note_or_safety_instruction(
        self,
        tree,
        keyword: NoteOrSafetyKeyword
    ) -> list[TokenBase]:
        assert isinstance(tree, Tree), type(tree)
        assert isinstance(keyword, str), type(keyword)

        result = TokenFactory.NoteOrSafetyInstruction(
            meta=tree.meta,
            parent=self._parent[-1],
            keyword=keyword,
            tokens=[],
        )
        self._token_registry.add_or_update(ste100=result, lark=tree)
        self._parent.append(result)
        result.tokens = self._get_items(tree.children)
        self._parent.pop()

        return [result]

    def _get_items(self, remaining: list) -> list[TokenBase]:

        assert isinstance(remaining, list)
        assert 0 < len(remaining), len(remaining)

        result = []
        for item in remaining:
            assert isinstance(item, Tree), type(item)
            visited = self.visit(item)
            if isinstance(visited, list):
                result.extend(visited)
            elif visited is not None:
                result.append(visited)

        return result

    def TEXT(self, tree) -> list[TokenBase]:
        assert isinstance(tree, Tree), type(tree)
        assert 1 == len(tree.children), len(tree.children)
        value = tree.children[0]
        assert isinstance(value, str), type(value)
        assert 0 < len(value)

        is_in_vocab = any(
            word for word in self._vocab if word.name.lower() == value.lower())
        if is_in_vocab:
            result = TokenFactory.Word(
                meta=tree.meta,
                parent=self._parent[-1],
                value=value,
            )
            self._token_registry.add_or_update(ste100=result, lark=tree)
            return [result]

        text, punct = value[:-1], value[-1]
        if punct in (
            Character.DOT, Character.COMMA,
            Character.EXCLAMATION, Character.QUESTION,
            Character.COLON, Character.SEMICOLON,
        ):
            # When a punctuation follows parentheses or quotes or formatters,
            # the TEXT token consists of only one character.
            result = []
            if 0 != len(text):
                result.append(
                    TokenFactory.Text(
                        meta=tree.meta,
                        parent=self._parent[-1],
                        value=text,
                    ),
                )
            result.append(
                TokenFactory.Punct(
                    meta=tree.meta,
                    parent=self._parent[-1],
                    value=punct,
                ),
            )
            return result

        try:
            _ = float(value)
            result = TokenFactory.Number(
                meta=tree.meta,
                parent=self._parent[-1],
                value=str(value),
            )
            self._token_registry.add_or_update(ste100=result, lark=tree)
            return [result]
        except ValueError:
            pass

        result = TokenFactory.Text(
            meta=tree.meta,
            parent=self._parent[-1],
            value=value,
        )
        self._token_registry.add_or_update(ste100=result, lark=tree)

        return [result]

    def APOSTROPHE(self, tree) -> list[TokenBase]:
        assert isinstance(tree, Tree), type(tree)
        assert 1 == len(tree.children), len(tree.children)
        value = tree.children[0]
        assert isinstance(value, str), type(value)

        result = TokenFactory.Apostrophe(
            meta=tree.meta,
            parent=self._parent[-1],
            value=value,
        )
        self._token_registry.add_or_update(ste100=result, lark=tree)

        return [result]

    def CHAR(self, tree) -> list[TokenBase]:
        assert isinstance(tree, Tree), type(tree)
        assert 1 == len(tree.children), len(tree.children)
        value = tree.children[0]
        assert isinstance(value, str), type(value)

        result = TokenFactory.Char(
            meta=tree.meta,
            parent=self._parent[-1],
            value=value,
        )
        self._token_registry.add_or_update(ste100=result, lark=tree)

        return [result]

    def WS(self, tree) -> list[TokenBase]:
        # (f"TextInterpreter.WS")
        assert isinstance(tree, Tree), type(tree)
        assert 1 == len(tree.children), len(tree.children)
        value = tree.children[0]
        assert isinstance(value, str), type(value)
        assert value.isdigit(), value

        result = TokenFactory.Ws(
            meta=tree.meta,
            parent=self._parent[-1],
            value=int(value) * Character.SPACE,
        )
        self._token_registry.add_or_update(ste100=result, lark=tree)

        return [result]

    def PLURAL_S(self, tree) -> list[TokenBase]:
        assert isinstance(tree, Tree), type(tree)

        result = TokenFactory.Plural(
            meta=tree.meta,
            parent=self._parent[-1],
        )
        self._token_registry.add_or_update(ste100=result, lark=tree)

        return [result]

    def MULTIPLY(self, tree) -> list[TokenBase]:
        assert isinstance(tree, Tree), type(tree)

        result = TokenFactory.Multiply(
            meta=tree.meta,
            parent=self._parent[-1],
        )
        self._token_registry.add_or_update(ste100=result, lark=tree)

        return [result]

    def LINEBREAK(self, tree) -> list[TokenBase]:
        assert isinstance(tree, Tree), type(tree)

        result = TokenFactory.LineBreak(
            meta=tree.meta,
            parent=self._parent[-1],
        )
        self._token_registry.add_or_update(ste100=result, lark=tree)

        return [result]

    def NEWLINE(self, tree) -> list[TokenBase]:
        assert isinstance(tree, Tree), type(tree)

        span = from_lark_meta(tree.meta)
        raise NotImplementedError(
            "LogicError: NEWLINE is not permitted at this point in text. "
            f"{span}"
        )

    def dquote(self, tree) -> list[TokenBase]:
        assert isinstance(tree, Tree), type(tree)

        result = TokenFactory.Dquote(
            meta=tree.meta,
            parent=self._parent[-1],
            tokens=[],
        )
        self._token_registry.add_or_update(ste100=result, lark=tree)
        self._parent.append(result)
        result.tokens = self._get_items(tree.children)
        self._parent.pop()

        return [result]

    def squote(self, tree) -> list[TokenBase]:
        assert isinstance(tree, Tree), type(tree)

        result = TokenFactory.Squote(
            meta=tree.meta,
            parent=self._parent[-1],
            tokens=[],
        )
        self._token_registry.add_or_update(ste100=result, lark=tree)
        self._parent.append(result)
        result.tokens = self._get_items(tree.children)
        self._parent.pop()

        return [result]

    def cite(self, tree) -> list[TokenBase]:
        assert isinstance(tree, Tree), type(tree)

        result = TokenFactory.Cite(
            meta=tree.meta,
            parent=self._parent[-1],
            tokens=[],
        )
        self._token_registry.add_or_update(ste100=result, lark=tree)
        self._parent.append(result)
        result.tokens = self._get_items(tree.children)
        self._parent.pop()

        return [result]

    def bold(self, tree) -> list[TokenBase]:
        assert isinstance(tree, Tree), type(tree)

        result = TokenFactory.Bold(
            meta=tree.meta,
            parent=self._parent[-1],
            tokens=[],
        )
        self._token_registry.add_or_update(ste100=result, lark=tree)
        self._parent.append(result)
        result.tokens = self._get_items(tree.children)
        self._parent.pop()

        return [result]

    def emph(self, tree) -> list[TokenBase]:
        assert isinstance(tree, Tree), type(tree)

        result = TokenFactory.Emph(
            meta=tree.meta,
            parent=self._parent[-1],
            tokens=[],
        )
        self._token_registry.add_or_update(ste100=result, lark=tree)
        self._parent.append(result)
        result.tokens = self._get_items(tree.children)
        self._parent.pop()

        return [result]

    def bold_emph(self, tree) -> list[TokenBase]:
        assert isinstance(tree, Tree), type(tree)

        result = TokenFactory.BoldEmph(
            meta=tree.meta,
            parent=self._parent[-1],
            tokens=[],
        )
        self._token_registry.add_or_update(ste100=result, lark=tree)
        self._parent.append(result)
        result.tokens = self._get_items(tree.children)
        self._parent.pop()

        return [result]

    def CODE(self, tree) -> list[TokenBase]:
        assert isinstance(tree, Tree), type(tree)
        assert 1 == len(tree.children), len(tree.children)
        value = tree.children[0]
        assert isinstance(value, str), type(value)

        result = TokenFactory.Code(
            meta=tree.meta,
            parent=self._parent[-1],
            value=value,
        )
        self._token_registry.add_or_update(ste100=result, lark=tree)

        return [result]

    def code_block(self, tree) -> list[TokenBase]:
        assert isinstance(tree, Tree), type(tree)
        assert 2 == len(tree.children), len(tree.children)

        language_tree = tree.children[0]
        assert isinstance(language_tree, Tree), type(language_tree)
        assert 1 == len(language_tree.children), len(language_tree.children)
        language = language_tree.children[0]
        assert isinstance(language, str)

        value_tree = tree.children[1]
        assert isinstance(value_tree, Tree), type(value_tree)
        assert 1 == len(value_tree.children), len(value_tree.children)
        value = value_tree.children[0]
        assert isinstance(value, str)

        result = TokenFactory.CodeBlock(
            meta=tree.meta,
            parent=self._parent[-1],
            value=value,
            language=language,
        )
        self._token_registry.add_or_update(ste100=result, lark=tree)

        return [result]

    def paren(self, tree) -> list[TokenBase]:
        assert isinstance(tree, Tree), type(tree)

        result = TokenFactory.Parentheses(
            meta=tree.meta,
            parent=self._parent[-1] if self._parent else None,  # type: ignore
            tokens=[],
        )
        self._token_registry.add_or_update(ste100=result, lark=tree)
        self._parent.append(result)
        result.tokens = self._get_items(tree.children)
        self._parent.pop()

        return [result]

    def is_next_token_ws(
        self,
        tokens: list[TokenBase],
        i: int,
    ) -> bool:
        assert isinstance(tokens, list), type(tokens)

        next_idx = i + 1
        if next_idx == len(tokens):
            return False

        token = tokens[next_idx]
        return isinstance(token, Ws)

    def extract_words(
        self,
        tokens: list[TokenBase],
        *,
        exclude: Exclude,
    ) -> tuple[
        list[str],
        list[bool],
        list[TokenBase],
        list[bool],
    ]:
        assert isinstance(tokens, list), type(tokens)
        assert isinstance(exclude, Exclude), type(exclude)

        assert 0 < len(tokens)
        assert isinstance(tokens, list)

        words: list[str] = []
        spaces: list[bool] = []
        source: list[TokenBase] = []
        sents: list[bool] = []

        def process_white_space(_):
            return

        def process_list_token(token):
            nested = self.extract_words(
                token.tokens, exclude=exclude)
            words.extend(nested[0])
            spaces.extend(nested[1])
            source.extend(nested[2])
            sents.extend(nested[3])

        def process_parentheses(token):
            if Exclude.PAREN_TOK not in exclude:
                words.append(Character.PAREN_OPEN.value)
                spaces.append(False)
                source.append(token)
                sents.append(0 == i)

            if Exclude.PAREN not in exclude:
                nested = self.extract_words(
                    token.tokens, exclude=exclude)
                words.extend(nested[0])
                spaces.extend(nested[1])
                source.extend(nested[2])
                sents.extend(nested[3])

            if Exclude.PAREN_TOK not in exclude:
                words.append(Character.PAREN_CLOSE.value)
                spaces.append(self.is_next_token_ws(tokens, i))
                source.append(token)
                sents.append(0 == i)

        def process_quote(token):
            quote_char: str | None = None
            if QuoteType.SINGLE == token.type_:
                quote_char = Character.SQUOTE.value
            elif QuoteType.DOUBLE == token.type_:
                quote_char = Character.DQUOTE.value

            if (
                QuoteType.DOUBLE == token.type_ and
                Exclude.DQUOTE_TOK not in exclude or
                QuoteType.SINGLE == token.type_ and
                Exclude.SQUOTE_TOK not in exclude
            ):
                if quote_char is not None:
                    words.append(quote_char)
                    spaces.append(self.is_next_token_ws(tokens, i))
                    source.append(token)
                    sents.append(0 == i)

            if not any(
                f in exclude for f in (
                    Exclude.SQUOTE, Exclude.DQUOTE, Exclude.CITE)):
                nested = self.extract_words(
                    token.tokens, exclude=exclude)
                words.extend(nested[0])
                spaces.extend(nested[1])
                source.extend(nested[2])
                sents.extend(nested[3])

            if (
                QuoteType.DOUBLE == token.type_ and
                Exclude.DQUOTE_TOK not in exclude or
                QuoteType.SINGLE == token.type_ and
                Exclude.SQUOTE_TOK not in exclude
            ):
                if quote_char is not None:
                    words.append(quote_char)
                    spaces.append(self.is_next_token_ws(tokens, i))
                    source.append(token)
                    sents.append(0 == i)

        def process_value_token(token):
            words.append(token.text)
            spaces.append(self.is_next_token_ws(tokens, i))
            source.append(token)
            sents.append(0 == i)

        mappings = {
            Ws: process_white_space,
            LineBreak: process_white_space,
            Text: process_value_token,
            Word: process_value_token,
            Char: process_value_token,
            Punct: process_value_token,
            Number: process_value_token,
            TokenRoot: process_list_token,
            Paragraph: process_list_token,
            ProcItem: process_list_token,
            # Heading: process_list_token,
            Format: process_list_token,
            Code: process_value_token,
            CodeBlock: process_value_token,
            Parentheses: process_parentheses,
            Quote: process_quote,
            NoteOrSafetyInstruction: process_list_token,
            Sentence: process_list_token,
        }

        for i, token in enumerate(tokens):

            mapping = mappings.get(type(token))
            assert mapping is not None, type(token)
            mapping(token)

        print(words)
        assert len(words) == len(spaces)
        assert len(words) == len(source)
        assert len(words) == len(sents)

        return words, spaces, source, sents
