# test_simhyds.py
# unit tests for simhyds class
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

import pytest

import iwfm


def create_gwhyd_file(filepath, data_lines):
    """Helper to create a minimal IWFM groundwater hydrograph file for testing.

    Parameters
    ----------
    filepath : path
        Path to write the file
    data_lines : list of str
        Data lines to write after the 9 header lines
    """
    lines = []

    # 9 header lines (class skips first 9 lines)
    lines.append("*                                        ***************************************")
    lines.append("*                                        *       GROUNDWATER HYDROGRAPH        *")
    lines.append("*                                        *             (UNIT=FEET)             *")
    lines.append("*                                        ***************************************")
    lines.append("*          HYDROGRAPH ID        1           2           3")
    lines.append("*                  LAYER        1           2           3")
    lines.append("*                   NODE        0           0           0")
    lines.append("*                ELEMENT        6           6           6")
    lines.append("*        TIME")

    # Add data lines
    lines.extend(data_lines)

    filepath.write_text('\n'.join(lines))


class TestSimhydsInit:
    """Tests for simhyds class initialization."""

    def test_basic_initialization(self, tmp_path):
        """Test basic class initialization."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "09/30/1973_24:00         478.8368    371.7239    367.5474",
            "10/31/1973_24:00         457.6409    413.6935    413.5092",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        hyds = iwfm.simhyds(str(gwhyd_file))

        assert hyds is not None

    def test_stores_filename(self, tmp_path):
        """Test that filename is stored."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "09/30/1973_24:00         100.0    200.0    300.0",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        hyds = iwfm.simhyds(str(gwhyd_file))

        assert hyds.filename == str(gwhyd_file)

    def test_sim_vals_is_list(self, tmp_path):
        """Test that sim_vals is a list."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "09/30/1973_24:00         100.0    200.0    300.0",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        hyds = iwfm.simhyds(str(gwhyd_file))

        assert isinstance(hyds.sim_vals, list)

    def test_sim_dates_is_list(self, tmp_path):
        """Test that sim_dates is a list."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "09/30/1973_24:00         100.0    200.0    300.0",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        hyds = iwfm.simhyds(str(gwhyd_file))

        assert isinstance(hyds.sim_dates, list)

    def test_dates_are_datetime(self, tmp_path):
        """Test that dates are parsed as datetime objects."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "09/30/1973_24:00         100.0    200.0    300.0",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        hyds = iwfm.simhyds(str(gwhyd_file))

        assert isinstance(hyds.sim_dates[0], datetime)

    def test_values_are_floats(self, tmp_path):
        """Test that values are converted to floats."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "09/30/1973_24:00         100.0    200.0    300.0",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        hyds = iwfm.simhyds(str(gwhyd_file))

        # First element is datetime, rest are floats
        for i in range(1, len(hyds.sim_vals[0])):
            assert isinstance(hyds.sim_vals[0][i], float)

    def test_correct_values_parsed(self, tmp_path):
        """Test that values are correctly parsed."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "01/01/2000_24:00         123.456    789.012    345.678",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        hyds = iwfm.simhyds(str(gwhyd_file))

        assert hyds.sim_vals[0][1] == 123.456
        assert hyds.sim_vals[0][2] == 789.012
        assert hyds.sim_vals[0][3] == 345.678

    def test_multiple_data_lines(self, tmp_path):
        """Test reading multiple data lines."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "01/31/1973_24:00         100.0    110.0    120.0",
            "02/28/1973_24:00         200.0    210.0    220.0",
            "03/31/1973_24:00         300.0    310.0    320.0",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        hyds = iwfm.simhyds(str(gwhyd_file))

        assert len(hyds.sim_vals) == 3
        assert len(hyds.sim_dates) == 3

    def test_empty_data_section(self, tmp_path):
        """Test file with no data lines (only headers)."""
        gwhyd_file = tmp_path / "test_gw.out"
        create_gwhyd_file(gwhyd_file, [])

        hyds = iwfm.simhyds(str(gwhyd_file))

        assert hyds.sim_vals == []
        assert hyds.sim_dates == []


class TestSimhydsNlines:
    """Tests for nlines method."""

    def test_nlines_single_row(self, tmp_path):
        """Test nlines with single data row."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "09/30/1973_24:00         100.0    200.0    300.0",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        hyds = iwfm.simhyds(str(gwhyd_file))

        assert hyds.nlines() == 1

    def test_nlines_multiple_rows(self, tmp_path):
        """Test nlines with multiple data rows."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "01/31/1973_24:00         100.0    200.0    300.0",
            "02/28/1973_24:00         100.0    200.0    300.0",
            "03/31/1973_24:00         100.0    200.0    300.0",
            "04/30/1973_24:00         100.0    200.0    300.0",
            "05/31/1973_24:00         100.0    200.0    300.0",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        hyds = iwfm.simhyds(str(gwhyd_file))

        assert hyds.nlines() == 5

    def test_nlines_empty(self, tmp_path):
        """Test nlines with no data rows."""
        gwhyd_file = tmp_path / "test_gw.out"
        create_gwhyd_file(gwhyd_file, [])

        hyds = iwfm.simhyds(str(gwhyd_file))

        assert hyds.nlines() == 0


class TestSimhydsNcols:
    """Tests for ncols method."""

    def test_ncols_basic(self, tmp_path):
        """Test ncols returns correct column count."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "09/30/1973_24:00         100.0    200.0    300.0",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        hyds = iwfm.simhyds(str(gwhyd_file))

        # date + 3 values = 4 columns
        assert hyds.ncols() == 4

    def test_ncols_many_columns(self, tmp_path):
        """Test ncols with many columns."""
        gwhyd_file = tmp_path / "test_gw.out"
        values = " ".join([f"{i * 10.0}" for i in range(1, 11)])
        data_lines = [
            f"09/30/1973_24:00         {values}",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        hyds = iwfm.simhyds(str(gwhyd_file))

        # date + 10 values = 11 columns
        assert hyds.ncols() == 11

    def test_ncols_empty_returns_zero(self, tmp_path):
        """Test ncols returns 0 when no data."""
        gwhyd_file = tmp_path / "test_gw.out"
        create_gwhyd_file(gwhyd_file, [])

        hyds = iwfm.simhyds(str(gwhyd_file))

        assert hyds.ncols() == 0


class TestSimhydsDate:
    """Tests for date method."""

    def test_date_first_row(self, tmp_path):
        """Test getting date from first row."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "09/30/1973_24:00         100.0    200.0    300.0",
            "10/31/1973_24:00         100.0    200.0    300.0",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        hyds = iwfm.simhyds(str(gwhyd_file))

        result = hyds.date(0)
        assert isinstance(result, datetime)
        assert result.month == 9
        assert result.day == 30
        assert result.year == 1973

    def test_date_second_row(self, tmp_path):
        """Test getting date from second row."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "09/30/1973_24:00         100.0    200.0    300.0",
            "10/31/1973_24:00         100.0    200.0    300.0",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        hyds = iwfm.simhyds(str(gwhyd_file))

        result = hyds.date(1)
        assert result.month == 10
        assert result.day == 31
        assert result.year == 1973


class TestSimhydsStartEndDate:
    """Tests for start_date and end_date methods."""

    def test_start_date(self, tmp_path):
        """Test start_date returns first row date."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "01/31/1973_24:00         100.0    200.0    300.0",
            "02/28/1973_24:00         100.0    200.0    300.0",
            "03/31/1973_24:00         100.0    200.0    300.0",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        hyds = iwfm.simhyds(str(gwhyd_file))

        result = hyds.start_date()
        assert result.month == 1
        assert result.day == 31
        assert result.year == 1973

    def test_end_date(self, tmp_path):
        """Test end_date returns last row date."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "01/31/1973_24:00         100.0    200.0    300.0",
            "02/28/1973_24:00         100.0    200.0    300.0",
            "03/31/1973_24:00         100.0    200.0    300.0",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        hyds = iwfm.simhyds(str(gwhyd_file))

        result = hyds.end_date()
        assert result.month == 3
        assert result.day == 31
        assert result.year == 1973

    def test_single_row_start_end_same(self, tmp_path):
        """Test that single row has same start and end date."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "06/15/2000_24:00         100.0    200.0    300.0",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        hyds = iwfm.simhyds(str(gwhyd_file))

        assert hyds.start_date() == hyds.end_date()

    def test_start_date_empty_returns_none(self, tmp_path):
        """Test start_date returns None when no data."""
        gwhyd_file = tmp_path / "test_gw.out"
        create_gwhyd_file(gwhyd_file, [])

        hyds = iwfm.simhyds(str(gwhyd_file))

        assert hyds.start_date() is None

    def test_end_date_empty_returns_none(self, tmp_path):
        """Test end_date returns None when no data."""
        gwhyd_file = tmp_path / "test_gw.out"
        create_gwhyd_file(gwhyd_file, [])

        hyds = iwfm.simhyds(str(gwhyd_file))

        assert hyds.end_date() is None


class TestSimhydsGetHead:
    """Tests for get_head method."""

    def test_get_head_first_value(self, tmp_path):
        """Test getting first value column."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "09/30/1973_24:00         100.0    200.0    300.0",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        hyds = iwfm.simhyds(str(gwhyd_file))

        # Column 1 is first value (column 0 is date)
        result = hyds.get_head(0, 1)
        assert result == 100.0

    def test_get_head_different_columns(self, tmp_path):
        """Test getting values from different columns."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "09/30/1973_24:00         100.0    200.0    300.0",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        hyds = iwfm.simhyds(str(gwhyd_file))

        assert hyds.get_head(0, 1) == 100.0
        assert hyds.get_head(0, 2) == 200.0
        assert hyds.get_head(0, 3) == 300.0

    def test_get_head_different_rows(self, tmp_path):
        """Test getting values from different rows."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "01/31/1973_24:00         100.0    110.0    120.0",
            "02/28/1973_24:00         200.0    210.0    220.0",
            "03/31/1973_24:00         300.0    310.0    320.0",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        hyds = iwfm.simhyds(str(gwhyd_file))

        assert hyds.get_head(0, 1) == 100.0
        assert hyds.get_head(1, 1) == 200.0
        assert hyds.get_head(2, 1) == 300.0

    def test_get_head_returns_datetime_for_col_zero(self, tmp_path):
        """Test that column 0 returns datetime."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "09/30/1973_24:00         100.0    200.0    300.0",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        hyds = iwfm.simhyds(str(gwhyd_file))

        result = hyds.get_head(0, 0)
        assert isinstance(result, datetime)


class TestSimhydsSimHead:
    """Tests for sim_head method (interpolation)."""

    def test_sim_head_exact_date(self, tmp_path):
        """Test sim_head with exact matching date."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "01/31/1973_24:00         100.0    200.0    300.0",
            "02/28/1973_24:00         110.0    210.0    310.0",
            "03/31/1973_24:00         120.0    220.0    320.0",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        hyds = iwfm.simhyds(str(gwhyd_file))

        # Get value at exact date - should return exact value
        result = hyds.sim_head("02/28/1973", 1)

        assert result == 110.0

    def test_sim_head_interpolation(self, tmp_path):
        """Test sim_head with date between data points."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "01/01/2000_24:00         100.0    200.0    300.0",
            "01/31/2000_24:00         200.0    300.0    400.0",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        hyds = iwfm.simhyds(str(gwhyd_file))

        # Get interpolated value roughly in middle
        result = hyds.sim_head("01/15/2000", 1)

        # Should be between 100 and 200
        assert 100.0 <= result <= 200.0

    def test_sim_head_different_columns(self, tmp_path):
        """Test sim_head for different columns."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "01/01/2000_24:00         100.0    200.0    300.0",
            "01/31/2000_24:00         100.0    200.0    300.0",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        hyds = iwfm.simhyds(str(gwhyd_file))

        result1 = hyds.sim_head("01/15/2000", 1)
        result2 = hyds.sim_head("01/15/2000", 2)
        result3 = hyds.sim_head("01/15/2000", 3)

        # Values are constant, so interpolation should return same
        assert result1 == 100.0
        assert result2 == 200.0
        assert result3 == 300.0

    def test_sim_head_date_before_start_raises_error(self, tmp_path):
        """Test sim_head raises error for date before simulation start."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "01/31/2000_24:00         100.0    200.0    300.0",
            "02/28/2000_24:00         110.0    210.0    310.0",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        hyds = iwfm.simhyds(str(gwhyd_file))

        with pytest.raises(ValueError, match="before simulation start date"):
            hyds.sim_head("01/01/2000", 1)

    def test_sim_head_date_after_end_raises_error(self, tmp_path):
        """Test sim_head raises error for date after simulation end."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "01/31/2000_24:00         100.0    200.0    300.0",
            "02/28/2000_24:00         110.0    210.0    310.0",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        hyds = iwfm.simhyds(str(gwhyd_file))

        with pytest.raises(ValueError, match="after simulation end date"):
            hyds.sim_head("03/31/2000", 1)

    def test_sim_head_no_data_raises_error(self, tmp_path):
        """Test sim_head raises error when no data available."""
        gwhyd_file = tmp_path / "test_gw.out"
        create_gwhyd_file(gwhyd_file, [])

        hyds = iwfm.simhyds(str(gwhyd_file))

        with pytest.raises(ValueError, match="No simulation data available"):
            hyds.sim_head("01/15/2000", 1)

    def test_sim_head_first_date_exact(self, tmp_path):
        """Test sim_head with exact first date."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "01/31/2000_24:00         100.0    200.0    300.0",
            "02/28/2000_24:00         110.0    210.0    310.0",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        hyds = iwfm.simhyds(str(gwhyd_file))

        result = hyds.sim_head("01/31/2000", 1)

        assert result == 100.0

    def test_sim_head_last_date_exact(self, tmp_path):
        """Test sim_head with exact last date."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "01/31/2000_24:00         100.0    200.0    300.0",
            "02/28/2000_24:00         110.0    210.0    310.0",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        hyds = iwfm.simhyds(str(gwhyd_file))

        result = hyds.sim_head("02/28/2000", 1)

        assert result == 110.0


class TestSimhydsEdgeCases:
    """Edge case tests for simhyds class."""

    def test_negative_values(self, tmp_path):
        """Test handling of negative values."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "09/30/1973_24:00         -100.5    200.0    -300.5",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        hyds = iwfm.simhyds(str(gwhyd_file))

        assert hyds.sim_vals[0][1] == -100.5
        assert hyds.sim_vals[0][3] == -300.5

    def test_leap_year_date(self, tmp_path):
        """Test handling of leap year date."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "02/29/2000_24:00         100.0    200.0    300.0",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        hyds = iwfm.simhyds(str(gwhyd_file))

        assert hyds.sim_dates[0].month == 2
        assert hyds.sim_dates[0].day == 29
        assert hyds.sim_dates[0].year == 2000

    def test_high_precision_values(self, tmp_path):
        """Test handling of high precision values."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "09/30/1973_24:00         478.83680123    371.72390456    367.54740789",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        hyds = iwfm.simhyds(str(gwhyd_file))

        assert abs(hyds.sim_vals[0][1] - 478.83680123) < 1e-6


class TestSimhydsRealFile:
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

        hyds = iwfm.simhyds(test_file)

        # Verify we got data
        assert hyds.nlines() > 0
        assert hyds.ncols() > 1

    def test_real_file_dates_are_datetime(self):
        """Test that dates are datetime objects in real file."""
        test_file = os.path.join(
            os.path.dirname(__file__),
            'C2VSimCG-2021',
            'Results',
            'C2VSimCG_Hydrographs_GW.out'
        )

        if not os.path.exists(test_file):
            pytest.skip("Test data file not available")

        hyds = iwfm.simhyds(test_file)

        assert isinstance(hyds.sim_dates[0], datetime)
        assert isinstance(hyds.start_date(), datetime)
        assert isinstance(hyds.end_date(), datetime)

    def test_real_file_known_first_date(self):
        """Test known first date from real file."""
        test_file = os.path.join(
            os.path.dirname(__file__),
            'C2VSimCG-2021',
            'Results',
            'C2VSimCG_Hydrographs_GW.out'
        )

        if not os.path.exists(test_file):
            pytest.skip("Test data file not available")

        hyds = iwfm.simhyds(test_file)

        # From file inspection: 09/30/1973_24:00
        start = hyds.start_date()
        assert start.month == 9
        assert start.day == 30
        assert start.year == 1973

    def test_real_file_known_first_values(self):
        """Test known first values from real file (truncated test data)."""
        test_file = os.path.join(
            os.path.dirname(__file__),
            'C2VSimCG-2021',
            'Results',
            'C2VSimCG_Hydrographs_GW.out'
        )

        if not os.path.exists(test_file):
            pytest.skip("Test data file not available")

        hyds = iwfm.simhyds(test_file)

        # From truncated test file: 28.3519, -35.2681, -16.6453
        assert abs(hyds.get_head(0, 1) - 28.3519) < 0.001
        assert abs(hyds.get_head(0, 2) - (-35.2681)) < 0.001
        assert abs(hyds.get_head(0, 3) - (-16.6453)) < 0.001

    def test_real_file_date_method(self):
        """Test date method with real file."""
        test_file = os.path.join(
            os.path.dirname(__file__),
            'C2VSimCG-2021',
            'Results',
            'C2VSimCG_Hydrographs_GW.out'
        )

        if not os.path.exists(test_file):
            pytest.skip("Test data file not available")

        hyds = iwfm.simhyds(test_file)

        # date(0) and start_date() should be same
        assert hyds.date(0) == hyds.start_date()
