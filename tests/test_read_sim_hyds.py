# test_read_sim_hyds.py
# unit tests for read_sim_hyds function
# Copyright (C) 2026 University of California
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
import os
from datetime import datetime

import numpy as np
import pytest

import iwfm


def create_gw_hyd_file(filepath, data_rows, num_hydrographs=3):
    """Helper to create an IWFM groundwater hydrograph output file for testing.

    Parameters
    ----------
    filepath : path
        Path to write the file
    data_rows : list
        List of tuples: (date_str, values_list)
        e.g., [('09/30/1973_24:00', [100.0, 200.0, 300.0])]
    num_hydrographs : int
        Number of hydrographs (columns)
    """
    lines = []

    # Header lines (lines 0-3)
    lines.append("*                                        ***************************************")
    lines.append("*                                        *       GROUNDWATER HYDROGRAPH        *")
    lines.append("*                                        *             (UNIT=FEET)             *")
    lines.append("*                                        ***************************************")

    # Column header lines (lines 4-8)
    hyd_ids = ''.join(f'{i+1:12d}' for i in range(num_hydrographs))
    lines.append(f"*          HYDROGRAPH ID{hyd_ids}")

    layers = ''.join(f'{1:12d}' for _ in range(num_hydrographs))
    lines.append(f"*                  LAYER{layers}")

    nodes = ''.join(f'{0:12d}' for _ in range(num_hydrographs))
    lines.append(f"*                   NODE{nodes}")

    elements = ''.join(f'{i+1:12d}' for i in range(num_hydrographs))
    lines.append(f"*                ELEMENT{elements}")

    lines.append("*        TIME")

    # Data lines (starting at line 9)
    for date_str, values in data_rows:
        values_str = ''.join(f'{v:12.4f}' for v in values)
        lines.append(f"{date_str}{values_str}")

    filepath.write_text('\n'.join(lines))


class TestReadSimHyds:
    """Tests for the read_sim_hyds function."""

    def test_basic_single_file(self, tmp_path):
        """Test reading single hydrograph file."""
        hyd_file = tmp_path / "hydrograph.out"
        data_rows = [
            ('09/30/1973_24:00', [100.0, 200.0, 300.0]),
            ('10/31/1973_24:00', [105.0, 205.0, 305.0]),
        ]
        create_gw_hyd_file(hyd_file, data_rows, num_hydrographs=3)

        result = iwfm.read_sim_hyds([str(hyd_file)])

        assert len(result) == 1
        assert isinstance(result[0], np.ndarray)

    def test_multiple_files(self, tmp_path):
        """Test reading multiple hydrograph files."""
        hyd_file1 = tmp_path / "hydrograph1.out"
        hyd_file2 = tmp_path / "hydrograph2.out"
        data_rows = [
            ('09/30/1973_24:00', [100.0, 200.0]),
            ('10/31/1973_24:00', [105.0, 205.0]),
        ]
        create_gw_hyd_file(hyd_file1, data_rows, num_hydrographs=2)
        create_gw_hyd_file(hyd_file2, data_rows, num_hydrographs=2)

        result = iwfm.read_sim_hyds([str(hyd_file1), str(hyd_file2)])

        assert len(result) == 2
        assert isinstance(result[0], np.ndarray)
        assert isinstance(result[1], np.ndarray)

    def test_returns_list(self, tmp_path):
        """Test that function returns a list."""
        hyd_file = tmp_path / "hydrograph.out"
        data_rows = [('09/30/1973_24:00', [100.0])]
        create_gw_hyd_file(hyd_file, data_rows, num_hydrographs=1)

        result = iwfm.read_sim_hyds([str(hyd_file)])

        assert isinstance(result, list)

    def test_returns_numpy_arrays(self, tmp_path):
        """Test that each item in result is a numpy array."""
        hyd_file = tmp_path / "hydrograph.out"
        data_rows = [('09/30/1973_24:00', [100.0, 200.0])]
        create_gw_hyd_file(hyd_file, data_rows, num_hydrographs=2)

        result = iwfm.read_sim_hyds([str(hyd_file)])

        assert isinstance(result[0], np.ndarray)

    def test_array_shape(self, tmp_path):
        """Test that array has correct shape (rows x columns)."""
        hyd_file = tmp_path / "hydrograph.out"
        data_rows = [
            ('09/30/1973_24:00', [100.0, 200.0, 300.0]),
            ('10/31/1973_24:00', [105.0, 205.0, 305.0]),
            ('11/30/1973_24:00', [110.0, 210.0, 310.0]),
        ]
        create_gw_hyd_file(hyd_file, data_rows, num_hydrographs=3)

        result = iwfm.read_sim_hyds([str(hyd_file)])

        # 3 rows, 4 columns (date + 3 values)
        assert result[0].shape == (3, 4)

    def test_first_column_is_datetime(self, tmp_path):
        """Test that first column contains datetime objects."""
        hyd_file = tmp_path / "hydrograph.out"
        data_rows = [('09/30/1973_24:00', [100.0])]
        create_gw_hyd_file(hyd_file, data_rows, num_hydrographs=1)

        result = iwfm.read_sim_hyds([str(hyd_file)])

        # First column should be datetime
        first_date = result[0][0, 0]
        assert isinstance(first_date, datetime)

    def test_date_parsing(self, tmp_path):
        """Test that dates are parsed correctly."""
        hyd_file = tmp_path / "hydrograph.out"
        data_rows = [
            ('09/30/1973_24:00', [100.0]),
            ('10/31/1973_24:00', [105.0]),
        ]
        create_gw_hyd_file(hyd_file, data_rows, num_hydrographs=1)

        result = iwfm.read_sim_hyds([str(hyd_file)])

        # Check first date: 09/30/1973
        assert result[0][0, 0].month == 9
        assert result[0][0, 0].day == 30
        assert result[0][0, 0].year == 1973

        # Check second date: 10/31/1973
        assert result[0][1, 0].month == 10
        assert result[0][1, 0].day == 31
        assert result[0][1, 0].year == 1973

    def test_24_00_removed_from_date(self, tmp_path):
        """Test that _24:00 is removed from date string before parsing."""
        hyd_file = tmp_path / "hydrograph.out"
        # The date format in IWFM is MM/DD/YYYY_24:00
        data_rows = [('12/31/2000_24:00', [100.0])]
        create_gw_hyd_file(hyd_file, data_rows, num_hydrographs=1)

        result = iwfm.read_sim_hyds([str(hyd_file)])

        # Should parse without error
        assert result[0][0, 0].year == 2000
        assert result[0][0, 0].month == 12
        assert result[0][0, 0].day == 31

    def test_values_are_floats(self, tmp_path):
        """Test that hydrograph values are floats."""
        hyd_file = tmp_path / "hydrograph.out"
        data_rows = [('09/30/1973_24:00', [123.456, 789.012])]
        create_gw_hyd_file(hyd_file, data_rows, num_hydrographs=2)

        result = iwfm.read_sim_hyds([str(hyd_file)])

        # Values start at column 1
        assert abs(result[0][0, 1] - 123.456) < 0.001
        assert abs(result[0][0, 2] - 789.012) < 0.001

    def test_correct_values_extracted(self, tmp_path):
        """Test that correct values are extracted from file."""
        hyd_file = tmp_path / "hydrograph.out"
        data_rows = [
            ('09/30/1973_24:00', [100.5, 200.5, 300.5]),
            ('10/31/1973_24:00', [110.5, 210.5, 310.5]),
        ]
        create_gw_hyd_file(hyd_file, data_rows, num_hydrographs=3)

        result = iwfm.read_sim_hyds([str(hyd_file)])

        # Check first row values
        assert abs(result[0][0, 1] - 100.5) < 0.01
        assert abs(result[0][0, 2] - 200.5) < 0.01
        assert abs(result[0][0, 3] - 300.5) < 0.01

        # Check second row values
        assert abs(result[0][1, 1] - 110.5) < 0.01
        assert abs(result[0][1, 2] - 210.5) < 0.01
        assert abs(result[0][1, 3] - 310.5) < 0.01

    def test_negative_values(self, tmp_path):
        """Test reading negative hydrograph values."""
        hyd_file = tmp_path / "hydrograph.out"
        data_rows = [('09/30/1973_24:00', [-50.0, -100.0])]
        create_gw_hyd_file(hyd_file, data_rows, num_hydrographs=2)

        result = iwfm.read_sim_hyds([str(hyd_file)])

        assert result[0][0, 1] == -50.0
        assert result[0][0, 2] == -100.0

    def test_zero_values(self, tmp_path):
        """Test reading zero hydrograph values."""
        hyd_file = tmp_path / "hydrograph.out"
        data_rows = [('09/30/1973_24:00', [0.0, 0.0])]
        create_gw_hyd_file(hyd_file, data_rows, num_hydrographs=2)

        result = iwfm.read_sim_hyds([str(hyd_file)])

        assert result[0][0, 1] == 0.0
        assert result[0][0, 2] == 0.0

    def test_large_values(self, tmp_path):
        """Test reading large hydrograph values."""
        hyd_file = tmp_path / "hydrograph.out"
        data_rows = [('09/30/1973_24:00', [9999.9999, 12345.6789])]
        create_gw_hyd_file(hyd_file, data_rows, num_hydrographs=2)

        result = iwfm.read_sim_hyds([str(hyd_file)])

        assert abs(result[0][0, 1] - 9999.9999) < 0.0001
        assert abs(result[0][0, 2] - 12345.6789) < 0.0001

    def test_many_timesteps(self, tmp_path):
        """Test reading file with many timesteps."""
        hyd_file = tmp_path / "hydrograph.out"
        # Create 100 timesteps
        data_rows = [
            (f'{(i % 12) + 1:02d}/{28}/1973_24:00', [float(i * 10)])
            for i in range(1, 101)
        ]
        create_gw_hyd_file(hyd_file, data_rows, num_hydrographs=1)

        result = iwfm.read_sim_hyds([str(hyd_file)])

        assert result[0].shape[0] == 100

    def test_many_hydrographs(self, tmp_path):
        """Test reading file with many hydrographs (columns)."""
        hyd_file = tmp_path / "hydrograph.out"
        num_hyds = 50
        data_rows = [
            ('09/30/1973_24:00', [float(i) for i in range(num_hyds)]),
        ]
        create_gw_hyd_file(hyd_file, data_rows, num_hydrographs=num_hyds)

        result = iwfm.read_sim_hyds([str(hyd_file)])

        # Shape should be (1 row, 51 columns = 1 date + 50 values)
        assert result[0].shape == (1, num_hyds + 1)

    def test_file_not_found_raises_error(self, tmp_path):
        """Test that nonexistent file raises FileNotFoundError."""
        nonexistent = tmp_path / "nonexistent.out"

        with pytest.raises(FileNotFoundError):
            iwfm.read_sim_hyds([str(nonexistent)])

    def test_empty_file_list(self):
        """Test with empty file list."""
        result = iwfm.read_sim_hyds([])

        assert result == []

    def test_skips_header_lines(self, tmp_path):
        """Test that first 9 lines are skipped."""
        hyd_file = tmp_path / "hydrograph.out"
        data_rows = [('09/30/1973_24:00', [100.0])]
        create_gw_hyd_file(hyd_file, data_rows, num_hydrographs=1)

        result = iwfm.read_sim_hyds([str(hyd_file)])

        # Should have 1 data row (header lines skipped)
        assert result[0].shape[0] == 1


class TestReadSimHydsRealFile:
    """Tests using real IWFM test data files."""

    def test_with_real_hydrograph_file(self):
        """Test with actual C2VSimCG hydrograph file if available."""
        test_file = os.path.join(
            os.path.dirname(__file__),
            'C2VSimCG-2021',
            'Results',
            'C2VSimCG_Hydrographs_GW.out'
        )

        if not os.path.exists(test_file):
            pytest.skip("Test data file not available")

        result = iwfm.read_sim_hyds([test_file])

        # Verify we got a list with one numpy array
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], np.ndarray)

        # Should have many rows and columns
        assert result[0].shape[0] > 0  # rows (timesteps)
        assert result[0].shape[1] > 1  # columns (date + hydrographs)

    def test_with_multiple_real_files(self):
        """Test with multiple actual hydrograph files."""
        test_file1 = os.path.join(
            os.path.dirname(__file__),
            'C2VSimCG-2021',
            'Results',
            'C2VSimCG_Hydrographs_GW.out'
        )
        test_file2 = os.path.join(
            os.path.dirname(__file__),
            'C2VSimCG-2021',
            'Results',
            'C2VSimCG_Hydrographs_GW_mod.out'
        )

        if not os.path.exists(test_file1) or not os.path.exists(test_file2):
            pytest.skip("Test data files not available")

        result = iwfm.read_sim_hyds([test_file1, test_file2])

        assert len(result) == 2
        assert isinstance(result[0], np.ndarray)
        assert isinstance(result[1], np.ndarray)

    def test_real_file_dates_are_datetime(self):
        """Test that dates in real file are parsed as datetime objects."""
        test_file = os.path.join(
            os.path.dirname(__file__),
            'C2VSimCG-2021',
            'Results',
            'C2VSimCG_Hydrographs_GW.out'
        )

        if not os.path.exists(test_file):
            pytest.skip("Test data file not available")

        result = iwfm.read_sim_hyds([test_file])

        # Check first date is datetime
        first_date = result[0][0, 0]
        assert isinstance(first_date, datetime)

    def test_real_file_known_values(self):
        """Test known values from the real file."""
        test_file = os.path.join(
            os.path.dirname(__file__),
            'C2VSimCG-2021',
            'Results',
            'C2VSimCG_Hydrographs_GW.out'
        )

        if not os.path.exists(test_file):
            pytest.skip("Test data file not available")

        result = iwfm.read_sim_hyds([test_file])

        # From file inspection:
        # First data line: 09/30/1973_24:00 with first value ~478.8368
        first_date = result[0][0, 0]
        assert first_date.month == 9
        assert first_date.day == 30
        assert first_date.year == 1973

        # First hydrograph value should be approximately 28.3519
        first_value = result[0][0, 1]
        assert abs(first_value - 28.3519) < 0.01

    def test_real_file_all_values_numeric(self):
        """Test that all non-date values in real file are numeric."""
        test_file = os.path.join(
            os.path.dirname(__file__),
            'C2VSimCG-2021',
            'Results',
            'C2VSimCG_Hydrographs_GW.out'
        )

        if not os.path.exists(test_file):
            pytest.skip("Test data file not available")

        result = iwfm.read_sim_hyds([test_file])

        # Check that all values except first column are numeric
        for row in range(min(10, result[0].shape[0])):  # Check first 10 rows
            for col in range(1, min(10, result[0].shape[1])):  # Check first 10 value columns
                val = result[0][row, col]
                assert isinstance(val, (int, float, np.integer, np.floating)), \
                    f"Value at ({row}, {col}) is not numeric: {type(val)}"
