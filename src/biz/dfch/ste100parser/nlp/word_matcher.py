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

from spacy.tokens import Doc, Span

from biz.dfch.asdste100vocab import Vocab
from biz.dfch.asdste100vocab import WordType


class WordMatcher:
    """
    Make a word from the STE100 vocabulary into relation of a spaCy token.
    """

    _vocab: Vocab

    pos_map: dict[str, list[WordType]] = {
        "VERB": [WordType.VERB, WordType.TECHNICAL_VERB],
        "AUX": [WordType.VERB],
        "ADP": [WordType.PREPOSITION],
        "NOUN": [WordType.NOUN, WordType.TECHNICAL_NOUN],
        "X": [WordType.UNKNOWN],
    }

    def __init__(self, vocab: Vocab) -> None:
        assert isinstance(vocab, Vocab), type(vocab)

        self._vocab = Vocab()

    def _process_sentence(self, sent: Span) -> None:
        assert isinstance(sent, Doc), type(sent)

    def __call__(self, doc: Doc) -> Doc:
        """
        Make a word from the STE100 vocabulary into relation of a spaCy token.
        """
        assert isinstance(doc, Doc), type(doc)

        for sent in doc.sents:
            self._process_sentence(sent)

        return doc
