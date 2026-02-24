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

"""Ste100Doc class."""

from __future__ import annotations

from typing import Iterator

from lark import Tree

from .char import Char
from .nlp.spacy_nlp import SpacyNlp
from .serializer.text_interpreter import TextInterpreter
from .serializer.token_base import TokenBase


class Ste100Doc:
    """
    This is a doc representation of text.
    """

    _items: list[TokenBase]
    _nlp: SpacyNlp

    @staticmethod
    def from_parse_tree(tree: Tree) -> Ste100Doc:
        assert isinstance(tree, Tree), type(tree)

        interpreter = TextInterpreter()
        tokens = interpreter.invoke(tree)

        result = Ste100Doc(tokens)
        return result

    def __init__(self, items: list[TokenBase]) -> None:
        assert isinstance(items, list)

        self._items = items

        self._nlp = SpacyNlp.Factory.get_instance()

    def __iter__(self) -> Iterator[TokenBase]:
        """This is an iterator over the tokens in the document."""

        return iter(self._items)

    def __len__(self) -> int:
        """Return the number of tokens in the document."""
        return len(self._items)

    def get_token(self, index: int) -> TokenBase:
        """Get token by index.

        Args:
            index: Integer index or slice object.

        Returns:
            Single token if index is int, list of tokens if index is slice.

        Raises:
            IndexError: If index is out of range.
        """

        return self._items[index]

    def __getitem__(self, index: int | slice) -> TokenBase | list[TokenBase]:
        """Get token by index or slice.

        Args:
            index: Integer index or slice object.

        Returns:
            Single token if index is int, list of tokens if index is slice.

        Raises:
            IndexError: If index is out of range.
        """
        return self._items[index]

    def __setitem__(self, index: int, value: TokenBase) -> None:
        """Set token at specific index.

        Args:
            index: Integer index.
            value: TokenBase object to set.

        Raises:
            IndexError: If index is out of range.
        """
        self._items[index] = value

    def __delitem__(self, index: int | slice) -> None:
        """Delete token by index or slice.

        Args:
            index: Integer index or slice object.
        """
        del self._items[index]

    def __contains__(self, item: TokenBase) -> bool:
        """Check if a token is in the document.

        Args:
            item: TokenBase object to find.

        Returns:
            True if token is found, False otherwise.
        """
        return item in self._items

    def append(self, token: TokenBase) -> None:
        """Add a token to the end of the document.

        Args:
            token: TokenBase object to add.
        """
        self._items.append(token)

    def insert(self, index: int, token: TokenBase) -> None:
        """Insert a token at a specific position.

        Args:
            index: Position to insert the token.
            token: TokenBase object to insert.
        """
        self._items.insert(index, token)

    def remove(self, token: TokenBase) -> None:
        """Remove the first occurrence of a token.

        Args:
            token: TokenBase object to remove.

        Raises:
            ValueError: If token is not found in the document.
        """
        self._items.remove(token)

    def pop(self, index: int = -1) -> TokenBase:
        """Remove and return token at index.

        Args:
            index: Index of token to remove (default: -1, last token).

        Returns:
            The removed token.

        Raises:
            IndexError: If index is out of range.
        """
        return self._items.pop(index)

    def clear(self) -> None:
        """Remove all tokens from the document."""
        self._items.clear()

    def count(self, token: TokenBase) -> int:
        """Count occurrences of a token.

        Args:
            token: TokenBase object to count.

        Returns:
            Number of occurrences.
        """
        return self._items.count(token)

    def extend(self, tokens: list[TokenBase]) -> None:
        """Add multiple tokens to the end of the document.

        Args:
            tokens: List of TokenBase objects to add.
        """
        self._items.extend(tokens)
