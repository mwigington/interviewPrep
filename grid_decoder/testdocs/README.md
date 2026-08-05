# Test documents

Upload each `.html` file to Google Drive, open it with Google Docs,
then **File > Share > Publish to web** and pass the resulting `/pub`
URL to `print_grid_from_doc`.

Each file has the same shape as the real example document: a short
paragraph followed by one table with `x-coordinate` / `Character` /
`y-coordinate` columns.

> Note: the grid is sized from the largest coordinates present, so
> blank rows *below* and blank columns *left of* the content survive
> a round trip, while blank rows above and columns to the right of
> the content cannot be represented at all.

Regenerate everything with `python testdocs/build.py`.

## `01_letter_L.html` — Letter L

Smallest realistic case; confirms the bottom-left origin.

Expected output:

```
█   
█   
█   
█   
████
```

## `02_single_char.html` — Single character

Degenerate 1x1 grid: one character at (0,0).

Expected output:

```
█
```

## `03_offset_and_gaps.html` — Offset with blank rows and columns

Leading blank columns, a blank middle row, and blank bottom rows must all be preserved as spaces.

Expected output:

```
    ▄▄    ▄▄
    ▀▀    ▀▀
            
  ▀▄      ▄▀
    ▀▄▄▄▄▀  
            
            
```

## `04_shuffled_rows.html` — Shuffled table rows

Same letter T, table rows in random order. Output must not depend on row order in the document.

Expected output:

```
████
 ██ 
 ██ 
 ██ 
 ██ 
```

## `05_word_CAT.html` — Multi-letter message

The realistic case: a sequence of uppercase letters.

Expected output:

```
████ ████ ████
█    █  █  ██ 
█    ████  ██ 
█    █  █  ██ 
████ █  █  ██ 
```

## `06_mixed_glyphs.html` — Mixed Unicode glyphs

Several distinct block characters, to catch encoding damage on upload or export.

Expected output:

```
░▒▓█▓▒░
▒▓█ █▓▒
▓█   █▓
```

## `07_column_order_swapped.html` — Swapped column order

Bonus robustness check, NOT the assessment's format: columns are Character / x / y, so the parser must read the header rather than assume positions.

Expected output:

```
████
█   
█   
█   
████
```
