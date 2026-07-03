from typing import Iterable

import requests
from bs4 import BeautifulSoup

Entry = tuple[int, int, str]


def fetch_doc(url: str) -> str:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.text


def _identify_columns(header_cells: list[str]) -> tuple[int, int, int]:
    x_idx = y_idx = char_idx = None
    for i, raw in enumerate(header_cells):
        h = raw.strip().lower()
        if h.startswith("x"):
            x_idx = i
        elif h.startswith("y"):
            y_idx = i
        else:
            char_idx = i
    if x_idx is None or y_idx is None or char_idx is None:
        raise ValueError(f"Could not identify x/y/char columns from headers: {header_cells}")
    return x_idx, y_idx, char_idx


def parse_entries(html: str) -> list[Entry]:
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if table is None:
        raise ValueError("No <table> found in document")

    rows = table.find_all("tr")
    if len(rows) < 2:
        raise ValueError("Table has no data rows")

    header_texts = [c.get_text().strip() for c in rows[0].find_all(["td", "th"])]
    x_idx, y_idx, char_idx = _identify_columns(header_texts)

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


def build_grid(entries: Iterable[Entry]) -> str:
    entries = list(entries)
    if not entries:
        return ""
    width = max(x for x, _, _ in entries) + 1
    height = max(y for _, y, _ in entries) + 1
    grid = [[" "] * width for _ in range(height)]
    for x, y, char in entries:
        grid[y][x] = char
    return "\n".join("".join(row) for row in grid)


def print_grid_from_doc(url: str) -> str:
    html = fetch_doc(url)
    entries = parse_entries(html)
    grid = build_grid(entries)
    print(grid)
    return grid


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python decoder.py <google-doc-url>", file=sys.stderr)
        sys.exit(1)
    print_grid_from_doc(sys.argv[1])
