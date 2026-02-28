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

"""TokenRegistry class."""

from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock
from typing import ClassVar

from lark import Tree
from spacy.tokens import Span, Token

from .serializer.token_base import TokenBase


class TokenRegistry:
    """
    A registry that creates a relation between these items:
      * lark Tree items
      * spaCy Token and Spans
      * STE100 tokens (from TokenBase).
    """

    @dataclass
    class Record:
        """A tripe of related tokens."""
        ste100: TokenBase | None = field(init=False, default=None)
        spacy: Span | Token | None = field(init=False, default=None)
        lark: Tree | None = field(init=False, default=None)

    _sync_root: Lock

    _record_map: dict[int, Record]

    _ste100_map: dict[int, int]
    _spacy_map: dict[int, int]
    _lark_map: dict[int, int]

    def __init__(self) -> None:
        self._sync_root = Lock()

        self._record_map = {}

        self._ste100_map = {}
        self._spacy_map = {}
        self._lark_map = {}

    def __str__(self) -> str:
        result = [(r[0], r[1].ste100) for r in self._record_map.items()]
        return str(result)

    def clear(self) -> None:
        """Remove all `Record` from the token registry."""
        with self._sync_root:
            self._record_map.clear()
            self._ste100_map.clear()
            self._spacy_map.clear()
            self._lark_map.clear()

    def remove(
        self,
        record: TokenRegistry.Record
    ) -> TokenRegistry.Record | None:
        """Remove a `Record` from the token registry."""
        assert isinstance(record, TokenRegistry.Record), type(record)

        key = id(record)
        with self._sync_root:
            result = self._record_map.pop(key, None)
            if result is None:
                return result

            if result.ste100 is not None:
                key = id(result.ste100)
                _ = self._ste100_map.pop(key, None)

            if result.spacy is not None:
                key = id(result.spacy)
                _ = self._spacy_map.pop(key, None)

            if result.lark is not None:
                key = id(result.lark)
                _ = self._lark_map.pop(key, None)

            return result

    def update(
        self,
        record: TokenRegistry.Record
    ) -> None:
        """Update a `Record` in the token registry."""
        assert isinstance(record, TokenRegistry.Record), type(record)

        record_id = id(record)
        with self._sync_root:
            result = self._record_map.get(record_id)
            assert isinstance(result, TokenRegistry.Record), type(result)

            if result.ste100 is not None:
                key = id(result.ste100)
                self._ste100_map[key] = record_id

            if result.spacy is not None:
                key = id(result.spacy)
                self._spacy_map[key] = record_id

            if result.lark is not None:
                key = id(result.lark)
                self._lark_map[key] = record_id

    def add_or_update(
        self,
        *,
        ste100: TokenBase | None = None,
        spacy: Span | Token | None = None,
        lark: Tree | None = None,
    ) -> TokenRegistry.Record:
        """Add or update a `Record` in the token registry."""

        with self._sync_root:
            record_id: int | None = None
            if record_id is None and ste100 is not None:
                key = id(ste100)
                record_id = self._ste100_map.get(key)
            if record_id is None and spacy is not None:
                key = id(spacy)
                record_id = self._spacy_map.get(key)
            if record_id is None and lark is not None:
                key = id(lark)
                record_id = self._lark_map.get(key)

            if record_id is None:
                record = self.Record()
                record_id = id(record)
            else:
                record = self._record_map.get(record_id)
                assert record is not None, record_id

            self._record_map[record_id] = record

            if ste100 is not None:
                record.ste100 = ste100
                self._ste100_map[id(ste100)] = record_id
            if spacy is not None:
                record.spacy = spacy
                self._spacy_map[id(spacy)] = record_id
            if lark is not None:
                record.lark = lark
                self._lark_map[id(lark)] = record_id

            return record

    def get_or_default_ste100(
        self,
        token: TokenBase,
        default: Record | None = None,
    ) -> Record | None:
        """Examine if there is an ste100 token in the Token Registry."""
        assert isinstance(token, TokenBase), type(token)

        key = id(token)
        with self._sync_root:
            record_id = self._ste100_map.get(key)
            if record_id is None:
                return default

            result = self._record_map.get(record_id)
            if result is None:
                return default

            assert result.ste100 is not None
            return result

    def get_or_default_spacy(
        self,
        token: Span | Token,
    ) -> TokenRegistry.Record | None:
        """Examine if there is a spacy token in the Token Registry."""
        assert isinstance(token, (Span, Token)), type(token)

        key = id(token)
        with self._sync_root:
            record_id = self._spacy_map.get(key)
            if record_id is None:
                return None

            result = self._record_map.get(record_id)
            if result is None:
                return None

            assert result.spacy is not None
            return result

    def get_or_default_lark(
        self,
        token: Tree,
        default: Record | None = None,
    ) -> Record | None:
        """Examine if there is a lark token in the Token Registry."""
        assert isinstance(token, Tree), type(token)

        key = id(token)
        with self._sync_root:
            record_id = self._lark_map.get(key)
            if record_id is None:
                return default

            result = self._record_map.get(record_id)
            if result is None:
                return default

            assert result.lark is not None
            return result

    # def get_or_add_ste100(
    #     self,
    #     token: TokenBase,
    # ) -> TokenRegistry.Record:
    #     """Get a `Record` from an ste100 token."""
    #     assert isinstance(token, TokenBase), type(token)

    #     key = id(token)
    #     with self._sync_root:
    #         record_id = self._ste100_map.get(key)
    #         if record_id is None:
    #             record = self.Record()
    #             record.ste100 = token
    #             record_id = id(record)
    #             self._ste100_map[key] = record_id
    #             self._record_map[record_id] = record
    #             return record

    #         record = self._record_map.get(record_id)
    #         if record is None:
    #             record = self.Record()
    #             record.ste100 = token

    #         self._record_map[record_id] = record
    #         return record

    # def get_or_add_spacy(
    #     self,
    #     token: Span | Token,
    # ) -> TokenRegistry.Record:
    #     """Get a `Record` from a spaCy token."""
    #     assert isinstance(token, (Span, Token)), type(token)

    #     key = id(token)
    #     with self._sync_root:
    #         record_id = self._spacy_map.get(key)
    #         if record_id is None:
    #             result = self.Record()
    #             result.spacy = token
    #             self._spacy_map[key] = id(result)
    #             return result

    #         result = self._record_map.get(record_id)
    #         if result is None:
    #             result = self.Record()
    #             result.spacy = token

    #         return result

    # def get_or_add_lark(
    #     self,
    #     token: Tree,
    # ) -> Record:
    #     """Get a `Record` from a lark token."""
    #     assert isinstance(token, Tree), type(token)

    #     key = id(token)
    #     with self._sync_root:
    #         record_id = self._lark_map.get(key, None)
    #         if record_id is None:
    #             record = self.Record()
    #             record_id = id(record_id)
    #             record.lark = token
    #             self._lark_map[key] = record_id
    #             self._record_map[record_id] = record
    #             return record

    #         record = self._record_map.get(record_id)
    #         assert record is not None, token
    #         return record

    def remove_ste100(
        self,
        token: TokenBase,
    ) -> Record:
        """Remove a ste100 token from a `Record` in the token registry."""
        assert isinstance(token, TokenBase), type(token)

        key = id(token)
        with self._sync_root:
            record_id = self._ste100_map.pop(key)
            result = self._record_map.get(record_id)
            assert isinstance(result, self.Record), type(result)

            result.ste100 = None

            return result

    def remove_spacy(
        self,
        token: Span | Token,
    ) -> Record:
        """Remove a spacy token from a `Record` in the token registry."""
        assert isinstance(token, (Span, Token)), type(token)

        key = id(token)
        with self._sync_root:
            record_id = self._spacy_map.pop(key)
            result = self._record_map.get(record_id)
            assert isinstance(result, self.Record), type(result)

            result.spacy = None

            return result

    def remove_lark(
        self,
        token: Tree,
    ) -> Record:
        """Remove a lark token from a `Record` in the token registry."""
        assert isinstance(token, Tree), type(token)

        key = id(token)
        with self._sync_root:
            record_id = self._lark_map.pop(key)
            result = self._record_map.get(record_id)
            assert isinstance(result, self.Record), type(result)

            result.lark = None

            return result

    class Factory:  # pylint: disable=R0903
        """Singleton factory."""

        _lock: ClassVar[Lock] = Lock()
        _instance: ClassVar[TokenRegistry | None] = None

        @classmethod
        def get_instance(cls) -> TokenRegistry:
            """Create or get the singleton instance."""

            if cls._instance is not None:
                return cls._instance
            with cls._lock:
                if cls._instance is not None:
                    assert isinstance(cls._instance, TokenRegistry)
                    return cls._instance
                cls._instance = TokenRegistry()
                return cls._instance
