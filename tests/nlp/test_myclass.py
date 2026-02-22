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

# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116
# pylint: disable=C0301

"""nlp tests"""

from typing import cast
import unittest

from spacy.language import Language
from spacy.tokens import Doc, Token

from biz.dfch.asdste100vocab import Vocab
from biz.dfch.asdste100vocab import Word
from biz.dfch.asdste100vocab import WordCategory
from biz.dfch.asdste100vocab import WordStatus
from biz.dfch.asdste100vocab import WordType

from biz.dfch.ste100parser import Char
from biz.dfch.ste100parser import Parser
from biz.dfch.ste100parser import ParserAction
from biz.dfch.ste100parser import GrammarType
from biz.dfch.ste100parser.ste100doc import Ste100Doc
from biz.dfch.ste100parser.inspector import Inspector
from biz.dfch.ste100parser.token_map import TokenMap

from biz.dfch.ste100parser.nlp import SpacyNlp

from biz.dfch.ste100parser.serializer.token_base import TokenBase
from biz.dfch.ste100parser.serializer.token_base import TokenRoot
from biz.dfch.ste100parser.serializer.token_base import ListToken
from biz.dfch.ste100parser.serializer.token_base import Paragraph
from biz.dfch.ste100parser.serializer.token_base import Sentence
from biz.dfch.ste100parser.serializer.token_base import Text
from biz.dfch.ste100parser.serializer.token_base import Parentheses
from biz.dfch.ste100parser.serializer.token_base import Punct
from biz.dfch.ste100parser.serializer.token_base import Number
from biz.dfch.ste100parser.serializer.token_base import Ws
from biz.dfch.ste100parser.serializer.token_base import Format
from biz.dfch.ste100parser.serializer.token_base import Quote
from biz.dfch.ste100parser.serializer.token_base import QuoteType
from biz.dfch.ste100parser.serializer.token_factory import TokenFactory
from biz.dfch.ste100parser.serializer.token_factory import from_lark_meta
from biz.dfch.ste100parser.serializer.text_interpreter import TextInterpreter
from biz.dfch.ste100parser.serializer.text_interpreter import Exclude


def is_possible_eos(abbrev: Token, min_token: int, max_token: int) -> bool:

    assert isinstance(abbrev, Token), type(abbrev)
    assert isinstance(min_token, int) and 0 <= min_token
    assert isinstance(max_token, int) and 0 <= max_token

    # When the abbreviation is not within both tokens, it is not end-of-sentence.
    if False == min_token < abbrev.i < max_token:
        return False

    # When there is a token dependency after our abbreviation, it is not end-of-sentence.
    return not abbrev.head.i > abbrev.i


def find_eos_token_index(abbrevs: list[Token], min_token: int, max_token: int) -> int | None:

    assert isinstance(abbrevs, list), type(abbrevs)
    assert isinstance(min_token, int) and 0 <= min_token
    assert isinstance(max_token, int) and 0 <= max_token

    candidates: dict[int, bool] = {}
    for abbrev in abbrevs:
        candidates[abbrev.i] = is_possible_eos(abbrev, min_token, max_token)

    if not any(c for c in candidates.values() if True is c):
        print("Nothing found. Trying reverse order.")
        candidates.clear()
        for abbrev in abbrevs:
            candidates[abbrev.i] = is_possible_eos(
                abbrev, max_token, min_token)  # pylint: disable=W1114

    if not any(c for c in candidates.values() if True is c):
        print("No candidates found.")
        return None

    result = max(candidates, key=candidates.__getitem__)
    return result


@Language.component("before_parser")
def before_parser(doc: Doc) -> Doc:
    assert isinstance(doc, Doc), type(Doc)

    if 0 < len(doc):
        doc[0].is_sent_start = True

    return doc


@Language.component("after_parser")
def after_parser(doc: Doc) -> Doc:
    assert isinstance(doc, Doc), type(Doc)

    DOT = Char.DOT

    for i, token in enumerate(doc):
        print(f"[{i}] {token.text, token.pos_, token.dep_}")

    abbrevs = [token for token in doc if token.text !=
               DOT and token.text.endswith(DOT)]
    if not any(abbrevs) or 0 >= len(abbrevs):
        print("#### no abbrevs")
        return doc

    roots = [token for token in doc if token.dep_ == "ROOT"]
    if not any(roots) or 1 != len(roots):
        print("#### no roots")
        return doc

    root = roots[0]
    print(f"root: '{root.text}' [{root.i}]")
    assert isinstance(root, Token), type(root)

    print([(t.text, t.i, t.pos_, t.head, t.head.i) for t in doc])
    print([(t.text, t.i, t.head, t.head.i)
          for t in doc if t.pos_ in ("VERB", "AUX")])
    print([(t.text, t.i, t.head, t.head.i)
          for t in doc if t.head.i == root.i and t.i != root.i])
    candidates = [t for t in doc if t.head.i ==
                  root.i and t.pos_ in ("VERB", "AUX") and t.i != root.i]
    print(f"candidates: '{candidates}'")
    if not any(candidates) or 1 != len(candidates):
        print("#### no candidates")
        return doc

    candidate = candidates[0]
    print(f"NewRoot: '{(candidate.i, candidate.text)}'")
    print(f"Root: '{(root.i, root.text)}'")

    return doc


def get_child_of_container(
    token: TokenBase,
    container_token: TokenBase,
) -> TokenBase | None:
    assert isinstance(token, TokenBase), type(token)
    assert isinstance(container_token, TokenBase), type(container_token)

    while token.parent is not None:
        if token.parent is container_token:
            return token
        token = token.parent

    return None


class TestInspector(unittest.TestCase):

    def test_inspector_full(self):
        text = r"""*This* _is_ an *in-flight* *_text_* from the U.K. """ \
            r"""with (something in) parentheses. """ \
            r"""And here is another sentence """ \
            r"""(*which* does not make sense (sic!)). """

        vocab = Vocab(use_ste100=True)
        vocab.append(Word(
            name="U.K.",
            status=WordStatus.APPROVED,
            type_=WordType.NOUN,
            source="custom001",
            category=WordCategory.ROLES_GROUPS,
        ))
        vocab.append(Word(
            name="in-flight",
            status=WordStatus.APPROVED,
            type_=WordType.ADJECTIVE,
            source="custom001",
            category=WordCategory.VEHICLES_MACHINES,
        ))
        parser = Parser(GrammarType.ASD_STE100_9)
        tree = parser.invoke(text, action=ParserAction.PASS2)

        interpreter = TextInterpreter(vocab)
        tokens = interpreter.invoke(tree)
        # We start at Paragraph
        tokens = tokens[0].tokens  # type: ignore
        container_token = tokens[0]
        self.assertIsInstance(tokens, list)
        self.assertTrue(0 < len(tokens))
        print("#### 1")
        print(tokens)

        ste100doc = Ste100Doc(tokens)
        token_map = TokenMap()
        inspect = Inspector()
        print(inspect.ste100doc(ste100doc, token_map))


class TestMyClass(unittest.TestCase):
    def test_sth(self):
        text = r"""London is the capital of the U.K. And they have the Tower of London."""
        text = r"""Calibration of the resistance of the runway light connection is important."""
        text = r"""To extinguish a possible fire, portable fire extinguishers are installed in these areas: ..."""
        text = r"""To extinguish a possible fire, portable fire extinguishers are installed in the crew rest compartment."""
        text = r"""London is the capital of the U.K. Very often, it rains there."""
        text = r"""Make sure that the EMER pushbutton switch is released (the EMER legend is off)."""
        text = r"""To extinguish a possible fire, portable fire extinguishers are installed in the sub-compartment."""
        text = r"""First sentence. This is a "100.5" % _version_ of the *in-flight* sentence (or term (A)) in the U.K. And this starts a list:
"""
        text = r"""The door is made of "carbon-fiber-reinforced plastic" (see figure A1), too."""
        text = r"""This is a *fully complete* sentence. The door is made of "carbon-fiber-reinforced 'plastic'" (see figure A1), too."""
        text = r"""(This is a sentence in parentheses (a1).)"""
        text = r"""(This is a sentence in parentheses.)"""
        text = r"""This is text with (something in) parentheses. Lorem ipsum dolor sit amet."""
        text = r"""This is text with parentheses. Lorem ipsum dolor sit amet."""
        text = r"""*This* _is_ an *in-flight* *_text_* from the U.K. with (something in) parentheses. And here is another sentence (*which* does not make sense (sic!)). """

        vocab = Vocab(use_ste100=True)
        vocab.append(Word(
            name="U.K.",
            status=WordStatus.APPROVED,
            type_=WordType.NOUN,
            source="custom001",
            category=WordCategory.ROLES_GROUPS,
        ))
        vocab.append(Word(
            name="in-flight",
            status=WordStatus.APPROVED,
            type_=WordType.ADJECTIVE,
            source="custom001",
            category=WordCategory.VEHICLES_MACHINES,
        ))
        parser = Parser(GrammarType.ASD_STE100_9)
        tree = parser.invoke(text, action=ParserAction.PASS2)

        print(tree.pretty())

        interpreter = TextInterpreter(vocab)
        tokens = interpreter.invoke(tree)
        # We start at Paragraph
        tokens = tokens[0].tokens  # type: ignore
        container = tokens[0]
        self.assertIsInstance(tokens, list)
        self.assertTrue(0 < len(tokens))
        print("#### 1")
        print(tokens)

        ste100doc = Ste100Doc(tokens)
        token_map = TokenMap()
        inspect = Inspector()
        print(inspect.ste100doc(ste100doc, token_map))
        words, spaces, source, sents = interpreter.extract_words(
            tokens,
            exclude=Exclude.PAREN,
        )
        nlp = SpacyNlp.Factory.get_instance()
        print(f"Start nlp. [items: #{len(words)}]")
        doc = Doc(nlp.vocab, words=words, spaces=spaces)
        doc._.ste100_doc = ste100doc
        for spacy_token, ste_token in zip(doc, source, strict=True):
            spacy_token._.ste100_token = ste_token
        doc = nlp(doc)

        k = -1
        sentences = []
        for i, sent in enumerate(doc.sents):
            sent_text_tokens = []
            for j, token in enumerate(sent):
                k += 1
                ste_token = cast(TokenBase, token._.ste100_token)
                sent_text_tokens.append(ste_token)
                sent_container = ste_token.parent
                print(
                    f"[{i}/{j}/{k}] "
                    f"{token.text, token.pos_, token.dep_, type(ste_token).__name__, type(sent_container).__name__} "
                    f"[i:{token_map[ste_token]:02}][p:{token_map[sent_container]:02}]"
                )
                # print(f"[{i}/{j}/{k}] '{token.is_sent_start}'")
                # print(f"[{i}/{j}/{k}] {token.is_sent_end}'")

            sent_start_token = get_child_of_container(
                sent_text_tokens[0], container)
            assert sent_start_token is not None
            print(
                f"Container '{container.text}' [{type(container).__name__}] [i:{token_map[container]:02}] [p:{token_map[container.parent]:02}]")
            print(
                f"SentStart '{sent_start_token.text}' [{type(sent_start_token).__name__}] [i:{token_map[sent_start_token]:02}] [p:{token_map[sent_start_token.parent]:02}]")

            sentence = Sentence(
                sent_start_token.span, container, [])  # type: ignore

            first = token_map[sent_start_token]
            last = token_map[sent_text_tokens[-1]]
            idx = container.tokens.index(sent_start_token)
            container.tokens.insert(idx, sentence)
            to_be_removed = []
            for t in container.tokens:
                assert isinstance(t, TokenBase), type(t)

                if token_map[t] == token_map[sentence]:
                    continue
                if token_map[t.parent] == token_map[sentence]:
                    continue

                idx = token_map[t]
                if not first <= idx <= last:
                    print(
                        f"Skip token '{t.text}' [{type(t).__name__}] [i:{token_map[t]:02}] [p:{token_map[t.parent]:02}]")
                    continue

                print(f"[{first} <= {idx} <= {last}]")
                print(
                    f"Token '{t.text}' [{type(t).__name__}] [i:{token_map[t]:02}] [p:{token_map[t.parent]:02}]")

                t.parent = sentence
                sentence.tokens.append(t)
                to_be_removed.append(t)

            for t in to_be_removed:
                container.tokens.remove(t)

            sentences.append(sentence)

        print(inspect.ste100doc(Ste100Doc(tokens), token_map))
