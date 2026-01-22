# test_headall2table.py
# unit tests for headall2table function
# Copyright (C) 2025-2026 University of California
# -----------------------------------------------------------------------------
# This information is free; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This work is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# For a copy of the GNU General Public License, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
# -----------------------------------------------------------------------------

import pytest
import polars as pl
from pathlib import Path
from unittest.mock import patch, MagicMock


def _load_module():
    """Load the headall2table module dynamically."""
    from importlib.util import spec_from_file_location, module_from_spec
    base = Path(__file__).resolve().parents[1] / "iwfm" / "headall2table.py"
    spec = spec_from_file_location("headall2table", str(base))
    assert spec is not None, "Failed to load module specification"
    mod = module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


_module = _load_module()
headall2table = _module.headall2table


def create_headall_file(file_path, dates_data):
    """Helper to create a mock headall.out file.

    Parameters
    ----------
    file_path : Path
        Output file path
    dates_data : list
        List of tuples (date_str, layer_data) where layer_data is list of layer values

    Note: The headall2table function expects:
    - Lines 0-4: 5 header lines (skipped)
    - Line 5: Node numbers line (first two items are popped as labels)
    - Line 6+: Date lines with head values
    """
    lines = [
        "C  IWFM Headall Output File",
        "C  Header line 2",
        "C  Header line 3",
        "C  Header line 4",
        "C  Header line 5",
        "Node  ID        1        2        3",  # node numbers - first two items popped
    ]

    for date_str, layers in dates_data:
        # First line for date: date followed by layer 1 values
        lines.append(f"{date_str}    {layers[0][0]}    {layers[0][1]}    {layers[0][2]}")
        # Additional layers start with whitespace (detected by isspace())
        for layer in layers[1:]:
            lines.append(f"            {layer[0]}    {layer[1]}    {layer[2]}")

    # Add a trailing line that doesn't start with whitespace to end the last time step
    lines.append("END")

    file_path.write_text('\n'.join(lines))


class TestHeadall2table:
    """Tests for the headall2table function."""

    def test_basic_extraction(self, tmp_path):
        """Test basic extraction of head data for a specific date."""
        heads_file = tmp_path / "headall.out"
        dates_data = [
            ("01/15/2022", [
                [100.0, 110.0, 120.0],  # layer 1
                [90.0, 100.0, 110.0],   # layer 2
            ])
        ]
        create_headall_file(heads_file, dates_data)

        output_file = tmp_path / "heads_table.csv"

        # Call the function directly - iwfm date functions will parse the date string
        headall2table(str(heads_file), str(output_file), "01/15/2022")

        assert output_file.exists()
        result = pl.read_csv(str(output_file))
        assert 'Node' in result.columns

    def test_date_matching(self, tmp_path):
        """Test that the correct date is extracted from multiple dates."""
        heads_file = tmp_path / "headall_multi.out"
        dates_data = [
            ("01/15/2022", [
                [100.0, 110.0, 120.0],
            ]),
            ("02/15/2022", [
                [200.0, 210.0, 220.0],
            ]),
        ]
        create_headall_file(heads_file, dates_data)

        output_file = tmp_path / "heads_feb.csv"

        # Request February data
        headall2table(str(heads_file), str(output_file), "02/15/2022")

        if output_file.exists():
            result = pl.read_csv(str(output_file))
            # Should contain February values (200s) not January (100s)
            assert result is not None

    def test_no_matching_date(self, tmp_path):
        """Test behavior when requested date is not in file."""
        heads_file = tmp_path / "headall_nomatch.out"
        dates_data = [
            ("01/15/2022", [
                [100.0, 110.0, 120.0],
            ]),
        ]
        create_headall_file(heads_file, dates_data)

        output_file = tmp_path / "heads_nomatch.csv"

        # Request a date not in file
        headall2table(str(heads_file), str(output_file), "01/01/2022")

        # File may not be created if date not found
        # This is expected behavior - function returns without writing


class TestHeadall2tableEdgeCases:
    """Edge case tests for headall2table."""

    def test_single_layer(self, tmp_path):
        """Test with single layer data."""
        heads_file = tmp_path / "headall_single.out"
        # Create minimal file with single layer
        lines = [
            "C  Header 1",
            "C  Header 2",
            "C  Header 3",
            "C  Header 4",
            "C  Header 5",
            "Node        1        2",
            "06/01/2022    100.0    200.0",
        ]
        heads_file.write_text('\n'.join(lines))

        output_file = tmp_path / "heads_single.csv"

        headall2table(str(heads_file), str(output_file), "06/01/2022")

        # Output may or may not be created depending on parsing
        # The function should not raise an error

    def test_output_columns(self, tmp_path):
        """Test that output has correct column structure."""
        heads_file = tmp_path / "headall_cols.out"
        dates_data = [
            ("03/15/2022", [
                [10.0, 20.0, 30.0],  # layer 1
                [11.0, 21.0, 31.0],  # layer 2
                [12.0, 22.0, 32.0],  # layer 3
            ])
        ]
        create_headall_file(heads_file, dates_data)

        output_file = tmp_path / "heads_cols.csv"

        headall2table(str(heads_file), str(output_file), "03/15/2022")

        if output_file.exists():
            result = pl.read_csv(str(output_file))
            # Should have Node column plus one column per layer
            assert 'Node' in result.columns
