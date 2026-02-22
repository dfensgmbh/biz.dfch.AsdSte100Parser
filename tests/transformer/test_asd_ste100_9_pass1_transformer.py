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

"""test_asd_ste100_9_pass1_transformer module."""

import unittest

from biz.dfch.ste100parser import GrammarType
from biz.dfch.ste100parser import Inspector
from biz.dfch.ste100parser import Parser
from biz.dfch.ste100parser import ParserAction
from biz.dfch.ste100parser import Ste100Doc
from biz.dfch.ste100parser.serializer.text_interpreter import TextInterpreter


class TestAsdSte1009Pass1Transformer(unittest.TestCase):

    def test_pass1(self):
        text = """# Topmost heading

A) This is work step A.
 * Vertical list item 1
 * This is another vertical list item.
 * The last (3) vertical list item.
B) Work step B
C) The last work step (C).

"""
        parser = Parser(GrammarType.ASD_STE100_9)
        tree = parser.invoke(text, action=ParserAction.PASS1)
        print(tree.pretty())

    def test_pass2(self):
        text = """### Topmost "heading" (with parentheses)

A) This is work step A. And we have 2 sentences:
 * Vertical list item 1. There are 2 sentences.
 * This is another vertical list item.
 * The last (3) vertical list item.
CAUTION: Safety instruction. 2 sentences.
B) Work step B
WARNING: This is a *safety* instruction (with parentheses).
C) The last work step (C).
CAUTION: This is a `safety` instruction without parentheses.

Paragraph with a NOTE. And in this paragraph we have more than one sentence. This sentence starts a list:
 1 First list item
 2 This is another list item that is a full sentence.
 3 The last list item.
The paragraph continues after the vertical list.
NOTE: This is a note. And this note has more than one sentence (this is sentence 2).
"""
        parser = Parser(GrammarType.ASD_STE100_9)
        tree = parser.invoke(text, action=ParserAction.PASS2)
        print(tree.pretty())

    def test_pass2_and_interpret(self):
        text = """# Topmost "heading" (with parentheses)

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
D) The last work step (D).

## Descriptive Writing

Paragraph with a NOTE. And in this paragraph we have more than one sentence. This sentence starts a list:
 1 First list item
 2 This is another list item that is a full sentence.
 3 The last list item.
The paragraph continues after the vertical list.
NOTE: This is a note. And this note has more than one sentence (this is sentence 2).

## Lorem ipsum

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris vel arcu at enim elementum porttitor. Duis ante purus, condimentum eu nulla quis, molestie pharetra est. Proin sed mattis libero. Maecenas lacinia sem nec hendrerit pulvinar. Suspendisse ante nulla, mattis ut justo vel, pharetra finibus tortor. Aliquam ullamcorper malesuada ultricies. Nullam lacinia, ligula vel ultricies rutrum, lorem libero luctus neque, ut feugiat est justo vel sapien. Etiam suscipit mi vel sollicitudin vestibulum. Mauris feugiat volutpat quam sed venenatis. Praesent sit amet nunc volutpat lacus eleifend ornare. 

Phasellus porta mi quis est hendrerit rhoncus. Phasellus nec nulla quis nibh aliquam dapibus. Mauris luctus augue libero. Nam tempor porta nisl ac venenatis. Maecenas varius ligula ex, a feugiat massa tristique vel. Sed in feugiat sapien, a consequat sem. Vivamus euismod sed lorem quis hendrerit. Duis quis velit eget lorem feugiat ultricies. Nunc finibus interdum diam, non lacinia mauris finibus pharetra. In ultrices placerat arcu, tincidunt aliquet lectus lacinia sed. Mauris ut massa vel orci finibus imperdiet. Morbi orci felis, interdum at blandit vel, semper volutpat libero. Proin lorem tortor, vehicula dignissim mi at, hendrerit accumsan velit. Vestibulum nec felis tortor.

Duis fringilla dolor in justo aliquam semper eget at purus. Curabitur vitae eros enim. Maecenas sit amet urna quis nulla tincidunt faucibus. Cras vulputate a sapien et dignissim. Mauris ut ornare erat, ut gravida arcu. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Etiam elementum tincidunt arcu, vel tempus leo. Suspendisse laoreet turpis ac mi tempus posuere. Ut in erat gravida sapien auctor vestibulum vel sodales nibh. Morbi interdum, est eu imperdiet vestibulum, metus erat venenatis risus, non faucibus lacus erat eu ex. Cras vitae sodales orci. Morbi mattis, nibh at interdum tempus, ante massa fringilla ante, sed volutpat sapien velit ac dui. Nam sit amet congue lectus. Fusce quis blandit augue. Nullam quis gravida quam.

Pellentesque id eros vel velit cursus malesuada. Praesent ut justo dignissim, hendrerit tellus in, accumsan dolor. Aliquam vel quam pulvinar, fringilla dui vitae, varius elit. Ut vel est eu risus tempor molestie nec id urna. Cras congue maximus orci eget lobortis. Fusce metus nisi, aliquet ornare scelerisque vitae, egestas non nisi. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras ut malesuada massa. Vestibulum tempus, est sed iaculis dignissim, augue massa ornare ex, laoreet condimentum urna purus eu lorem. In luctus, lectus eget molestie blandit, tortor dui venenatis tortor, et semper neque metus et nisl. Pellentesque semper ligula ultrices urna vestibulum, eget efficitur turpis condimentum.

Fusce vitae est metus. Donec vehicula tellus eu sem molestie, non rhoncus magna congue. Phasellus pharetra diam eu nisi ornare, nec accumsan urna hendrerit. In at turpis felis. Morbi vulputate, lectus sit amet facilisis volutpat, eros nulla hendrerit purus, id consequat enim odio ut quam. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Fusce porttitor finibus semper. Duis elementum accumsan fermentum. Proin a magna sit amet dui venenatis rhoncus et eget nisi. 

### 10 more paragraphs of 'Lorem ipsum'

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus finibus velit lorem, vel eleifend elit faucibus a. Aenean tempus auctor risus, id porttitor mi efficitur et. Sed suscipit justo aliquet, vestibulum nulla iaculis, aliquam tortor. Etiam bibendum bibendum arcu eu suscipit. Aenean tincidunt justo sit amet vestibulum eleifend. In consequat dolor id arcu pretium, nec varius ipsum semper. Maecenas rhoncus pulvinar bibendum. Ut efficitur rutrum gravida. Etiam velit urna, blandit ornare cursus vitae, convallis id erat. Nunc in libero auctor, fringilla libero a, blandit ex. Maecenas nec efficitur sem.

Nulla nec finibus arcu. Curabitur a erat eu leo finibus bibendum. Ut eget bibendum magna. Suspendisse potenti. Sed lacinia felis justo, quis mollis odio tincidunt eu. Aenean imperdiet enim non erat fermentum ultricies. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Sed suscipit mollis erat, quis posuere lacus. Morbi auctor nisl eu tortor euismod efficitur in vitae ipsum.

Maecenas pretium vestibulum ligula sit amet pretium. Integer ac nisl maximus, vulputate nisi nec, lacinia nisi. Phasellus consectetur erat porttitor consequat sodales. Sed id urna ac turpis dignissim consectetur quis eu mauris. Phasellus non enim velit. Fusce volutpat sapien et augue congue tempor. Proin ultricies lectus eget lorem pharetra feugiat. Nulla iaculis et risus vel vehicula. Praesent fermentum orci vel quam porta, in aliquam sem scelerisque. Ut molestie sollicitudin mi, a interdum nisi posuere ac. Ut finibus purus leo, eget lobortis urna elementum eu. Quisque imperdiet tortor sed faucibus convallis. Cras sagittis nisl tempor dolor convallis molestie.

Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Proin ornare leo metus, vel pretium risus porta nec. Suspendisse lobortis iaculis tellus non feugiat. Nulla porttitor suscipit euismod. Aenean ullamcorper, elit et tempus finibus, dolor quam auctor augue, et elementum odio nisl non dui. Aenean eget euismod odio. Curabitur ut magna eget ex luctus egestas eu id libero. Ut dolor nibh, lacinia eu neque sit amet, pretium euismod ex. Fusce vel leo viverra, rutrum urna et, scelerisque erat. Nulla tincidunt at lectus id scelerisque.

Nullam euismod consectetur semper. 
Cras aliquam pellentesque consectetur. 
Duis rhoncus semper lacus, ac ultrices elit efficitur non. 
Nunc ut consequat odio, at varius turpis. 
Praesent ultrices libero a massa bibendum, sed malesuada dolor vehicula. 
Sed commodo velit id tellus sagittis maximus. 
Phasellus sed risus condimentum, viverra magna sed, hendrerit nibh. 
Donec ultricies turpis massa, at ultrices orci viverra a. 
Quisque ullamcorper tempus erat, sit amet mattis ante malesuada eget. 
Morbi dignissim dui nunc, a vulputate tellus congue a. 
Fusce vehicula finibus nulla, ut interdum nunc blandit id.

Sed efficitur at mi nec congue. Duis massa augue, ornare in elit et, interdum tincidunt est. Phasellus sit amet urna vitae tortor consectetur efficitur at vitae orci. Aenean ut ante volutpat, accumsan enim sed, accumsan libero. Curabitur imperdiet ullamcorper odio. Sed euismod enim sit amet erat laoreet volutpat. In molestie vel urna at scelerisque. Praesent in efficitur ex. Nulla eu nisi gravida, viverra orci ac, pulvinar neque. Pellentesque id mi vitae ex fermentum consequat eu sed ligula. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Pellentesque et ligula ac leo consequat ultrices. Cras condimentum quis erat ut euismod. Morbi fringilla metus eget erat ullamcorper tincidunt.

Proin laoreet volutpat finibus. Nulla et iaculis ipsum. Nullam dolor odio, sollicitudin quis volutpat sit amet, venenatis et orci. Quisque fermentum magna id sem semper, at ornare ipsum mattis. Suspendisse non nunc elementum, cursus tortor ac, iaculis magna. Nam iaculis lacus dui. Ut aliquam luctus faucibus.

Duis fringilla tincidunt quam et euismod. Fusce ut augue felis. Praesent lorem urna, lobortis id dolor viverra, placerat ultricies diam. Mauris porta eu nisl sed congue. Morbi dapibus risus ut dolor accumsan finibus. Aliquam elementum erat non pretium interdum. Vivamus dictum non sapien ut ultrices. Fusce a erat accumsan diam ultrices pulvinar non et mi. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Aliquam vel enim velit.

Suspendisse nec ornare erat, ac feugiat neque. Cras nulla sem, eleifend vitae risus eu, vestibulum dignissim ipsum. Duis auctor vitae urna ac blandit. Maecenas interdum libero at interdum lobortis. Maecenas et tellus dapibus, interdum ante at, viverra nibh. Etiam varius condimentum lorem eu porta. Maecenas euismod urna id lectus molestie accumsan. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Vestibulum pharetra lacinia leo. Vestibulum rutrum luctus eros, sed dignissim risus viverra at. Pellentesque fringilla efficitur odio vitae placerat. Maecenas consectetur euismod nulla, ac tincidunt lorem ornare non. Suspendisse vel nunc vitae diam volutpat mollis nec ut metus.

Nulla vitae nibh libero. Mauris vel eros risus. Donec placerat rhoncus velit sit amet sollicitudin. Curabitur tristique lectus ac erat sagittis, id finibus risus semper. Aliquam euismod rhoncus felis. Proin rhoncus dui enim, vel vehicula nulla luctus ut. Nulla porta ipsum eget lectus volutpat dapibus. 
"""
        parser = Parser(GrammarType.ASD_STE100_9)
        tree = parser.invoke(text, action=ParserAction.PASS2)
        print(tree.pretty())

        interpreter = TextInterpreter()
        tokens = interpreter.invoke(tree)
        doc = Ste100Doc(tokens)
        inspector = Inspector()
        structure = inspector.ste100doc(doc)
        print(structure)
