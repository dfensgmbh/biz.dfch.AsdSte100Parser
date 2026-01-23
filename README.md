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

You must use a special structure of **Markdown** as the input text.

# Format

  * There a top-level tokens. These are tokens, that must be at the top-most hierarchical level of the text.
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
  * For example, in `1) Text` the `SPACE` is the delimter after `1)`. 

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

  * This formatter shows text in "souble quote" (`squote`).
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

  * This formatter shows text is **_bold emphasis_** (`boldemph`).
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
