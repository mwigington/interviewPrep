from typing import Iterable

import requests
from bs4 import BeautifulSoup

Entry = tuple[int, int, str]


def _fetch_gdoc(url: str) -> str:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.text


def _identify_columns(header_row: list[str]) -> tuple[int, int, int]:
    x_idx = y_idx = char_idx = None
    for idx, raw_cell in enumerate(header_row):
        header_cell = raw_cell.strip().lower()
        if header_cell.startswith("x"):
            x_idx = i
        elif header_cell.startswith("y"):
            y_idx = i
        else:
            char_idx = i
    if x_idx is None or y_idx is None or char_idx is None:
        raise ValueError(f"Could not identify columns from headers: {header_row}")
    return x_idx, y_idx, char_idx


def _parse_table(html: str) -> list[Entry]:
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if table is None:
        raise ValueError("No <table> found in document")

    rows = table.find_all("tr")
    if len(rows) < 2:
        raise ValueError("Table has no data rows")

    header_row = [c.get_text().strip() for c in rows[0].find_all(["td", "th"])]
    x_idx, y_idx, char_idx = _identify_columns(header_row)

    entries: list[Entry] = []
    for row in rows[1:]:
        cells = row.find_all(["td", "th"])
        if len(cells) < 3:
            continue
        char = cells[char_idx].get_text().strip()
        if not char:
            continue
        x = int(cells[x_idx].get_text().strip())
        y = int(cells[y_idx].get_text().strip())
        entries.append((x, y, char))
    return entries


def _build_letter(entries: Iterable[Entry]) -> str:
    entries = list(entries)
    if not entries:
        return ""
    width = max(x for x, _, _ in entries) + 1
    height = max(y for _, y, _ in entries) + 1
    letter_grid = [[" "] * width for _ in range(height)]
    for x, y, char in entries:
        letter_grid[height-1-y][x] = char
    letter = "\n".join("".join(row) for row in grid)
    return letter


def print_gdoc_letter(url: str) -> str:
    html = _fetch_gdoc(url)
    entries = _parse_table(html)
    letter = _build_letter(entries)
    print(letter)
    return letter


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python decoder.py <google-doc-url>", file=sys.stderr)
        sys.exit(1)
    print_grid_from_doc(sys.argv[1])

