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

"""test_text_interpreter tests."""

# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116
# pylint: disable=C0301

import unittest

from biz.dfch.ste100parser import Parser
from biz.dfch.ste100parser import GrammarType
from biz.dfch.ste100parser.serializer.text_interpreter import TextInterpreter


class TextTextInterpreter(unittest.TestCase):
    def test_sth(self):

        value = """
A) This is work   step 1.
WARNING: This is a "WARNING" safety instruction (for (very) real).
CAUTION: This is a "CAUTION" safety instruction.

This is a paragraph.
A new sentence on a new line.
NOTE: This is a note1.

This is a new paragraph. (And the last paragraph.) Open the left (right) access panel L42 (R42).

# Heading for a procedure

A) Before you do the test, install the component.
B) Do the Peter's test(s) three * times
C) The `uber product` of 3 * 3 is 9.

This *is* _a_ *_"paragraph"_* "*with*" `some code`.

> And this is a "citation 'line'" (1).
> And `this` is _another_ "citation 'line'" (2).

```py
# This is a python script.
```

```c#
System.Console.WriteLine("hello, world");
```

And here is another paragraph with a list:
  1 This is list item 1.
  2 Another list item
  3 This is the third (and "last") list item.

This is the final paragraph It has two sentences.

"""

        parser = Parser(GrammarType.ASD_STE100_9)
        parsed = parser.invoke(value, do_transform=True)
        sut = TextInterpreter()
        # result = sut.visit_children(parsed)
        nested = sut.visit_children(parsed)
        self.assertIsNotNone(nested, nested)

        result = sut.flatten_result(nested)
        self.assertIsNotNone(result, result)

        print(f"result: '{result}'")

        for item in result:
            print(f"[{type(item).__name__}]: '{item.text}'")
