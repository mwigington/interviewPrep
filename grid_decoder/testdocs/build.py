"""Regenerate the test documents in this directory.

Run from the grid_decoder directory:  python testdocs/build.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from decoder import build_grid, parse_entries  # noqa: E402
from make_test_doc import art_to_html  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

LETTERS = {
    "C": ["████", "█   ", "█   ", "█   ", "████"],
    "A": ["████", "█  █", "████", "█  █", "█  █"],
    "T": ["████", " ██ ", " ██ ", " ██ ", " ██ "],
}


def word(letters: str, gap: int = 1) -> list[str]:
    blocks = [LETTERS[letter] for letter in letters]
    return [(" " * gap).join(parts) for parts in zip(*blocks)]


CASES = [
    (
        "01_letter_L.html",
        "Letter L",
        "Smallest realistic case; confirms the bottom-left origin.",
        ["█   ", "█   ", "█   ", "█   ", "████"],
        {},
    ),
    (
        "02_single_char.html",
        "Single character",
        "Degenerate 1x1 grid: one character at (0,0).",
        ["█"],
        {},
    ),
    (
        "03_offset_and_gaps.html",
        "Offset with blank rows and columns",
        "Leading blank columns, a blank middle row, and blank bottom rows "
        "must all be preserved as spaces.",
        [
            "    ▄▄    ▄▄",
            "    ▀▀    ▀▀",
            "            ",
            "  ▀▄      ▄▀",
            "    ▀▄▄▄▄▀  ",
            "            ",
            "            ",
        ],
        {},
    ),
    (
        "04_shuffled_rows.html",
        "Shuffled table rows",
        "Same letter T, table rows in random order. Output must not depend "
        "on row order in the document.",
        LETTERS["T"],
        {"shuffle_seed": 7},
    ),
    (
        "05_word_CAT.html",
        "Multi-letter message",
        "The realistic case: a sequence of uppercase letters.",
        word("CAT"),
        {},
    ),
    (
        "06_mixed_glyphs.html",
        "Mixed Unicode glyphs",
        "Several distinct block characters, to catch encoding damage on "
        "upload or export.",
        ["░▒▓█▓▒░", "▒▓█ █▓▒", "▓█   █▓"],
        {},
    ),
    (
        "07_column_order_swapped.html",
        "Swapped column order",
        "Bonus robustness check, NOT the assessment's format: columns are "
        "Character / x / y, so the parser must read the header rather than "
        "assume positions.",
        LETTERS["C"],
        {"column_order": ("char", "x", "y")},
    ),
]


def normalize(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.split("\n"))


def main() -> int:
    readme = [
        "# Test documents",
        "",
        "Upload each `.html` file to Google Drive, open it with Google Docs,",
        "then **File > Share > Publish to web** and pass the resulting `/pub`",
        "URL to `print_grid_from_doc`.",
        "",
        "Each file has the same shape as the real example document: a short",
        "paragraph followed by one table with `x-coordinate` / `Character` /",
        "`y-coordinate` columns.",
        "",
        "> Note: the grid is sized from the largest coordinates present, so",
        "> blank rows *below* and blank columns *left of* the content survive",
        "> a round trip, while blank rows above and columns to the right of",
        "> the content cannot be represented at all.",
        "",
        "Regenerate everything with `python testdocs/build.py`.",
        "",
    ]

    failures = 0
    for filename, title, purpose, art, kwargs in CASES:
        html = art_to_html(art, title, **kwargs)
        with open(os.path.join(HERE, filename), "w", encoding="utf-8") as handle:
            handle.write(html)

        rendered = build_grid(parse_entries(html))
        status = "ok" if normalize(rendered) == normalize("\n".join(art)) else "FAILED"
        if status == "FAILED":
            failures += 1
        print(f"{status:6} {filename}")

        readme += [
            f"## `{filename}` — {title}",
            "",
            purpose,
            "",
            "Expected output:",
            "",
            "```",
            rendered,
            "```",
            "",
        ]

    with open(os.path.join(HERE, "README.md"), "w", encoding="utf-8") as handle:
        handle.write("\n".join(readme))

    print(f"\n{len(CASES) - failures}/{len(CASES)} round-tripped through the decoder")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
