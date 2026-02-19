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

from threading import Lock
from typing import ClassVar


import spacy
from spacy.tokens import Doc
from spacy.language import Language


class SpacyNlp:  # pylint: disable=R0903
    """A wrapper for spaCy NLP."""

    _model_name = "en_core_web_sm"

    _nlp: Language

    def __init__(self) -> None:
        self._nlp = spacy.load(SpacyNlp._model_name)

    def __call__(self, text: str) -> Doc:
        assert isinstance(text, str), type(text)
        assert text.strip()

        return self._nlp(text)

    class Factory:  # pylint: disable=R0903
        """Singleton factory."""

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
                cls._instance = SpacyNlp()
                return cls._instance
