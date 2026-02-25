[![ASD-STE100: Issue 9](https://img.shields.io/badge/ASD--STE100-Issue%209-blue.svg)](https://www.asd-ste100.org/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPLv3-blue.svg)](https://github.com/dfensgmbh/biz.dfch.AsdSte100Parser/blob/dev/LICENSE)
![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue.svg)
[![Pylint and unittest](https://github.com/dfensgmbh/biz.dfch.AsdSte100Parser/actions/workflows/ci.yml/badge.svg)](https://github.com/dfensgmbh/biz.dfch.AsdSte100Parser/actions/workflows/ci.yml)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=dfensgmbh_biz.dfch.AsdSte100Parser&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=dfensgmbh_biz.dfch.AsdSte100Parser)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=dfensgmbh_biz.dfch.AsdSte100Parser&metric=bugs)](https://sonarcloud.io/summary/new_code?id=dfensgmbh_biz.dfch.AsdSte100Parser)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=dfensgmbh_biz.dfch.AsdSte100Parser&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=dfensgmbh_biz.dfch.AsdSte100Parser)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=dfensgmbh_biz.dfch.AsdSte100Parser&metric=coverage)](https://sonarcloud.io/summary/new_code?id=dfensgmbh_biz.dfch.AsdSte100Parser)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=dfensgmbh_biz.dfch.AsdSte100Parser&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=dfensgmbh_biz.dfch.AsdSte100Parser)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=dfensgmbh_biz.dfch.AsdSte100Parser&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=dfensgmbh_biz.dfch.AsdSte100Parser)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=dfensgmbh_biz.dfch.AsdSte100Parser&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=dfensgmbh_biz.dfch.AsdSte100Parser)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=dfensgmbh_biz.dfch.AsdSte100Parser&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=dfensgmbh_biz.dfch.AsdSte100Parser)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=dfensgmbh_biz.dfch.AsdSte100Parser&metric=sqale_index)](https://sonarcloud.io/summary/new_code?id=dfensgmbh_biz.dfch.AsdSte100Parser)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=dfensgmbh_biz.dfch.AsdSte100Parser&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=dfensgmbh_biz.dfch.AsdSte100Parser)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=dfensgmbh_biz.dfch.AsdSte100Parser&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=dfensgmbh_biz.dfch.AsdSte100Parser)

# biz.dfch.AsdSte100Parser

This library implements a:
  * An EBNF grammar for Lark (earley) 
  * A multi-pass transformer
  * A tokenizer
  * A serializer.

You must use a special structure of **Markdown** as the input text.

## Installation

[biz-dfch-ste100parser](https://pypi.org/project/biz-dfch-ste100parser) is on [PyPI](https://pypi.org). Create a virtual environment and install the library with `pip`:

```
pip install biz-dfch-ste100parser
```

## Usage

```py
from biz.dfch.ste100parser import ContainerTransformer
from biz.dfch.ste100parser import GrammarType
from biz.dfch.ste100parser import Parser
from biz.dfch.ste100parser import Token

value = ""  # Specify text (example content and output see below).

parser = Parser(GrammarType.CONTAINER)
assert parser.is_valid(value)

# This parses the tree according to the CONTAINER grammar.
initial_tree = parser.invoke(value)

# This transforms the tree to the tokens described in the "Format" section.
transformer = ContainerTransformer()
transformed_tree = transformer.invoke(initial_tree)

# This prints the resulting AST.
print(transformed.pretty())
```

### Input text

```
# This is a heading *level 1*

This is the start of the _first_ paragraph. This is the second sentence.
Third sentence, after a LINEBREAK. The fourth sentence starts a list:
  1 This is the first list item.
  2 Another item
  3 Last item.
The paragraph continues.

This is para2. And, this is a new paragraph with only a single sentence.

## This is our procedure

1. Do this
2. Do that:
   a This is a list with item 1
   b The next item
   c The last item.
3. And then, do this one last time.

This is para3. Here, we have another paragraph.

This is para4. Here, we have another paragraph.
This continues para4 after a LINEBREAK.

This is para5. Here, we have another paragraph.
    a This is a list with item 1
    b The next item
    c The last item.

1. Another proc (without heading)
2. Last step.

> Line1. This-is-some-cite-text-1.1. This-is-some-cite-text-2.1.
> Line2. This-is-some-cite-text-2.1. This-is-some-cite-text-2.2.

And yet another, paragraph.

> LineA. This-is-some-cite-text-A.1. This-is-some-cite-text-A.1.
> LineB. This-is-some-cite-text-B.1. This-is-some-cite-text-B.2.

```

### EBNF earley lark Tree

```
start
  heading
    HEADING_LEVEL       1
    TEXT        This
    WS  1
    TEXT        is
    WS  1
    TEXT        a
    WS  1
    TEXT        heading
    WS  1
    bold
      TEXT      level
      WS        1
      TEXT      1
  paragraph
    TEXT        This
    WS  1
    TEXT        is
    WS  1
    TEXT        the
    WS  1
    TEXT        start
    WS  1
    TEXT        of
    WS  1
    TEXT        the
    WS  1
    emph
      TEXT      first
    WS  1
    TEXT        paragraph.
    WS  1
    TEXT        This
    WS  1
    TEXT        is
    WS  1
    TEXT        the
    WS  1
    TEXT        second
    WS  1
    TEXT        sentence.
    LINEBREAK

    TEXT        Third
    WS  1
    TEXT        sentence,
    WS  1
    TEXT        after
    WS  1
    TEXT        a
    WS  1
    TEXT        LINEBREAK.
    WS  1
    TEXT        The
    WS  1
    TEXT        fourth
    WS  1
    TEXT        sentence
    WS  1
    TEXT        starts
    WS  1
    TEXT        a
    WS  1
    TEXT        list:
    list_item
      LIST_MARKER       1
      LIST_INDENT       2
      TEXT      This
      WS        1
      TEXT      is
      WS        1
      TEXT      the
      WS        1
      TEXT      first
      WS        1
      TEXT      list
      WS        1
      TEXT      item.
    list_item
      LIST_MARKER       2
      LIST_INDENT       2
      TEXT      Another
      WS        1
      TEXT      item
    list_item
      LIST_MARKER       3
      LIST_INDENT       2
      TEXT      Last
      WS        1
      TEXT      item.
    TEXT        The
    WS  1
    TEXT        paragraph
    WS  1
    TEXT        continues.
  paragraph
    TEXT        This
    WS  1
    TEXT        is
    WS  1
    TEXT        para2.
    WS  1
    TEXT        And,
    WS  1
    TEXT        this
    WS  1
    TEXT        is
    WS  1
    TEXT        a
    WS  1
    TEXT        new
    WS  1
    TEXT        paragraph
    WS  1
    TEXT        with
    WS  1
    TEXT        only
    WS  1
    TEXT        a
    WS  1
    TEXT        single
    WS  1
    TEXT        sentence.
  heading
    HEADING_LEVEL       2
    TEXT        This
    WS  1
    TEXT        is
    WS  1
    TEXT        our
    WS  1
    TEXT        procedure
  proc_item
    PROC_STEP   1
    PROC_DELIMITER      .
    TEXT        Do
    WS  1
    TEXT        this
  proc_item
    PROC_STEP   2
    PROC_DELIMITER      .
    TEXT        Do
    WS  1
    TEXT        that:
    list_item
      LIST_MARKER       a
      LIST_INDENT       3
      TEXT      This
      WS        1
      TEXT      is
      WS        1
      TEXT      a
      WS        1
      TEXT      list
      WS        1
      TEXT      with
      WS        1
      TEXT      item
      WS        1
      TEXT      1
    list_item
      LIST_MARKER       b
      LIST_INDENT       3
      TEXT      The
      WS        1
      TEXT      next
      WS        1
      TEXT      item
    list_item
      LIST_MARKER       c
      LIST_INDENT       3
      TEXT      The
      WS        1
      TEXT      last
      WS        1
      TEXT      item.
  proc_item
    PROC_STEP   3
    PROC_DELIMITER      .
    TEXT        And
    WS  1
    TEXT        then,
    WS  1
    TEXT        do
    WS  1
    TEXT        this
    WS  1
    TEXT        one
    WS  1
    TEXT        last
    WS  1
    TEXT        time.
  paragraph
    TEXT        This
    WS  1
    TEXT        is
    WS  1
    TEXT        para3.
    WS  1
    TEXT        Here,
    WS  1
    TEXT        we
    WS  1
    TEXT        have
    WS  1
    TEXT        another
    WS  1
    TEXT        paragraph.
  paragraph
    TEXT        This
    WS  1
    TEXT        is
    WS  1
    TEXT        para4.
    WS  1
    TEXT        Here,
    WS  1
    TEXT        we
    WS  1
    TEXT        have
    WS  1
    TEXT        another
    WS  1
    TEXT        paragraph.
    LINEBREAK

    TEXT        This
    WS  1
    TEXT        continues
    WS  1
    TEXT        para4
    WS  1
    TEXT        after
    WS  1
    TEXT        a
    WS  1
    TEXT        LINEBREAK.
  paragraph
    TEXT        This
    WS  1
    TEXT        is
    WS  1
    TEXT        para5.
    WS  1
    TEXT        Here,
    WS  1
    TEXT        we
    WS  1
    TEXT        have
    WS  1
    TEXT        another
    WS  1
    TEXT        paragraph.
    list_item
      LIST_MARKER       a
      LIST_INDENT       4
      TEXT      This
      WS        1
      TEXT      is
      WS        1
      TEXT      a
      WS        1
      TEXT      list
      WS        1
      TEXT      with
      WS        1
      TEXT      item
      WS        1
      TEXT      1
    list_item
      LIST_MARKER       b
      LIST_INDENT       4
      TEXT      The
      WS        1
      TEXT      next
      WS        1
      TEXT      item
    list_item
      LIST_MARKER       c
      LIST_INDENT       4
      TEXT      The
      WS        1
      TEXT      last
      WS        1
      TEXT      item.
  proc_item
    PROC_STEP   1
    PROC_DELIMITER      .
    TEXT        Another
    WS  1
    TEXT        proc
    WS  1
    paren
      TEXT      without
      WS        1
      TEXT      heading
  proc_item
    PROC_STEP   2
    PROC_DELIMITER      .
    TEXT        Last
    WS  1
    TEXT        step.
  cite
    TEXT        Line1.
    WS  1
    TEXT        This-is-some-cite-text-1.1.
    WS  1
    TEXT        This-is-some-cite-text-2.1.
  cite
    TEXT        Line2.
    WS  1
    TEXT        This-is-some-cite-text-2.1.
    WS  1
    TEXT        This-is-some-cite-text-2.2.
  paragraph
    TEXT        And
    WS  1
    TEXT        yet
    WS  1
    TEXT        another,
    WS  1
    TEXT        paragraph.
  cite
    TEXT        LineA.
    WS  1
    TEXT        This-is-some-cite-text-A.1.
    WS  1
    TEXT        This-is-some-cite-text-A.1.
  cite
    TEXT        LineB.
    WS  1
    TEXT        This-is-some-cite-text-B.1.
    WS  1
    TEXT        This-is-some-cite-text-B.2.

```

### Abstract Syntax Tree

```
# Topmost "heading line" (with parentheses)

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
D) Open the eenie-weenie self-inflating door.
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
```

This is what the Abstract Syntax Tree (AST) looks like (after spaCy did sentence detection and dependency):

```
[level:total:index]
[00:01:00][TokenRoot] [id:00][p:-1] [#11]
[01:11:00]. [Heading] [id:01][p:00] [#1]
[02:01:00]. . [Sentence] [id:02][p:01] [#5]
[03:05:00]. . . 'Topmost' [Text] [id:03][p:02] 
[03:05:01]. . . ' ' [Ws] [id:04][p:02] 
[03:05:02]. . . [Quote] [id:05][p:02] [#3]
[04:03:00]. . . . 'heading' [Text] [id:06][p:05] 
[04:03:01]. . . . ' ' [Ws] [id:07][p:05] 
[04:03:02]. . . . 'line' [Text] [id:08][p:05] 
[03:05:03]. . . ' ' [Ws] [id:09][p:02] 
[03:05:04]. . . [Parentheses] [id:10][p:02] [#1]
[04:01:00]. . . . [Sentence] [id:11][p:10] [#3]
[05:03:00]. . . . . 'with' [Word] [id:12][p:11] 
[05:03:01]. . . . . ' ' [Ws] [id:13][p:11] 
[05:03:02]. . . . . 'parentheses' [Text] [id:14][p:11] 
[01:11:01]. [Heading] [id:15][p:00] [#1]
[02:01:00]. . [Sentence] [id:16][p:15] [#3]
[03:03:00]. . . 'Procedural' [Text] [id:17][p:16] 
[03:03:01]. . . ' ' [Ws] [id:18][p:16] 
[03:03:02]. . . 'Writing' [Text] [id:19][p:16] 
[01:11:02]. [ProcItem] [id:20][p:00] [#6]
[02:06:00]. . [Sentence] [id:21][p:20] [#10]
[03:10:00]. . . 'This' [Word] [id:22][p:21] 
[03:10:01]. . . ' ' [Ws] [id:23][p:21] 
[03:10:02]. . . 'is' [Text] [id:24][p:21] 
[03:10:03]. . . ' ' [Ws] [id:25][p:21] 
[03:10:04]. . . 'work' [Word] [id:26][p:21] 
[03:10:05]. . . ' ' [Ws] [id:27][p:21] 
[03:10:06]. . . 'step' [Word] [id:28][p:21] 
[03:10:07]. . . ' ' [Ws] [id:29][p:21] 
[03:10:08]. . . 'A' [Word] [id:30][p:21] 
[03:10:09]. . . '.' [Punct] [id:31][p:21] 
[02:06:01]. . [Sentence] [id:32][p:20] [#10]
[03:10:00]. . . 'And' [Word] [id:33][p:32] 
[03:10:01]. . . ' ' [Ws] [id:34][p:32] 
[03:10:02]. . . 'we' [Word] [id:35][p:32] 
[03:10:03]. . . ' ' [Ws] [id:36][p:32] 
[03:10:04]. . . 'have' [Word] [id:37][p:32] 
[03:10:05]. . . ' ' [Ws] [id:38][p:32] 
[03:10:06]. . . '2' [Number] [id:39][p:32] 
[03:10:07]. . . ' ' [Ws] [id:40][p:32] 
[03:10:08]. . . 'sentences' [Text] [id:41][p:32] 
[03:10:09]. . . ':' [Punct] [id:42][p:32] 
[02:06:02]. . [ListItem] [id:43][p:20] [#2]
[03:02:00]. . . [Sentence] [id:44][p:43] [#8]
[04:08:00]. . . . 'Vertical' [Word] [id:45][p:44] 
[04:08:01]. . . . ' ' [Ws] [id:46][p:44] 
[04:08:02]. . . . 'list' [Word] [id:47][p:44] 
[04:08:03]. . . . ' ' [Ws] [id:48][p:44] 
[04:08:04]. . . . 'item' [Word] [id:49][p:44] 
[04:08:05]. . . . ' ' [Ws] [id:50][p:44] 
[04:08:06]. . . . '1' [Number] [id:51][p:44] 
[04:08:07]. . . . '.' [Punct] [id:52][p:44] 
[03:02:01]. . . [Sentence] [id:53][p:43] [#8]
[04:08:00]. . . . 'There' [Word] [id:54][p:53] 
[04:08:01]. . . . ' ' [Ws] [id:55][p:53] 
[04:08:02]. . . . 'are' [Text] [id:56][p:53] 
[04:08:03]. . . . ' ' [Ws] [id:57][p:53] 
[04:08:04]. . . . '2' [Number] [id:58][p:53] 
[04:08:05]. . . . ' ' [Ws] [id:59][p:53] 
[04:08:06]. . . . 'sentences' [Text] [id:60][p:53] 
[04:08:07]. . . . '.' [Punct] [id:61][p:53] 
[02:06:03]. . [ListItem] [id:62][p:20] [#1]
[03:01:00]. . . [Sentence] [id:63][p:62] [#12]
[04:12:00]. . . . 'This' [Word] [id:64][p:63] 
[04:12:01]. . . . ' ' [Ws] [id:65][p:63] 
[04:12:02]. . . . 'is' [Text] [id:66][p:63] 
[04:12:03]. . . . ' ' [Ws] [id:67][p:63] 
[04:12:04]. . . . 'another' [Word] [id:68][p:63] 
[04:12:05]. . . . ' ' [Ws] [id:69][p:63] 
[04:12:06]. . . . 'vertical' [Word] [id:70][p:63] 
[04:12:07]. . . . ' ' [Ws] [id:71][p:63] 
[04:12:08]. . . . 'list' [Word] [id:72][p:63] 
[04:12:09]. . . . ' ' [Ws] [id:73][p:63] 
[04:12:10]. . . . 'item' [Word] [id:74][p:63] 
[04:12:11]. . . . '.' [Punct] [id:75][p:63] 
[02:06:04]. . [ListItem] [id:76][p:20] [#1]
[03:01:00]. . . [Sentence] [id:77][p:76] [#12]
[04:12:00]. . . . 'The' [Word] [id:78][p:77] 
[04:12:01]. . . . ' ' [Ws] [id:79][p:77] 
[04:12:02]. . . . 'last' [Word] [id:80][p:77] 
[04:12:03]. . . . ' ' [Ws] [id:81][p:77] 
[04:12:04]. . . . [Parentheses] [id:82][p:77] [#1]
[05:01:00]. . . . . [Sentence] [id:83][p:82] [#1]
[06:01:00]. . . . . . '3' [Number] [id:84][p:83] 
[04:12:05]. . . . ' ' [Ws] [id:85][p:77] 
[04:12:06]. . . . 'vertical' [Word] [id:86][p:77] 
[04:12:07]. . . . ' ' [Ws] [id:87][p:77] 
[04:12:08]. . . . 'list' [Word] [id:88][p:77] 
[04:12:09]. . . . ' ' [Ws] [id:89][p:77] 
[04:12:10]. . . . 'item' [Word] [id:90][p:77] 
[04:12:11]. . . . '.' [Punct] [id:91][p:77] 
[02:06:05]. . [NoteOrSafetyInstruction] [id:92][p:20] [#2]
[03:02:00]. . . [Sentence] [id:93][p:92] [#4]
[04:04:00]. . . . 'Safety' [Word] [id:94][p:93] 
[04:04:01]. . . . ' ' [Ws] [id:95][p:93] 
[04:04:02]. . . . 'instruction' [Word] [id:96][p:93] 
[04:04:03]. . . . '.' [Punct] [id:97][p:93] 
[03:02:01]. . . [Sentence] [id:98][p:92] [#4]
[04:04:00]. . . . '2' [Number] [id:99][p:98] 
[04:04:01]. . . . ' ' [Ws] [id:100][p:98] 
[04:04:02]. . . . 'sentences' [Text] [id:101][p:98] 
[04:04:03]. . . . '.' [Punct] [id:102][p:98] 
[01:11:03]. [ProcItem] [id:103][p:00] [#2]
[02:02:00]. . [Sentence] [id:104][p:103] [#5]
[03:05:00]. . . 'Work' [Word] [id:105][p:104] 
[03:05:01]. . . ' ' [Ws] [id:106][p:104] 
[03:05:02]. . . 'step' [Word] [id:107][p:104] 
[03:05:03]. . . ' ' [Ws] [id:108][p:104] 
[03:05:04]. . . 'B' [Text] [id:109][p:104] 
[02:02:01]. . [NoteOrSafetyInstruction] [id:110][p:103] [#1]
[03:01:00]. . . [Sentence] [id:111][p:110] [#12]
[04:12:00]. . . . 'This' [Word] [id:112][p:111] 
[04:12:01]. . . . ' ' [Ws] [id:113][p:111] 
[04:12:02]. . . . 'is' [Text] [id:114][p:111] 
[04:12:03]. . . . ' ' [Ws] [id:115][p:111] 
[04:12:04]. . . . 'a' [Word] [id:116][p:111] 
[04:12:05]. . . . ' ' [Ws] [id:117][p:111] 
[04:12:06]. . . . [Format] [id:118][p:111] [#1]
[05:01:00]. . . . . 'safety' [Word] [id:119][p:118] 
[04:12:07]. . . . ' ' [Ws] [id:120][p:111] 
[04:12:08]. . . . 'instruction' [Word] [id:121][p:111] 
[04:12:09]. . . . ' ' [Ws] [id:122][p:111] 
[04:12:10]. . . . [Parentheses] [id:123][p:111] [#1]
[05:01:00]. . . . . [Sentence] [id:124][p:123] [#3]
[06:03:00]. . . . . . 'with' [Word] [id:125][p:124] 
[06:03:01]. . . . . . ' ' [Ws] [id:126][p:124] 
[06:03:02]. . . . . . 'parentheses' [Text] [id:127][p:124] 
[04:12:11]. . . . '.' [Punct] [id:128][p:111] 
[01:11:04]. [ProcItem] [id:129][p:00] [#7]
[02:07:00]. . [Sentence] [id:130][p:129] [#29]
[03:29:00]. . . 'When' [Word] [id:131][p:130] 
[03:29:01]. . . ' ' [Ws] [id:132][p:130] 
[03:29:02]. . . 'you' [Word] [id:133][p:130] 
[03:29:03]. . . ' ' [Ws] [id:134][p:130] 
[03:29:04]. . . 'open' [Word] [id:135][p:130] 
[03:29:05]. . . ' ' [Ws] [id:136][p:130] 
[03:29:06]. . . 'the' [Word] [id:137][p:130] 
[03:29:07]. . . ' ' [Ws] [id:138][p:130] 
[03:29:08]. . . 'oven' [Text] [id:139][p:130] 
[03:29:09]. . . ',' [Punct] [id:140][p:130] 
[03:29:10]. . . ' ' [Ws] [id:141][p:130] 
[03:29:11]. . . 'make' [Word] [id:142][p:130] 
[03:29:12]. . . ' ' [Ws] [id:143][p:130] 
[03:29:13]. . . 'sure' [Word] [id:144][p:130] 
[03:29:14]. . . ' ' [Ws] [id:145][p:130] 
[03:29:15]. . . 'that' [Word] [id:146][p:130] 
[03:29:16]. . . ' ' [Ws] [id:147][p:130] 
[03:29:17]. . . 'you' [Word] [id:148][p:130] 
[03:29:18]. . . ' ' [Ws] [id:149][p:130] 
[03:29:19]. . . 'do' [Word] [id:150][p:130] 
[03:29:20]. . . ' ' [Ws] [id:151][p:130] 
[03:29:21]. . . 'not' [Word] [id:152][p:130] 
[03:29:22]. . . ' ' [Ws] [id:153][p:130] 
[03:29:23]. . . 'burn' [Word] [id:154][p:130] 
[03:29:24]. . . ' ' [Ws] [id:155][p:130] 
[03:29:25]. . . 'your' [Word] [id:156][p:130] 
[03:29:26]. . . ' ' [Ws] [id:157][p:130] 
[03:29:27]. . . 'skin' [Text] [id:158][p:130] 
[03:29:28]. . . '.' [Punct] [id:159][p:130] 
[02:07:01]. . [Sentence] [id:160][p:129] [#10]
[03:10:00]. . . 'Do' [Word] [id:161][p:160] 
[03:10:01]. . . ' ' [Ws] [id:162][p:160] 
[03:10:02]. . . 'it' [Word] [id:163][p:160] 
[03:10:03]. . . ' ' [Ws] [id:164][p:160] 
[03:10:04]. . . 'in' [Word] [id:165][p:160] 
[03:10:05]. . . ' ' [Ws] [id:166][p:160] 
[03:10:06]. . . 'this' [Word] [id:167][p:160] 
[03:10:07]. . . ' ' [Ws] [id:168][p:160] 
[03:10:08]. . . 'order' [Word] [id:169][p:160] 
[03:10:09]. . . ':' [Punct] [id:170][p:160] 
[02:07:02]. . [ListItem] [id:171][p:129] [#2]
[03:02:00]. . . [Sentence] [id:172][p:171] [#8]
[04:08:00]. . . . 'Put' [Word] [id:173][p:172] 
[04:08:01]. . . . ' ' [Ws] [id:174][p:172] 
[04:08:02]. . . . 'on' [Word] [id:175][p:172] 
[04:08:03]. . . . ' ' [Ws] [id:176][p:172] 
[04:08:04]. . . . 'protective' [Word] [id:177][p:172] 
[04:08:05]. . . . ' ' [Ws] [id:178][p:172] 
[04:08:06]. . . . 'gear' [Text] [id:179][p:172] 
[04:08:07]. . . . '.' [Punct] [id:180][p:172] 
[03:02:01]. . . [Sentence] [id:181][p:171] [#14]
[04:14:00]. . . . 'A' [Word] [id:182][p:181] 
[04:14:01]. . . . ' ' [Ws] [id:183][p:181] 
[04:14:02]. . . . 'heat' [Word] [id:184][p:181] 
[04:14:03]. . . . ' ' [Ws] [id:185][p:181] 
[04:14:04]. . . . 'resistant' [Word] [id:186][p:181] 
[04:14:05]. . . . ' ' [Ws] [id:187][p:181] 
[04:14:06]. . . . 'glove' [Text] [id:188][p:181] 
[04:14:07]. . . . ' ' [Ws] [id:189][p:181] 
[04:14:08]. . . . 'gives' [Text] [id:190][p:181] 
[04:14:09]. . . . ' ' [Ws] [id:191][p:181] 
[04:14:10]. . . . 'best' [Text] [id:192][p:181] 
[04:14:11]. . . . ' ' [Ws] [id:193][p:181] 
[04:14:12]. . . . 'protection' [Word] [id:194][p:181] 
[04:14:13]. . . . '.' [Punct] [id:195][p:181] 
[02:07:03]. . [ListItem] [id:196][p:129] [#1]
[03:01:00]. . . [Sentence] [id:197][p:196] [#15]
[04:15:00]. . . . 'Set' [Word] [id:198][p:197] 
[04:15:01]. . . . ' ' [Ws] [id:199][p:197] 
[04:15:02]. . . . 'the' [Word] [id:200][p:197] 
[04:15:03]. . . . ' ' [Ws] [id:201][p:197] 
[04:15:04]. . . . 'switch' [Word] [id:202][p:197] 
[04:15:05]. . . . ' ' [Ws] [id:203][p:197] 
[04:15:06]. . . . 'of' [Word] [id:204][p:197] 
[04:15:07]. . . . ' ' [Ws] [id:205][p:197] 
[04:15:08]. . . . 'the' [Word] [id:206][p:197] 
[04:15:09]. . . . ' ' [Ws] [id:207][p:197] 
[04:15:10]. . . . 'oven' [Text] [id:208][p:197] 
[04:15:11]. . . . ' ' [Ws] [id:209][p:197] 
[04:15:12]. . . . 'to' [Word] [id:210][p:197] 
[04:15:13]. . . . ' ' [Ws] [id:211][p:197] 
[04:15:14]. . . . [Quote] [id:212][p:197] [#1]
[05:01:00]. . . . . 'OFF' [Word] [id:213][p:212] 
[02:07:04]. . [Sentence] [id:214][p:129] [#1]
[03:01:00]. . . '.' [Punct] [id:215][p:214] 
[02:07:05]. . [ListItem] [id:216][p:129] [#1]
[03:01:00]. . . [Sentence] [id:217][p:216] [#9]
[04:09:00]. . . . 'Carefully' [Word] [id:218][p:217] 
[04:09:01]. . . . ',' [Punct] [id:219][p:217] 
[04:09:02]. . . . ' ' [Ws] [id:220][p:217] 
[04:09:03]. . . . 'open' [Word] [id:221][p:217] 
[04:09:04]. . . . ' ' [Ws] [id:222][p:217] 
[04:09:05]. . . . 'the' [Word] [id:223][p:217] 
[04:09:06]. . . . ' ' [Ws] [id:224][p:217] 
[04:09:07]. . . . 'door' [Text] [id:225][p:217] 
[04:09:08]. . . . '.' [Punct] [id:226][p:217] 
[02:07:06]. . [NoteOrSafetyInstruction] [id:227][p:129] [#1]
[03:01:00]. . . [Sentence] [id:228][p:227] [#14]
[04:14:00]. . . . 'This' [Word] [id:229][p:228] 
[04:14:01]. . . . ' ' [Ws] [id:230][p:228] 
[04:14:02]. . . . 'is' [Text] [id:231][p:228] 
[04:14:03]. . . . ' ' [Ws] [id:232][p:228] 
[04:14:04]. . . . 'a' [Word] [id:233][p:228] 
[04:14:05]. . . . ' ' [Ws] [id:234][p:228] 
[04:14:06]. . . . 'safety' [Code] [id:235][p:228] 
[04:14:07]. . . . ' ' [Ws] [id:236][p:228] 
[04:14:08]. . . . 'instruction' [Word] [id:237][p:228] 
[04:14:09]. . . . ' ' [Ws] [id:238][p:228] 
[04:14:10]. . . . 'without' [Word] [id:239][p:228] 
[04:14:11]. . . . ' ' [Ws] [id:240][p:228] 
[04:14:12]. . . . 'parentheses' [Text] [id:241][p:228] 
[04:14:13]. . . . '.' [Punct] [id:242][p:228] 
[01:11:05]. [ProcItem] [id:243][p:00] [#1]
[02:01:00]. . [Sentence] [id:244][p:243] [#10]
[03:10:00]. . . 'Open' [Word] [id:245][p:244] 
[03:10:01]. . . ' ' [Ws] [id:246][p:244] 
[03:10:02]. . . 'the' [Word] [id:247][p:244] 
[03:10:03]. . . ' ' [Ws] [id:248][p:244] 
[03:10:04]. . . 'eenie-weenie' [Word] [id:249][p:244] 
[03:10:05]. . . ' ' [Ws] [id:250][p:244] 
[03:10:06]. . . 'self-inflating' [Text] [id:251][p:244] 
[03:10:07]. . . ' ' [Ws] [id:252][p:244] 
[03:10:08]. . . 'door' [Text] [id:253][p:244] 
[03:10:09]. . . '.' [Punct] [id:254][p:244] 
[01:11:06]. [ProcItem] [id:255][p:00] [#1]
[02:01:00]. . [Sentence] [id:256][p:255] [#10]
[03:10:00]. . . 'The' [Word] [id:257][p:256] 
[03:10:01]. . . ' ' [Ws] [id:258][p:256] 
[03:10:02]. . . 'last' [Word] [id:259][p:256] 
[03:10:03]. . . ' ' [Ws] [id:260][p:256] 
[03:10:04]. . . 'work' [Word] [id:261][p:256] 
[03:10:05]. . . ' ' [Ws] [id:262][p:256] 
[03:10:06]. . . 'step' [Word] [id:263][p:256] 
[03:10:07]. . . ' ' [Ws] [id:264][p:256] 
[03:10:08]. . . [Parentheses] [id:265][p:256] [#1]
[04:01:00]. . . . [Sentence] [id:266][p:265] [#1]
[05:01:00]. . . . . 'E' [Text] [id:267][p:266] 
[03:10:09]. . . '.' [Punct] [id:268][p:256] 
[01:11:07]. [Heading] [id:269][p:00] [#1]
[02:01:00]. . [Sentence] [id:270][p:269] [#3]
[03:03:00]. . . 'Descriptive' [Text] [id:271][p:270] 
[03:03:01]. . . ' ' [Ws] [id:272][p:270] 
[03:03:02]. . . 'Writing' [Text] [id:273][p:270] 
[01:11:08]. [Paragraph] [id:274][p:00] [#8]
[02:08:00]. . [Sentence] [id:275][p:274] [#8]
[03:08:00]. . . 'Paragraph' [Text] [id:276][p:275] 
[03:08:01]. . . ' ' [Ws] [id:277][p:275] 
[03:08:02]. . . 'with' [Word] [id:278][p:275] 
[03:08:03]. . . ' ' [Ws] [id:279][p:275] 
[03:08:04]. . . 'a' [Word] [id:280][p:275] 
[03:08:05]. . . ' ' [Ws] [id:281][p:275] 
[03:08:06]. . . 'NOTE' [Word] [id:282][p:275] 
[03:08:07]. . . '.' [Punct] [id:283][p:275] 
[02:08:01]. . [Sentence] [id:284][p:274] [#20]
[03:20:00]. . . 'And' [Word] [id:285][p:284] 
[03:20:01]. . . ' ' [Ws] [id:286][p:284] 
[03:20:02]. . . 'in' [Word] [id:287][p:284] 
[03:20:03]. . . ' ' [Ws] [id:288][p:284] 
[03:20:04]. . . 'this' [Word] [id:289][p:284] 
[03:20:05]. . . ' ' [Ws] [id:290][p:284] 
[03:20:06]. . . 'paragraph' [Text] [id:291][p:284] 
[03:20:07]. . . ' ' [Ws] [id:292][p:284] 
[03:20:08]. . . 'we' [Word] [id:293][p:284] 
[03:20:09]. . . ' ' [Ws] [id:294][p:284] 
[03:20:10]. . . 'have' [Word] [id:295][p:284] 
[03:20:11]. . . ' ' [Ws] [id:296][p:284] 
[03:20:12]. . . 'more' [Word] [id:297][p:284] 
[03:20:13]. . . ' ' [Ws] [id:298][p:284] 
[03:20:14]. . . 'than' [Word] [id:299][p:284] 
[03:20:15]. . . ' ' [Ws] [id:300][p:284] 
[03:20:16]. . . 'one' [Word] [id:301][p:284] 
[03:20:17]. . . ' ' [Ws] [id:302][p:284] 
[03:20:18]. . . 'sentence' [Text] [id:303][p:284] 
[03:20:19]. . . '.' [Punct] [id:304][p:284] 
[02:08:02]. . [Sentence] [id:305][p:274] [#10]
[03:10:00]. . . 'This' [Word] [id:306][p:305] 
[03:10:01]. . . ' ' [Ws] [id:307][p:305] 
[03:10:02]. . . 'sentence' [Text] [id:308][p:305] 
[03:10:03]. . . ' ' [Ws] [id:309][p:305] 
[03:10:04]. . . 'starts' [Text] [id:310][p:305] 
[03:10:05]. . . ' ' [Ws] [id:311][p:305] 
[03:10:06]. . . 'a' [Word] [id:312][p:305] 
[03:10:07]. . . ' ' [Ws] [id:313][p:305] 
[03:10:08]. . . 'list' [Word] [id:314][p:305] 
[03:10:09]. . . ':' [Punct] [id:315][p:305] 
[02:08:03]. . [ListItem] [id:316][p:274] [#1]
[03:01:00]. . . [Sentence] [id:317][p:316] [#5]
[04:05:00]. . . . 'First' [Word] [id:318][p:317] 
[04:05:01]. . . . ' ' [Ws] [id:319][p:317] 
[04:05:02]. . . . 'list' [Word] [id:320][p:317] 
[04:05:03]. . . . ' ' [Ws] [id:321][p:317] 
[04:05:04]. . . . 'item' [Word] [id:322][p:317] 
[02:08:04]. . [ListItem] [id:323][p:274] [#1]
[03:01:00]. . . [Sentence] [id:324][p:323] [#20]
[04:20:00]. . . . 'This' [Word] [id:325][p:324] 
[04:20:01]. . . . ' ' [Ws] [id:326][p:324] 
[04:20:02]. . . . 'is' [Text] [id:327][p:324] 
[04:20:03]. . . . ' ' [Ws] [id:328][p:324] 
[04:20:04]. . . . 'another' [Word] [id:329][p:324] 
[04:20:05]. . . . ' ' [Ws] [id:330][p:324] 
[04:20:06]. . . . 'list' [Word] [id:331][p:324] 
[04:20:07]. . . . ' ' [Ws] [id:332][p:324] 
[04:20:08]. . . . 'item' [Word] [id:333][p:324] 
[04:20:09]. . . . ' ' [Ws] [id:334][p:324] 
[04:20:10]. . . . 'that' [Word] [id:335][p:324] 
[04:20:11]. . . . ' ' [Ws] [id:336][p:324] 
[04:20:12]. . . . 'is' [Text] [id:337][p:324] 
[04:20:13]. . . . ' ' [Ws] [id:338][p:324] 
[04:20:14]. . . . 'a' [Word] [id:339][p:324] 
[04:20:15]. . . . ' ' [Ws] [id:340][p:324] 
[04:20:16]. . . . 'full' [Word] [id:341][p:324] 
[04:20:17]. . . . ' ' [Ws] [id:342][p:324] 
[04:20:18]. . . . 'sentence' [Text] [id:343][p:324] 
[04:20:19]. . . . '.' [Punct] [id:344][p:324] 
[02:08:05]. . [ListItem] [id:345][p:274] [#1]
[03:01:00]. . . [Sentence] [id:346][p:345] [#8]
[04:08:00]. . . . 'The' [Word] [id:347][p:346] 
[04:08:01]. . . . ' ' [Ws] [id:348][p:346] 
[04:08:02]. . . . 'last' [Word] [id:349][p:346] 
[04:08:03]. . . . ' ' [Ws] [id:350][p:346] 
[04:08:04]. . . . 'list' [Word] [id:351][p:346] 
[04:08:05]. . . . ' ' [Ws] [id:352][p:346] 
[04:08:06]. . . . 'item' [Word] [id:353][p:346] 
[04:08:07]. . . . '.' [Punct] [id:354][p:346] 
[02:08:06]. . [Sentence] [id:355][p:274] [#14]
[03:14:00]. . . 'The' [Word] [id:356][p:355] 
[03:14:01]. . . ' ' [Ws] [id:357][p:355] 
[03:14:02]. . . 'paragraph' [Text] [id:358][p:355] 
[03:14:03]. . . ' ' [Ws] [id:359][p:355] 
[03:14:04]. . . 'continues' [Text] [id:360][p:355] 
[03:14:05]. . . ' ' [Ws] [id:361][p:355] 
[03:14:06]. . . 'after' [Word] [id:362][p:355] 
[03:14:07]. . . ' ' [Ws] [id:363][p:355] 
[03:14:08]. . . 'the' [Word] [id:364][p:355] 
[03:14:09]. . . ' ' [Ws] [id:365][p:355] 
[03:14:10]. . . 'vertical' [Word] [id:366][p:355] 
[03:14:11]. . . ' ' [Ws] [id:367][p:355] 
[03:14:12]. . . 'list' [Word] [id:368][p:355] 
[03:14:13]. . . '.' [Punct] [id:369][p:355] 
[02:08:07]. . [NoteOrSafetyInstruction] [id:370][p:274] [#2]
[03:02:00]. . . [Sentence] [id:371][p:370] [#8]
[04:08:00]. . . . 'This' [Word] [id:372][p:371] 
[04:08:01]. . . . ' ' [Ws] [id:373][p:371] 
[04:08:02]. . . . 'is' [Text] [id:374][p:371] 
[04:08:03]. . . . ' ' [Ws] [id:375][p:371] 
[04:08:04]. . . . 'a' [Word] [id:376][p:371] 
[04:08:05]. . . . ' ' [Ws] [id:377][p:371] 
[04:08:06]. . . . 'note' [Word] [id:378][p:371] 
[04:08:07]. . . . '.' [Punct] [id:379][p:371] 
[03:02:01]. . . [Sentence] [id:380][p:370] [#18]
[04:18:00]. . . . 'And' [Word] [id:381][p:380] 
[04:18:01]. . . . ' ' [Ws] [id:382][p:380] 
[04:18:02]. . . . 'this' [Word] [id:383][p:380] 
[04:18:03]. . . . ' ' [Ws] [id:384][p:380] 
[04:18:04]. . . . 'note' [Word] [id:385][p:380] 
[04:18:05]. . . . ' ' [Ws] [id:386][p:380] 
[04:18:06]. . . . 'has' [Text] [id:387][p:380] 
[04:18:07]. . . . ' ' [Ws] [id:388][p:380] 
[04:18:08]. . . . 'more' [Word] [id:389][p:380] 
[04:18:09]. . . . ' ' [Ws] [id:390][p:380] 
[04:18:10]. . . . 'than' [Word] [id:391][p:380] 
[04:18:11]. . . . ' ' [Ws] [id:392][p:380] 
[04:18:12]. . . . 'one' [Word] [id:393][p:380] 
[04:18:13]. . . . ' ' [Ws] [id:394][p:380] 
[04:18:14]. . . . 'sentence' [Text] [id:395][p:380] 
[04:18:15]. . . . ' ' [Ws] [id:396][p:380] 
[04:18:16]. . . . [Parentheses] [id:397][p:380] [#1]
[05:01:00]. . . . . [Sentence] [id:398][p:397] [#7]
[06:07:00]. . . . . . 'this' [Word] [id:399][p:398] 
[06:07:01]. . . . . . ' ' [Ws] [id:400][p:398] 
[06:07:02]. . . . . . 'is' [Text] [id:401][p:398] 
[06:07:03]. . . . . . ' ' [Ws] [id:402][p:398] 
[06:07:04]. . . . . . 'sentence' [Text] [id:403][p:398] 
[06:07:05]. . . . . . ' ' [Ws] [id:404][p:398] 
[06:07:06]. . . . . . '2' [Number] [id:405][p:398] 
[04:18:17]. . . . '.' [Punct] [id:406][p:380] 
[01:11:09]. [Heading] [id:407][p:00] [#1]
[02:01:00]. . [Sentence] [id:408][p:407] [#3]
[03:03:00]. . . 'Lorem' [Text] [id:409][p:408] 
[03:03:01]. . . ' ' [Ws] [id:410][p:408] 
[03:03:02]. . . 'ipsum' [Text] [id:411][p:408] 
[01:11:10]. [Paragraph] [id:412][p:00] [#11]
[02:11:00]. . [Sentence] [id:413][p:412] [#17]
[03:17:00]. . . 'Lorem' [Text] [id:414][p:413] 
[03:17:01]. . . ' ' [Ws] [id:415][p:413] 
[03:17:02]. . . 'ipsum' [Text] [id:416][p:413] 
[03:17:03]. . . ' ' [Ws] [id:417][p:413] 
[03:17:04]. . . 'dolor' [Text] [id:418][p:413] 
[03:17:05]. . . ' ' [Ws] [id:419][p:413] 
[03:17:06]. . . 'sit' [Text] [id:420][p:413] 
[03:17:07]. . . ' ' [Ws] [id:421][p:413] 
[03:17:08]. . . 'amet' [Text] [id:422][p:413] 
[03:17:09]. . . ',' [Punct] [id:423][p:413] 
[03:17:10]. . . ' ' [Ws] [id:424][p:413] 
[03:17:11]. . . 'consectetur' [Text] [id:425][p:413] 
[03:17:12]. . . ' ' [Ws] [id:426][p:413] 
[03:17:13]. . . 'adipiscing' [Text] [id:427][p:413] 
[03:17:14]. . . ' ' [Ws] [id:428][p:413] 
[03:17:15]. . . 'elit' [Text] [id:429][p:413] 
[03:17:16]. . . '.' [Punct] [id:430][p:413] 
[02:11:01]. . [Sentence] [id:431][p:412] [#14]
[03:14:00]. . . 'Mauris' [Text] [id:432][p:431] 
[03:14:01]. . . ' ' [Ws] [id:433][p:431] 
[03:14:02]. . . 'vel' [Text] [id:434][p:431] 
[03:14:03]. . . ' ' [Ws] [id:435][p:431] 
[03:14:04]. . . 'arcu' [Text] [id:436][p:431] 
[03:14:05]. . . ' ' [Ws] [id:437][p:431] 
[03:14:06]. . . 'at' [Word] [id:438][p:431] 
[03:14:07]. . . ' ' [Ws] [id:439][p:431] 
[03:14:08]. . . 'enim' [Text] [id:440][p:431] 
[03:14:09]. . . ' ' [Ws] [id:441][p:431] 
[03:14:10]. . . 'elementum' [Text] [id:442][p:431] 
[03:14:11]. . . ' ' [Ws] [id:443][p:431] 
[03:14:12]. . . 'porttitor' [Text] [id:444][p:431] 
[03:14:13]. . . '.' [Punct] [id:445][p:431] 
[02:11:02]. . [Sentence] [id:446][p:412] [#22]
[03:22:00]. . . 'Duis' [Text] [id:447][p:446] 
[03:22:01]. . . ' ' [Ws] [id:448][p:446] 
[03:22:02]. . . 'ante' [Text] [id:449][p:446] 
[03:22:03]. . . ' ' [Ws] [id:450][p:446] 
[03:22:04]. . . 'purus' [Text] [id:451][p:446] 
[03:22:05]. . . ',' [Punct] [id:452][p:446] 
[03:22:06]. . . ' ' [Ws] [id:453][p:446] 
[03:22:07]. . . 'condimentum' [Text] [id:454][p:446] 
[03:22:08]. . . ' ' [Ws] [id:455][p:446] 
[03:22:09]. . . 'eu' [Text] [id:456][p:446] 
[03:22:10]. . . ' ' [Ws] [id:457][p:446] 
[03:22:11]. . . 'nulla' [Text] [id:458][p:446] 
[03:22:12]. . . ' ' [Ws] [id:459][p:446] 
[03:22:13]. . . 'quis' [Text] [id:460][p:446] 
[03:22:14]. . . ',' [Punct] [id:461][p:446] 
[03:22:15]. . . ' ' [Ws] [id:462][p:446] 
[03:22:16]. . . 'molestie' [Text] [id:463][p:446] 
[03:22:17]. . . ' ' [Ws] [id:464][p:446] 
[03:22:18]. . . 'pharetra' [Text] [id:465][p:446] 
[03:22:19]. . . ' ' [Ws] [id:466][p:446] 
[03:22:20]. . . 'est' [Text] [id:467][p:446] 
[03:22:21]. . . '.' [Punct] [id:468][p:446] 
[02:11:03]. . [Sentence] [id:469][p:412] [#8]
[03:08:00]. . . 'Proin' [Text] [id:470][p:469] 
[03:08:01]. . . ' ' [Ws] [id:471][p:469] 
[03:08:02]. . . 'sed' [Text] [id:472][p:469] 
[03:08:03]. . . ' ' [Ws] [id:473][p:469] 
[03:08:04]. . . 'mattis' [Text] [id:474][p:469] 
[03:08:05]. . . ' ' [Ws] [id:475][p:469] 
[03:08:06]. . . 'libero' [Text] [id:476][p:469] 
[03:08:07]. . . '.' [Punct] [id:477][p:469] 
[02:11:04]. . [Sentence] [id:478][p:412] [#12]
[03:12:00]. . . 'Maecenas' [Text] [id:479][p:478] 
[03:12:01]. . . ' ' [Ws] [id:480][p:478] 
[03:12:02]. . . 'lacinia' [Text] [id:481][p:478] 
[03:12:03]. . . ' ' [Ws] [id:482][p:478] 
[03:12:04]. . . 'sem' [Text] [id:483][p:478] 
[03:12:05]. . . ' ' [Ws] [id:484][p:478] 
[03:12:06]. . . 'nec' [Text] [id:485][p:478] 
[03:12:07]. . . ' ' [Ws] [id:486][p:478] 
[03:12:08]. . . 'hendrerit' [Text] [id:487][p:478] 
[03:12:09]. . . ' ' [Ws] [id:488][p:478] 
[03:12:10]. . . 'pulvinar' [Text] [id:489][p:478] 
[03:12:11]. . . '.' [Punct] [id:490][p:478] 
[02:11:05]. . [Sentence] [id:491][p:412] [#22]
[03:22:00]. . . 'Suspendisse' [Text] [id:492][p:491] 
[03:22:01]. . . ' ' [Ws] [id:493][p:491] 
[03:22:02]. . . 'ante' [Text] [id:494][p:491] 
[03:22:03]. . . ' ' [Ws] [id:495][p:491] 
[03:22:04]. . . 'nulla' [Text] [id:496][p:491] 
[03:22:05]. . . ',' [Punct] [id:497][p:491] 
[03:22:06]. . . ' ' [Ws] [id:498][p:491] 
[03:22:07]. . . 'mattis' [Text] [id:499][p:491] 
[03:22:08]. . . ' ' [Ws] [id:500][p:491] 
[03:22:09]. . . 'ut' [Text] [id:501][p:491] 
[03:22:10]. . . ' ' [Ws] [id:502][p:491] 
[03:22:11]. . . 'justo' [Text] [id:503][p:491] 
[03:22:12]. . . ' ' [Ws] [id:504][p:491] 
[03:22:13]. . . 'vel' [Text] [id:505][p:491] 
[03:22:14]. . . ',' [Punct] [id:506][p:491] 
[03:22:15]. . . ' ' [Ws] [id:507][p:491] 
[03:22:16]. . . 'pharetra' [Text] [id:508][p:491] 
[03:22:17]. . . ' ' [Ws] [id:509][p:491] 
[03:22:18]. . . 'finibus' [Text] [id:510][p:491] 
[03:22:19]. . . ' ' [Ws] [id:511][p:491] 
[03:22:20]. . . 'tortor' [Text] [id:512][p:491] 
[03:22:21]. . . '.' [Punct] [id:513][p:491] 
[02:11:06]. . [Sentence] [id:514][p:412] [#8]
[03:08:00]. . . 'Aliquam' [Text] [id:515][p:514] 
[03:08:01]. . . ' ' [Ws] [id:516][p:514] 
[03:08:02]. . . 'ullamcorper' [Text] [id:517][p:514] 
[03:08:03]. . . ' ' [Ws] [id:518][p:514] 
[03:08:04]. . . 'malesuada' [Text] [id:519][p:514] 
[03:08:05]. . . ' ' [Ws] [id:520][p:514] 
[03:08:06]. . . 'ultricies' [Text] [id:521][p:514] 
[03:08:07]. . . '.' [Punct] [id:522][p:514] 
[02:11:07]. . [Sentence] [id:523][p:412] [#35]
[03:35:00]. . . 'Nullam' [Text] [id:524][p:523] 
[03:35:01]. . . ' ' [Ws] [id:525][p:523] 
[03:35:02]. . . 'lacinia' [Text] [id:526][p:523] 
[03:35:03]. . . ',' [Punct] [id:527][p:523] 
[03:35:04]. . . ' ' [Ws] [id:528][p:523] 
[03:35:05]. . . 'ligula' [Text] [id:529][p:523] 
[03:35:06]. . . ' ' [Ws] [id:530][p:523] 
[03:35:07]. . . 'vel' [Text] [id:531][p:523] 
[03:35:08]. . . ' ' [Ws] [id:532][p:523] 
[03:35:09]. . . 'ultricies' [Text] [id:533][p:523] 
[03:35:10]. . . ' ' [Ws] [id:534][p:523] 
[03:35:11]. . . 'rutrum' [Text] [id:535][p:523] 
[03:35:12]. . . ',' [Punct] [id:536][p:523] 
[03:35:13]. . . ' ' [Ws] [id:537][p:523] 
[03:35:14]. . . 'lorem' [Text] [id:538][p:523] 
[03:35:15]. . . ' ' [Ws] [id:539][p:523] 
[03:35:16]. . . 'libero' [Text] [id:540][p:523] 
[03:35:17]. . . ' ' [Ws] [id:541][p:523] 
[03:35:18]. . . 'luctus' [Text] [id:542][p:523] 
[03:35:19]. . . ' ' [Ws] [id:543][p:523] 
[03:35:20]. . . 'neque' [Text] [id:544][p:523] 
[03:35:21]. . . ',' [Punct] [id:545][p:523] 
[03:35:22]. . . ' ' [Ws] [id:546][p:523] 
[03:35:23]. . . 'ut' [Text] [id:547][p:523] 
[03:35:24]. . . ' ' [Ws] [id:548][p:523] 
[03:35:25]. . . 'feugiat' [Text] [id:549][p:523] 
[03:35:26]. . . ' ' [Ws] [id:550][p:523] 
[03:35:27]. . . 'est' [Text] [id:551][p:523] 
[03:35:28]. . . ' ' [Ws] [id:552][p:523] 
[03:35:29]. . . 'justo' [Text] [id:553][p:523] 
[03:35:30]. . . ' ' [Ws] [id:554][p:523] 
[03:35:31]. . . 'vel' [Text] [id:555][p:523] 
[03:35:32]. . . ' ' [Ws] [id:556][p:523] 
[03:35:33]. . . 'sapien' [Text] [id:557][p:523] 
[03:35:34]. . . '.' [Punct] [id:558][p:523] 
[02:11:08]. . [Sentence] [id:559][p:412] [#12]
[03:12:00]. . . 'Etiam' [Text] [id:560][p:559] 
[03:12:01]. . . ' ' [Ws] [id:561][p:559] 
[03:12:02]. . . 'suscipit' [Text] [id:562][p:559] 
[03:12:03]. . . ' ' [Ws] [id:563][p:559] 
[03:12:04]. . . 'mi' [Text] [id:564][p:559] 
[03:12:05]. . . ' ' [Ws] [id:565][p:559] 
[03:12:06]. . . 'vel' [Text] [id:566][p:559] 
[03:12:07]. . . ' ' [Ws] [id:567][p:559] 
[03:12:08]. . . 'sollicitudin' [Text] [id:568][p:559] 
[03:12:09]. . . ' ' [Ws] [id:569][p:559] 
[03:12:10]. . . 'vestibulum' [Text] [id:570][p:559] 
[03:12:11]. . . '.' [Punct] [id:571][p:559] 
[02:11:09]. . [Sentence] [id:572][p:412] [#12]
[03:12:00]. . . 'Mauris' [Text] [id:573][p:572] 
[03:12:01]. . . ' ' [Ws] [id:574][p:572] 
[03:12:02]. . . 'feugiat' [Text] [id:575][p:572] 
[03:12:03]. . . ' ' [Ws] [id:576][p:572] 
[03:12:04]. . . 'volutpat' [Text] [id:577][p:572] 
[03:12:05]. . . ' ' [Ws] [id:578][p:572] 
[03:12:06]. . . 'quam' [Text] [id:579][p:572] 
[03:12:07]. . . ' ' [Ws] [id:580][p:572] 
[03:12:08]. . . 'sed' [Text] [id:581][p:572] 
[03:12:09]. . . ' ' [Ws] [id:582][p:572] 
[03:12:10]. . . 'venenatis' [Text] [id:583][p:572] 
[03:12:11]. . . '.' [Punct] [id:584][p:572] 
[02:11:10]. . [Sentence] [id:585][p:412] [#16]
[03:16:00]. . . 'Praesent' [Text] [id:586][p:585] 
[03:16:01]. . . ' ' [Ws] [id:587][p:585] 
[03:16:02]. . . 'sit' [Text] [id:588][p:585] 
[03:16:03]. . . ' ' [Ws] [id:589][p:585] 
[03:16:04]. . . 'amet' [Text] [id:590][p:585] 
[03:16:05]. . . ' ' [Ws] [id:591][p:585] 
[03:16:06]. . . 'nunc' [Text] [id:592][p:585] 
[03:16:07]. . . ' ' [Ws] [id:593][p:585] 
[03:16:08]. . . 'volutpat' [Text] [id:594][p:585] 
[03:16:09]. . . ' ' [Ws] [id:595][p:585] 
[03:16:10]. . . 'lacus' [Text] [id:596][p:585] 
[03:16:11]. . . ' ' [Ws] [id:597][p:585] 
[03:16:12]. . . 'eleifend' [Text] [id:598][p:585] 
[03:16:13]. . . ' ' [Ws] [id:599][p:585] 
[03:16:14]. . . 'ornare' [Text] [id:600][p:585] 
[03:16:15]. . . '.' [Punct] [id:601][p:585]
```

# Format

  * There are top-level tokens. These are tokens, that must be at the top-most hierarchical level of the text.
  * There are tokens, that can only appear inside other tokens.
  * A text must end with two `NEWLINE` tokens.

## Whitespace (WS)

  * Whitespace is a sequence of either `\t` or ` ` tokens.
  * `\t` is the same as eight ` ` tokens.

```
This is TEXT with whitespace.

This is  TEXT   with    multiple     whitespace.

And\tthis\tis\talso\ttext\twith\twhitespace.
```

## Single space (SPACE)

  * A `SPACE` is a delimiter token that only is inside other `tokens.
  * For example, in `1) Text` the `SPACE` is the delimiter after `1)`. 

```
1) A work step.
```

## NEWLINE

  * A `NEWLINE` is a top-level token.
  * This is a `\r\n` or `\n`.

## TEXT

Any character sequence, that does not contain these characters: `^"'*_`()\s` (regex).

## APOSTROPHE

  * An `APOSTROPHE` is either `'s` or `'` when it comes directly after `TEXT`.
  * You must not put an `APOSTROPHE` in a `squote`.

## Heading

  * A `heading` is a top-level token.
  * A `NEWLINE` that starts with a `# ` (or a multiple of `#`) with one or more `TEXT` tokens.
  * Two `NEWLINE` tokens stop a `heading`.

```
# Heading level 1

## Heading level 2

### Heading level 3

#### Heading level 4

##### Heading level 5

```
## Paragraph

  * A `paragraph` is a top-level token.
  * A `paragraph` starts after a `NEWLINE`, when `TEXT` directly comes after the `NEWLINE` token.
  * Two `NEWLINE` tokens stop a `paragraph`. 
  * A `paragraph` can have a `NEWLINE` token between `TEXT` tokens.

```
This is a paragraph. This is still the paragraph.

This is another paragraph. This is still the second paragraph.
This is still the second paragraph (after a LINEBREAK).

This is a new and the last paragraph.

```

## Procedure (list of work steps)

  * A `procedure` is a top-level token.
  * A `procedure` is one or more *work step* (`proc_item`).
  * A `procedure` starts after a `NEWLINE` token, when `[a-zA-Z0-9]+` (`proc_marker`) and `[.)] ` (`PROC_DELIMITER`) directly come after the `NEWLINE` token.
  * A `proc_item` can contain a vertical list.
  * A `proc_item` can contain a `NOTE` or a safety instruction (`WARNING`, `CAUTION`).
  * In contrast to other markdown, there is no two `NEWLINE` to stop the vertical list, `NOTE` or safety instruction. There is only a single `NEWLINE` to stop one of these.

```
1. This is the first work step.
2. This is the second work step.
  * This is a list item in a work step.
  * Another list item in a work step.
3. This is the third work step.
NOTE: This is a note for the work step.
4. This is the fourth work step.
WARNING: This is a safety instruction for this work step of the type 'WARNING'.
4. This is the fifth work step.
CAUTION: This is a safety instruction for this work step of the type 'CAUTION'.
5. A work step can contain multiple:
  * 'NOTE'
  * 'WARNING'
  * 'CAUTION'.
NOTE: This is a note for the work step.
WARNING: This is a safety instruction for this work step of the type 'WARNING'.
CAUTION: This is a safety instruction for this work step of the type 'CAUTION'.
6. This is the last work step.

```

## Vertical list (`list_item`)

  * A vertical list can occur in a `paragraph` or a procedure (`proc_item`).
  * A vertical list is one or more `lite_item`.
  * A `NEWLINE` starts a `list_item` when `WS+`, a `list_marker` and a `SPACE` come directly after the `NEWLINE` token.
  * Before the `list_item`, there is `TEXT` that has a `:` as the last token.
  * A numeric `list_marker` cannot contain a `.` or `)`. This is only correct for `proc_item`.
  * A `list_marker` has `WS` (indentation).
  * You must not put a vertical list inside another vertical list.

```
This is a paragraph, that starts a list:
  * Indented list item with "*" as the list marker
  * Another list item.

This is another paragraph, that starts a list:
    * More indented list item with "*" as the list marker
    * Another list item.

This is a paragraph, that starts a list:
  1 Indented list item with a numeric as the list marker
  2 Another list item.

This is a paragraph, that starts a list:
  a Indented list item with a lower alpha as the list marker
  a Another list item.

This is a paragraph, that starts a list:
  A Indented list item with an upper alpha as the list marker
  B Another list item.
```

## Parentheses (`paren`)

  * This container can 
  * A `paragraph` can contain `paren`.
  * A `list_item` can contain `paren`.
  * A `proc_item` can contain `paren`.
  * A `cite` can contain `paren`.
  * `paren` must not contain `NEWLINE` tokens.
  * Parentheses can be nested.

## Quote and cite

### Double quote (`dquote`)

  * This formatter shows text in "double quote" (`dquote`).
  * This token cannot contain `NEWLINE`.
  * You must not nest `dquote`.
  * `dquote` can contain `squote`.
  * `squote` can contain "formatters".

```
"this is text in double quote"
```

### Single quote (`squote`)

  * This formatter shows text in 'single quote' (`squote`).
  * This token cannot contain `NEWLINE`.
  * You must not nest `squote`.
  * `squote` can contain `dquote`.
  * `squote` can contain "formatters".

```
*this is text in single quote*
```

### Citation (`cite`)

  * A `cite` is a top-level token.
  * This formatter shows text as a "citation" (`cite`).
  * A `NEWLINE` starts a `cite`, when a `> ` comes directly after the `NEWLINE` token.
  * A `cite` must not be empty. It must contain `TEXT` or `WS`.
  * This token cannot contain `NEWLINE`.
  * You must not nest `cite`.

```
> This is a citation line.
> This is another citation line.

```

## Formatters

### Bold

  * This formatter shows text is **bold** (`bold`).
  * This token cannot contain `NEWLINE`.

```
*this is text in bold*
```

### Emphasis

  * This formatter shows text is _emphasis_  (`emph`).
  * This token cannot contain `NEWLINE`.

```
_this is text in emphasis_
```

### Bold emphasis

  * This formatter shows text is **_bold emphasis_** (`bold_emph`).
  * This token cannot contain `NEWLINE`.

```
*_this is text in bold emphasis_*
```

### Code

  * This formatter shows text is `monospace` (`code`).
  * This token can contain `NEWLINE`.

```
`this is text in monospace`
```

# Examples:

You find examples in [./test/test_data/](./test/test_data/).

## Heading with paragraph

```
# This is a heading level 1

This is the start of a paragraph. And this is the end of the paragraph.

This is a new paragraph. A paragraph continues after a single NEWLINE.
This is still the same paragraph.
```

## Paragraph with vertical lists

```
# This is a heading level 1

This is the start of a paragraph. This will start a new vertical list:
  * Note, that the list delimiter '*' is indented by a minimum of one `WS`.
  * The next list item.
This continues the paragraph. This is not standard 'Github'-flavored Markdown.

This is a new paragraph. This will start a new vertical list:
  - This is another list delimiter.
  - Another list item.

This is a new paragraph. This will start a new vertical list:
 1 This is another list delimiter.
 2 Another list item.

This is another paragraph.

```

## Paragraph with formatters, quotes and cite

```
# This is a heading level 1

## Text in quotes

This is a paragraph. In *this* paragraph we have "text in double quotes".

> Here is a citation. This is similar to a full line in "double quotes".

This is another paragraph. In _that_ paragraph we have 'text in single quotes'.

At last, this is another paragraph. In *_that_* paragraph we have "text in 'double' quotes" that contains "'single' quotes".   

```

# ASD-STE100 Questions

## Parentheses within parentheses?

Is it allowed to place parentheses within parentheses? I would say yes, because:
    * There is no direct "no" that this is not allowed. R8.3
    * You can use parentheses to include a reference to a figure.
    * And you can use parentheses to explain something.
    * This explanation could potentially include a reference to a figure.
    * So, it should be possible to have nested parentheses.
However, this leaves open the option to include more "explanatory" text within a pair of parentheses.

An from R8.5 we would therefore have an infinite nesting of sentences.

I therefore suggest, to explicitly forbid to nest "explanatory" parentheses:
"To explain words or a part of a sentence"

## Multiple sentences in parentheses

Can we have multiple sentences in parentheses? 

## Multiple uses for one set of parentheses?

Can I have an explanation AND an abbreviation inside the same parentheses? Or must I use 2 different parentheses?

Example:
Lock the door (the door on the left side, L1).
Why would I use a COMMA instead of a DOT here? 
---OR---
Lock the door (the door on the left side) (L1).

## Sentence count in vertical lists

R8.4 states:

> Each item in a vertical list that comes after the colon counts as a new sentence.

Where is the rule that states, that a vertical list in full counts as only one sentence.

## "-ing" form as part of a technical noun

> You can use a word that has an -ing form as a technical noun (for example, in procedural titles or headings).

Only for TN or also for regular nouns?

Is this _not_ permitted (because it is a noun and not a technical noun): "cleaning person"

# ASD-STE100 Dictionary

## safety-clip

# R8.4 STE Example
