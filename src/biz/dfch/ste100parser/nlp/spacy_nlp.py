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

"""SpacyNlp class."""

from __future__ import annotations

from enum import StrEnum
from threading import Lock
from typing import ClassVar

import spacy
from spacy.language import Language
from spacy.tokens import Doc
from spacy.tokens import Token
from spacy.util import registry
from spacy.vocab import Vocab  # pylint: disable=E0611

from biz.dfch.asdste100vocab.vocab import Vocab as Ste100Vocab
from .word_matcher import WordMatcher


class SpacyExtension(StrEnum):
    """spaCy extensions."""

    ste100_doc = "ste100_doc"
    ste100_token = "ste100_token"


@registry.misc("load_vocabulary.v1")
def load_vocabulary():
    return Ste100Vocab()


@Language.factory("word_matcher")
def word_matcher_factory(nlp, name, vocab):
    assert isinstance(nlp, Language), type(nlp)
    assert isinstance(name, str), type(name)
    assert name.strip()
    assert isinstance(vocab, Ste100Vocab), type(vocab)

    pipeline = WordMatcher(vocab)

    return pipeline


# @Language.component("word_matcher")
# def word_matcher(doc: Doc) -> Doc:
#     assert isinstance(doc, Doc), type(doc)

#     return doc


class SpacyNlp:  # pylint: disable=R0903
    """A wrapper for spaCy NLP."""

    _model_name: str
    _nlp: Language

    vocab: Vocab

    @staticmethod
    def _register_ste100_extensions() -> None:
        if not Doc.has_extension(SpacyExtension.ste100_doc):
            Doc.set_extension(SpacyExtension.ste100_doc, default=None)
        if not Token.has_extension(SpacyExtension.ste100_token):
            Token.set_extension(SpacyExtension.ste100_token, default=None)

    def __init__(self, model_name: str) -> None:
        assert isinstance(model_name, str), type(model_name)
        assert model_name.strip()

        self._model_name = model_name
        self._nlp = spacy.load(self._model_name)
        self.vocab = self._nlp.vocab
        self.ste100_vocab = Ste100Vocab()
        self.vocab = self._nlp.vocab

        SpacyNlp._register_ste100_extensions()

    def __call__(self, text: str | Doc) -> Doc:
        assert isinstance(text, (str, Doc)), type(text)

        if isinstance(text, Doc):
            return self._nlp(text)

        assert text.strip()
        return self._nlp(text)

    class Factory:  # pylint: disable=R0903
        """Singleton factory."""

        _model_name: ClassVar[str] = "en_core_web_sm"
        _lock: ClassVar[Lock] = Lock()
        _instance: ClassVar[SpacyNlp | None] = None

        @classmethod
        def get_instance(cls) -> SpacyNlp:
            if cls._instance is not None:
                return cls._instance
            with cls._lock:
                if SpacyNlp.Factory._instance is not None:
                    assert isinstance(cls._instance, SpacyNlp)
                    return cls._instance
                cls._instance = SpacyNlp(SpacyNlp.Factory._model_name)
                return cls._instance
