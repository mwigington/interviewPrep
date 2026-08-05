import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from decoder import build_grid, parse_entries  # noqa: E402


def test_build_grid_single_point_at_origin():
    assert build_grid([(0, 0, "A")]) == "A"


def test_build_grid_offset_point_pads_rows_and_columns():
    grid = build_grid([(5, 2, "X")])
    lines = grid.split("\n")
    assert len(lines) == 3
    assert all(len(line) == 6 for line in lines)
    assert lines[0] == "     X"
    assert lines[1] == "      "
    assert lines[2] == "      "


def test_build_grid_dense_2x2():
    entries = [
        (0, 0, "A"), (1, 0, "B"),
        (0, 1, "C"), (1, 1, "D"),
    ]
    assert build_grid(entries) == "CD\nAB"


def test_build_grid_sparse_positions_fill_with_spaces():
    entries = [(0, 0, "X"), (2, 1, "Y")]
    assert build_grid(entries) == "  Y\nX  "


def test_build_grid_empty_input_returns_empty_string():
    assert build_grid([]) == ""


def test_build_grid_letter_H_shape():
    entries = [
        (0, 0, "█"), (2, 0, "█"),
        (0, 1, "█"), (2, 1, "█"),
        (0, 2, "█"), (1, 2, "█"), (2, 2, "█"),
        (0, 3, "█"), (2, 3, "█"),
        (0, 4, "█"), (2, 4, "█"),
    ]
    expected = "\n".join(["█ █", "█ █", "███", "█ █", "█ █"])
    assert build_grid(entries) == expected


def test_build_grid_origin_is_bottom_left():
    entries = [(0, 0, "B"), (0, 2, "T")]
    assert build_grid(entries) == "T\n \nB"


def test_build_grid_example_doc_letter_F():
    entries = [
        (0, 0, "█"),
        (0, 1, "█"), (1, 1, "▀"), (2, 1, "▀"),
        (0, 2, "█"), (1, 2, "▀"), (2, 2, "▀"), (3, 2, "▀"),
    ]
    expected = "\n".join(["█▀▀▀", "█▀▀ ", "█   "])
    assert build_grid(entries) == expected


HTML_X_CHAR_Y = """
<html><body>
<table>
  <tr><th>x-coordinate</th><th>Character</th><th>y-coordinate</th></tr>
  <tr><td>0</td><td>A</td><td>0</td></tr>
  <tr><td>1</td><td>B</td><td>0</td></tr>
  <tr><td>0</td><td>C</td><td>1</td></tr>
</table>
</body></html>
"""


def test_parse_entries_x_char_y_column_order():
    assert set(parse_entries(HTML_X_CHAR_Y)) == {
        (0, 0, "A"),
        (1, 0, "B"),
        (0, 1, "C"),
    }


HTML_CHAR_X_Y = """
<html><body>
<table>
  <tr><th>Character</th><th>x-coordinate</th><th>y-coordinate</th></tr>
  <tr><td>A</td><td>0</td><td>0</td></tr>
  <tr><td>B</td><td>1</td><td>0</td></tr>
</table>
</body></html>
"""


def test_parse_entries_char_x_y_column_order():
    assert set(parse_entries(HTML_CHAR_X_Y)) == {(0, 0, "A"), (1, 0, "B")}


HTML_UNICODE_GLYPHS = """
<html><body>
<table>
  <tr><th>x-coordinate</th><th>Character</th><th>y-coordinate</th></tr>
  <tr><td>0</td><td>█</td><td>0</td></tr>
  <tr><td>1</td><td>░</td><td>0</td></tr>
</table>
</body></html>
"""


def test_parse_entries_preserves_unicode_glyphs():
    assert set(parse_entries(HTML_UNICODE_GLYPHS)) == {(0, 0, "█"), (1, 0, "░")}


def test_parse_entries_raises_when_no_table():
    with pytest.raises(ValueError, match="No <table>"):
        parse_entries("<html><body><p>no table here</p></body></html>")


def test_end_to_end_parse_then_build():
    entries = parse_entries(HTML_X_CHAR_Y)
    assert build_grid(entries) == "C \nAB"


HTML_EXAMPLE_DOC = """
<html><body>
<p>This is an example document showing the format of the input data for the
coding assessment exercise.</p>
<table>
  <tr><td>x-coordinate</td><td>Character</td><td>y-coordinate</td></tr>
  <tr><td>0</td><td>█</td><td>0</td></tr>
  <tr><td>0</td><td>█</td><td>1</td></tr>
  <tr><td>0</td><td>█</td><td>2</td></tr>
  <tr><td>1</td><td>▀</td><td>1</td></tr>
  <tr><td>1</td><td>▀</td><td>2</td></tr>
  <tr><td>2</td><td>▀</td><td>1</td></tr>
  <tr><td>2</td><td>▀</td><td>2</td></tr>
  <tr><td>3</td><td>▀</td><td>2</td></tr>
</table>
</body></html>
"""


def test_end_to_end_example_doc_renders_letter_F():
    grid = build_grid(parse_entries(HTML_EXAMPLE_DOC))
    assert grid == "\n".join(["█▀▀▀", "█▀▀ ", "█   "])
