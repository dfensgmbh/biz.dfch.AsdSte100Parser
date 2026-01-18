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

# pylint: disable=C0116
# type: ignore

"""test_parser_structure"""

from enum import StrEnum
import unittest

from parameterized import parameterized

from biz.dfch.ste100parser import Char, GrammarType, Parser, Token, TokenMetrics
from biz.dfch.ste100parser.transformer import StructureTransformer


class Phrase(StrEnum):
    """Test phrases."""

    DQUOTE = '''"d quoted text"'''
    DQUOTE_START = '''"d quoted text" at the start.'''
    DQUOTE_END = '''This is "d quoted text"'''
    DQUOTE_DOT = """This is "d quoted text"."""
    DQUOTE_QUESTION = """This is "d quoted text"?"""
    DQUOTE_EXCL = """This is "d quoted text"!"""
    DQUOTE_COMMA = """This is "d quoted text","""
    DQUOTE_COLON = """This is "d quoted text":"""

    SQUOTE = """'s quoted text'"""
    SQUOTE_START = """'s quoted text' at the start."""
    SQUOTE_END = """This is 's quoted text'"""
    SQUOTE_DOT = """This is 's quoted text'."""
    SQUOTE_QUESTION = """This is 's quoted text'?"""
    SQUOTE_EXCL = """This is 's quoted text'!"""
    SQUOTE_COMMA = """This is 's quoted text',"""
    SQUOTE_COLON = """This is 's quoted text':"""


class TestParserBold(unittest.TestCase):
    """TestParserBold"""

    def test(self):

        value = "*bold text* at the start"
        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(11, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(5, metrics[Token.TEXT])
        self.assertEqual(4, metrics[Token.WS])
        self.assertEqual(1, metrics[Token.bold])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.bold, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)


class TestParserCode(unittest.TestCase):
    """TestParserCode"""

    def test_single(self):

        value = "`some_code` at-the-start."
        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(4, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(1, metrics[Token.CODE])
        self.assertEqual(1, metrics[Token.TEXT])
        self.assertEqual(1, metrics[Token.WS])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.CODE, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_double(self):

        value = "`some_code` `more code`"
        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(4, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(2, metrics[Token.CODE])
        self.assertEqual(1, metrics[Token.WS])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.CODE, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.CODE, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_multi_line(self):

        value = "`some_code\nmore code` "
        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(3, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(1, metrics[Token.WS])
        self.assertEqual(1, metrics[Token.CODE])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.CODE, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)


class TestParserCite(unittest.TestCase):
    """TestParserCite"""

    def test_single(self):

        value = "\r\n> block-quote-text *more-text*\nnormal-text"
        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(9, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(1, metrics[Token.cite])
        self.assertEqual(1, metrics[Token.bold])
        self.assertEqual(2, metrics[Token.NEWLINE])
        self.assertEqual(3, metrics[Token.TEXT])
        self.assertEqual(1, metrics[Token.WS])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.cite, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())
        self.assertEqual(Token.bold, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_double(self):

        value = "\r\n> block-quote-text1 *more-text*\n\n> block-quote-text1 *more-text*\nnormal-text"
        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(16, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(2, metrics[Token.cite])
        self.assertEqual(2, metrics[Token.bold])
        self.assertEqual(4, metrics[Token.NEWLINE])
        self.assertEqual(5, metrics[Token.TEXT])
        self.assertEqual(2, metrics[Token.WS])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        # # First block.
        self.assertEqual(Token.cite, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())
        self.assertEqual(Token.bold, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())

        # # Second block.
        self.assertEqual(Token.cite, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())
        self.assertEqual(Token.bold, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)


class TestParserStructureGeneric(unittest.TestCase):
    """TestParserStructureGeneric"""

    def test_inspect(self):

        value = "`_first`: 4 * 3\nNext-line-ddf\r\n\nFourth-line"
        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(12, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(1, metrics[Token.MULTIPLY])
        self.assertEqual(1, metrics[Token.CODE])
        self.assertEqual(5, metrics[Token.TEXT])
        self.assertEqual(3, metrics[Token.NEWLINE])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.MULTIPLY, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.CODE, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_newline(self):

        value = "first-line\r\n\nthird-line"
        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(5, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(2, metrics[Token.TEXT])
        self.assertEqual(2, metrics[Token.NEWLINE])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())
        self.assertEqual(Token.NEWLINE, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    @parameterized.expand([
        ("empty", Char.EMPTY, False),
        ("space", Char.SPACE, False),
        ("tab", Char.TAB, False),

        ("char_lower", 'a', True),
        ("char_upper", 'A', True),
        ("chars_lower", 'abc', True),
        ("chars_upper", 'ABC', True),
        ("chars_mixed", 'Abc', True),
        ("alpha_numeric1", 'abcABC123', True),
        ("alpha_numeric2", 'ABCabc123', True),
        ("alpha_numeric3", '123ABCabc', True),

        ("dot", Char.DOT, True),
        ("comma", Char.COMMA, True),
        ("colon", Char.COLON, True),
        ("question", Char.QUESTION, True),
        ("exclamation", Char.EXCLAMATION, True),

        ("alpha_num_ends_with_dot", "1TextThatEndsWithDot.", True),
        ("alpha_num_ends_with_comma", "1TextThatEndsWithComma,", True),
        ("alpha_num_ends_with_colon", "1TextThatEndsWithColon:", True),
        ("alpha_num_ends_with_question", "1TextThatEndsWithQuestion?", True),
        ("alpha_num_ends_with_exclamation", "1TextThatEndsWithExcl!", True),
    ])
    def test_text0(self, rule, value, expected):

        sut = Parser(GrammarType.STRUCTURE)

        if expected is False:
            self.assertFalse(sut.is_valid(value), rule)
            return

        initial = sut.invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(1, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.TEXT])

    @parameterized.expand([
        ("text_space", "text ", True),
        ("space_text", " text", True),
    ])
    def test_text1(self, rule, value, expected):

        _ = rule
        _ = expected

        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(3, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(1, metrics[Token.TEXT])
        self.assertEqual(1, metrics[Token.WS])

    @parameterized.expand([
        ("text_space", "text1 text2 ", True),
        ("space_text", " text1 text2", True),
    ])
    def test_text2(self, rule, value, expected):

        _ = rule
        _ = expected

        initial = Parser(GrammarType.STRUCTURE).invoke(value)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(5, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(2, metrics[Token.TEXT])
        self.assertEqual(2, metrics[Token.WS])


class TestParserStructureWs(unittest.TestCase):
    """TestParserStructureWs"""

    @parameterized.expand([
        ("single", ' text', True),
        ("double", '  text', True),
        ("triple", '   text', True),
        ("tab_single", '\ttext', True),
        ("tab_double", '\t\ttext', True),
        ("tab_triple", '\t\t\ttext', True),
        ("mixed", '\t \t text', True),
    ])
    def test_ws_single_token(self, rule, value, expected):

        _ = rule
        _ = expected

        initial = Parser(GrammarType.STRUCTURE).invoke(value)
        print(initial.pretty)

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(3, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(1, metrics[Token.WS])
        self.assertEqual(1, metrics[Token.TEXT])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    @parameterized.expand([
        ("tab", '\t.', True),
        ("single", ' .', True),
    ])
    def test_ws_start(self, rule, value, expected):

        _ = rule
        _ = expected

        initial = Parser(GrammarType.STRUCTURE).invoke(value)
        print(initial.pretty())

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(3, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(1, metrics[Token.WS])
        self.assertEqual(1, metrics[Token.TEXT])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    @parameterized.expand([
        ("single", '. ', True),
        ("tab", '.\t', True),
    ])
    def test_ws_end(self, rule, value, expected):

        _ = rule
        _ = expected

        initial = Parser(GrammarType.STRUCTURE).invoke(value)
        print(initial.pretty())

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(3, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(1, metrics[Token.WS])
        self.assertEqual(1, metrics[Token.TEXT])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)


class TestParserStructureApostrophe(unittest.TestCase):
    """TestParserStructureApostrophe"""

    def test_apostrophe_singular(self):

        value = """Peter's cat."""

        initial = Parser(GrammarType.STRUCTURE).invoke(value)
        print(initial.pretty())

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(5, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(1, metrics[Token.APOSTROPHE])
        self.assertEqual(1, metrics[Token.WS])
        self.assertEqual(2, metrics[Token.TEXT])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.APOSTROPHE, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_apostrophe_inside_squote(self):

        value = """'Peter's cat.' in squote."""

        initial = Parser(GrammarType.STRUCTURE).invoke(value)
        print(initial.pretty())

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(10, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(4, metrics[Token.TEXT])
        self.assertEqual(3, metrics[Token.WS])
        self.assertEqual(1, metrics[Token.squote])
        self.assertEqual(1, metrics[Token.APOSTROPHE])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.squote, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.APOSTROPHE, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_apostrophe_inside_dquote(self):

        value = """"Peter's cat." in squote."""

        initial = Parser(GrammarType.STRUCTURE).invoke(value)
        print(initial.pretty())

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(10, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(4, metrics[Token.TEXT])
        self.assertEqual(3, metrics[Token.WS])
        self.assertEqual(1, metrics[Token.dquote])
        self.assertEqual(1, metrics[Token.APOSTROPHE])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.dquote, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.APOSTROPHE, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_apostrophe_plural(self):

        value = """Manufacturers' regulations."""

        initial = Parser(GrammarType.STRUCTURE).invoke(value)
        print(initial.pretty())

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(5, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(2, metrics[Token.TEXT])
        self.assertEqual(1, metrics[Token.WS])
        self.assertEqual(1, metrics[Token.APOSTROPHE])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.APOSTROPHE, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_apostrophe_plural_in_squote(self):

        value = """'Manufacturers' regulations' in squote."""

        initial = Parser(GrammarType.STRUCTURE).invoke(value)
        print(initial.pretty())

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(10, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(4, metrics[Token.TEXT])
        self.assertEqual(1, metrics[Token.squote])
        self.assertEqual(3, metrics[Token.WS])
        self.assertEqual(1, metrics[Token.APOSTROPHE])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.squote, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.APOSTROPHE, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_apostrophe_plural_in_dquote(self):

        value = """"Manufacturers' regulations" in squote."""

        initial = Parser(GrammarType.STRUCTURE).invoke(value)
        print(initial.pretty())

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(10, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(4, metrics[Token.TEXT])
        self.assertEqual(1, metrics[Token.dquote])
        self.assertEqual(3, metrics[Token.WS])
        self.assertEqual(1, metrics[Token.APOSTROPHE])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.dquote, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.APOSTROPHE, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)


class TestParserStructure(unittest.TestCase):
    """TestParserStructure"""

    def test_and_display(self):

        value = """'I *can* _quote_ Peter's *_opening_* `parentheses` "(" and ")".'"""
        sut = Parser(GrammarType.STRUCTURE)

        try:
            result = sut.invoke(value)
            print(result.pretty())

            result = sut.is_valid(value)
            self.assertTrue(result)

        except Exception as ex:  # pylint: disable=W0718
            self.fail(ex)

    def test_squote_mixed(self):

        value = """'This is _an_ *squote*' at the *start* of a text."""

        initial = Parser(GrammarType.STRUCTURE).invoke(value)
        print(initial.pretty())

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(24, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(1, metrics[Token.squote])
        self.assertEqual(2, metrics[Token.bold])
        self.assertEqual(1, metrics[Token.emph])
        self.assertEqual(10, metrics[Token.TEXT])
        self.assertEqual(9, metrics[Token.WS])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.bold, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.squote, metrics.pop())
        self.assertEqual(Token.bold, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.emph, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    def test_dquote_mixed(self):

        value = """"This is _a_ *dquote*" at the *start* of a text."""

        initial = Parser(GrammarType.STRUCTURE).invoke(value)
        print(initial.pretty())

        metrics = TokenMetrics()
        transformed = StructureTransformer(metrics, log=True).transform(initial)
        print(transformed.pretty())

        # Assert type and quantity of tokens.
        self.assertEqual(24, len(metrics), metrics)
        self.assertEqual(1, metrics[Token.start])
        self.assertEqual(1, metrics[Token.dquote])
        self.assertEqual(2, metrics[Token.bold])
        self.assertEqual(1, metrics[Token.emph])
        self.assertEqual(10, metrics[Token.TEXT])
        self.assertEqual(9, metrics[Token.WS])

        # Assert order of tokens (recursively).
        self.assertEqual(Token.start, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.bold, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.dquote, metrics.pop())
        self.assertEqual(Token.bold, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.emph, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())
        self.assertEqual(Token.WS, metrics.pop())
        self.assertEqual(Token.TEXT, metrics.pop())

        self.assertEqual(0, len(metrics), metrics)

    @parameterized.expand([
        (Phrase.DQUOTE_DOT.name, Phrase.DQUOTE_DOT.value, True),
        (Phrase.SQUOTE_DOT.name, Phrase.SQUOTE_DOT.value, True),

        ("dquote_end", 'This is "d quoted text".', True),
        ("dquote_start", '"D quoted text" is at the start.', True),
        ("dquote_mid", 'And here "d quoted" text in the middle.', True),

        ("paren_end", 'This is text with parentheses (near the end).', True),
        ("paren_start", '(Unusual) But this can also occur.', True),
        ("paren_mid", 'Not unusual, (when writing) this can happen.', True),

        ("pq_end", 'I can use quoted text in parentheses ("This is quoted text.").', True),
        ("pq_start", '("Quoted text") Sometimes at the start.', True),
        ("pq_mid", 'Quoted text ("in this example") in the middle.', True),

        ("qp_mid_end", 'I can quote opening parentheses "(" and ")".', True),
        ("qp_start_mid", '"(" and ")" at the start.', True),

        ("bold", "This is text in *bold*", True),

        ("squote_with_apostrophe", "This is Edgar's 'single quoted' text.", True),
        ("squote_with_apostrophe", "This is 'single quoted' text from the 1900's.", True),
        ("squote_with_apostrophe",
         "'Single quoted' text from the manufacturers' specification.", True),
        ("dquote_with_apostrophe", '''This is Edgar's "double quoted" text.''', True),

        ("paren_nested", 'Nested parentheses (that is parentheses within (another pair of) parentheses).', True),
        ("paren_nested", 'Nested parentheses (that is parentheses within (another "pair" of) parentheses).', True),
    ])
    def test_container(self, rule, value, expected) -> None:

        sut = Parser(GrammarType.STRUCTURE)
        result = sut.is_valid(value)
        self.assertEqual(result, expected, f"{rule}: {value}")
