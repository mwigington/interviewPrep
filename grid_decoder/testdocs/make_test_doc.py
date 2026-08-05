"""Generate Google-Doc-style coordinate tables from ASCII art.

Art is given top row first, as it should appear when printed. Because the
document's y-axis grows upward, the last line of the art is y=0.
"""

import html
import random

Entry = tuple[int, int, str]

HEADERS = {"x": "x-coordinate", "char": "Character", "y": "y-coordinate"}

PREAMBLE = (
    "This is a test document showing the format of the input data for the "
    "coding assessment exercise."
)


def art_to_entries(art: list[str]) -> list[Entry]:
    height = len(art)
    entries: list[Entry] = []
    for row_index, line in enumerate(art):
        y = height - 1 - row_index
        for x, char in enumerate(line):
            if char != " ":
                entries.append((x, y, char))
    return entries


def entries_to_html(
    entries: list[Entry],
    title: str,
    column_order: tuple[str, str, str] = ("x", "char", "y"),
    shuffle_seed: int | None = None,
) -> str:
    entries = list(entries)
    if shuffle_seed is not None:
        random.Random(shuffle_seed).shuffle(entries)

    def cells(values: dict[str, str]) -> str:
        return "".join(f"<td>{html.escape(values[key])}</td>" for key in column_order)

    rows = [f"  <tr>{cells(HEADERS)}</tr>"]
    for x, y, char in entries:
        rows.append(f"  <tr>{cells({'x': str(x), 'char': char, 'y': str(y)})}</tr>")

    return (
        '<!DOCTYPE html>\n<html>\n<head>\n<meta charset="utf-8">\n'
        f"<title>{html.escape(title)}</title>\n</head>\n<body>\n"
        f"<p>{PREAMBLE}</p>\n"
        '<table border="1" cellpadding="6" cellspacing="0">\n'
        + "\n".join(rows)
        + "\n</table>\n</body>\n</html>\n"
    )


def art_to_html(art: list[str], title: str, **kwargs) -> str:
    return entries_to_html(art_to_entries(art), title, **kwargs)
