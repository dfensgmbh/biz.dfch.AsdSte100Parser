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

"""multipass_transformer module."""

import unittest

from biz.dfch.asdste100vocab import Vocab
from biz.dfch.asdste100vocab import Word
from biz.dfch.asdste100vocab import WordStatus
from biz.dfch.asdste100vocab import WordType

from biz.dfch.ste100parser import GrammarType
from biz.dfch.ste100parser import Inspector
from biz.dfch.ste100parser import Parser
from biz.dfch.ste100parser import ParserAction
from biz.dfch.ste100parser import Ste100Doc
from biz.dfch.ste100parser.serializer.text_interpreter import TextInterpreter


class TestMultiPassTransformer(unittest.TestCase):

    text = """# Topmost "heading line" (with parentheses)

## Procedural Writing

A) This is work step A. And we have 2 sentences:
 * Vertical list item 1. There are 2 sentences.
 * This is another vertical list item.
 * The last (3) vertical list item.
CAUTION: Safety instruction. 2 sentences.
B) Work step B
WARNING: This is a *safety* instruction (with parentheses).
C) When you open the oven, make sure that you do not burn your skin. Do it in this order:
  1 Put on protective gear. A heat resistant glove gives best protection.
  2 Set the switch of the oven to 'OFF'.
  3 Carefully, open the door.
CAUTION: This is a `safety` instruction without parentheses.
D) Open the smooth-rounded self-inflating door.
E) The last work step (E).

## Descriptive Writing

Paragraph with a NOTE. And in this paragraph we have more than one sentence. This sentence starts a list:
 1 First list item
 2 This is another list item that is a full sentence.
 3 The last list item.
The paragraph continues after the vertical list.
NOTE: This is a note. And this note has more than one sentence (this is sentence 2).

## Lorem ipsum

Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
Mauris vel arcu at enim elementum porttitor. 
Duis ante purus, condimentum eu nulla quis, molestie pharetra est. 
Proin sed mattis libero. 
Maecenas lacinia sem nec hendrerit pulvinar. 
Suspendisse ante nulla, mattis ut justo vel, pharetra finibus tortor. 
Aliquam ullamcorper malesuada ultricies. 
Nullam lacinia, ligula vel ultricies rutrum, lorem libero luctus neque, ut feugiat est justo vel sapien. 
Etiam suscipit mi vel sollicitudin vestibulum. 
Mauris feugiat volutpat quam sed venenatis. 
Praesent sit amet nunc volutpat lacus eleifend ornare. 
"""

    def test_pass1(self):
        text = self.text
        parser = Parser(GrammarType.ASD_STE100_9)
        tree = parser.invoke(text, action=ParserAction.PASS1)
        print(tree.pretty())

    def test_pass2(self):
        text = self.text
        parser = Parser(GrammarType.ASD_STE100_9)
        tree = parser.invoke(text, action=ParserAction.PASS2)
        print(tree.pretty())

    def test_pass2_and_interpret(self):
        text = self.text
        parser = Parser(GrammarType.ASD_STE100_9)
        tree = parser.invoke(text, action=ParserAction.PASS2)
        print(tree.pretty())

        vocab = Vocab()
        vocab.append(word=Word(
            name="eenie-weenie",
            status=WordStatus.APPROVED,
            type_=WordType.TECHNICAL_NOUN,
        ))
        interpreter = TextInterpreter(vocab=vocab)
        tokens = interpreter.invoke(tree)
        doc = Ste100Doc(tokens)
        inspector = Inspector()
        structure = inspector.ste100doc(doc)
        print(structure)
