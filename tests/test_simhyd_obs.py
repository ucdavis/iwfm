# test_simhyd_obs.py
# unit tests for simhyd_obs function
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

    # 9 header lines (function skips first 9 lines)
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


class TestSimhydObs:
    """Tests for the simhyd_obs function."""

    def test_basic_file_reading(self, tmp_path):
        """Test reading basic groundwater hydrograph file."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "09/30/1973_24:00         478.8368    371.7239    367.5474",
            "10/31/1973_24:00         457.6409    413.6935    413.5092",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        result = iwfm.simhyd_obs(str(gwhyd_file))

        assert len(result) == 2

    def test_returns_list(self, tmp_path):
        """Test that function returns a list."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "09/30/1973_24:00         100.0    200.0    300.0",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        result = iwfm.simhyd_obs(str(gwhyd_file))

        assert isinstance(result, list)

    def test_returns_list_of_lists(self, tmp_path):
        """Test that function returns list of lists."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "09/30/1973_24:00         100.0    200.0    300.0",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        result = iwfm.simhyd_obs(str(gwhyd_file))

        assert isinstance(result[0], list)

    def test_date_column_is_string(self, tmp_path):
        """Test that first column (date) remains a string."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "09/30/1973_24:00         100.0    200.0    300.0",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        result = iwfm.simhyd_obs(str(gwhyd_file))

        # First column should be string (date with _24:00 replaced by space)
        assert isinstance(result[0][0], str)

    def test_value_columns_are_floats(self, tmp_path):
        """Test that value columns are converted to floats."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "09/30/1973_24:00         100.0    200.0    300.0",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        result = iwfm.simhyd_obs(str(gwhyd_file))

        # All columns after first should be floats
        for i in range(1, len(result[0])):
            assert isinstance(result[0][i], float)

    def test_date_format_transformation(self, tmp_path):
        """Test that _24:00 is replaced with space in date."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "09/30/1973_24:00         100.0    200.0    300.0",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        result = iwfm.simhyd_obs(str(gwhyd_file))

        # Date should have _24:00 replaced with space, then split
        # "09/30/1973_24:00" -> "09/30/1973 " -> split -> ["09/30/1973"]
        # But the split happens on whitespace, so first element is date without _24:00
        assert "09/30/1973" in result[0][0]
        assert "_24:00" not in result[0][0]

    def test_correct_values_parsed(self, tmp_path):
        """Test that values are correctly parsed."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "01/01/2000_24:00         123.456    789.012    345.678",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        result = iwfm.simhyd_obs(str(gwhyd_file))

        assert result[0][1] == 123.456
        assert result[0][2] == 789.012
        assert result[0][3] == 345.678

    def test_multiple_data_lines(self, tmp_path):
        """Test reading multiple data lines."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "01/31/1973_24:00         100.0    110.0    120.0",
            "02/28/1973_24:00         200.0    210.0    220.0",
            "03/31/1973_24:00         300.0    310.0    320.0",
            "04/30/1973_24:00         400.0    410.0    420.0",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        result = iwfm.simhyd_obs(str(gwhyd_file))

        assert len(result) == 4
        assert result[0][1] == 100.0
        assert result[1][1] == 200.0
        assert result[2][1] == 300.0
        assert result[3][1] == 400.0

    def test_skips_first_nine_lines(self, tmp_path):
        """Test that function skips exactly 9 header lines."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "09/30/1973_24:00         478.8368    371.7239    367.5474",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        result = iwfm.simhyd_obs(str(gwhyd_file))

        # Should only get the data line, not header lines
        assert len(result) == 1
        # First element should be the date, not header content
        assert "09/30/1973" in result[0][0]

    def test_empty_data_section(self, tmp_path):
        """Test file with no data lines (only headers)."""
        gwhyd_file = tmp_path / "test_gw.out"
        create_gwhyd_file(gwhyd_file, [])

        result = iwfm.simhyd_obs(str(gwhyd_file))

        assert result == []

    def test_single_hydrograph_column(self, tmp_path):
        """Test file with single hydrograph column."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "09/30/1973_24:00         478.8368",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        result = iwfm.simhyd_obs(str(gwhyd_file))

        assert len(result[0]) == 2  # date + one value
        assert result[0][1] == 478.8368

    def test_many_hydrograph_columns(self, tmp_path):
        """Test file with many hydrograph columns."""
        gwhyd_file = tmp_path / "test_gw.out"
        values = " ".join([f"{i * 10.5}" for i in range(1, 11)])
        data_lines = [
            f"09/30/1973_24:00         {values}",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        result = iwfm.simhyd_obs(str(gwhyd_file))

        # date + 10 values
        assert len(result[0]) == 11
        assert result[0][1] == 10.5
        assert result[0][10] == 105.0

    def test_negative_values(self, tmp_path):
        """Test handling of negative values."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "09/30/1973_24:00         -100.5    200.0    -300.5",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        result = iwfm.simhyd_obs(str(gwhyd_file))

        assert result[0][1] == -100.5
        assert result[0][2] == 200.0
        assert result[0][3] == -300.5

    def test_integer_values(self, tmp_path):
        """Test handling of integer values (converted to float)."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "09/30/1973_24:00         100    200    300",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        result = iwfm.simhyd_obs(str(gwhyd_file))

        assert result[0][1] == 100.0
        assert isinstance(result[0][1], float)

    def test_scientific_notation(self, tmp_path):
        """Test handling of scientific notation values."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "09/30/1973_24:00         1.23e+02    4.56e-01    7.89e+00",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        result = iwfm.simhyd_obs(str(gwhyd_file))

        assert abs(result[0][1] - 123.0) < 0.01
        assert abs(result[0][2] - 0.456) < 0.001
        assert abs(result[0][3] - 7.89) < 0.01

    def test_different_date_formats(self, tmp_path):
        """Test various date formats with _24:00 suffix."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "01/01/2000_24:00         100.0",
            "12/31/1999_24:00         200.0",
            "02/29/2000_24:00         300.0",  # Leap year
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        result = iwfm.simhyd_obs(str(gwhyd_file))

        assert len(result) == 3
        assert "01/01/2000" in result[0][0]
        assert "12/31/1999" in result[1][0]
        assert "02/29/2000" in result[2][0]

    def test_preserves_row_order(self, tmp_path):
        """Test that data rows are returned in file order."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "01/31/1973_24:00         100.0",
            "02/28/1973_24:00         200.0",
            "03/31/1973_24:00         300.0",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        result = iwfm.simhyd_obs(str(gwhyd_file))

        assert result[0][1] == 100.0
        assert result[1][1] == 200.0
        assert result[2][1] == 300.0

    def test_zero_values(self, tmp_path):
        """Test handling of zero values."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "09/30/1973_24:00         0.0    0.00    0",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        result = iwfm.simhyd_obs(str(gwhyd_file))

        assert result[0][1] == 0.0
        assert result[0][2] == 0.0
        assert result[0][3] == 0.0

    def test_high_precision_values(self, tmp_path):
        """Test handling of high precision decimal values."""
        gwhyd_file = tmp_path / "test_gw.out"
        data_lines = [
            "09/30/1973_24:00         478.83680123    371.72390456    367.54740789",
        ]
        create_gwhyd_file(gwhyd_file, data_lines)

        result = iwfm.simhyd_obs(str(gwhyd_file))

        assert abs(result[0][1] - 478.83680123) < 1e-6
        assert abs(result[0][2] - 371.72390456) < 1e-6
        assert abs(result[0][3] - 367.54740789) < 1e-6


class TestSimhydObsRealFile:
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

        result = iwfm.simhyd_obs(test_file)

        # Verify we got data back
        assert isinstance(result, list)
        assert len(result) > 0
        # Each row should be a list
        assert isinstance(result[0], list)
        # Should have multiple columns (date + hydrographs)
        assert len(result[0]) > 1

    def test_real_file_data_types(self):
        """Test data types from real file."""
        test_file = os.path.join(
            os.path.dirname(__file__),
            'C2VSimCG-2021',
            'Results',
            'C2VSimCG_Hydrographs_GW.out'
        )

        if not os.path.exists(test_file):
            pytest.skip("Test data file not available")

        result = iwfm.simhyd_obs(test_file)

        # First column should be string (date)
        assert isinstance(result[0][0], str)
        # Remaining columns should be floats
        for i in range(1, len(result[0])):
            assert isinstance(result[0][i], float)

    def test_real_file_first_values(self):
        """Test known values from the real file (truncated test data)."""
        test_file = os.path.join(
            os.path.dirname(__file__),
            'C2VSimCG-2021',
            'Results',
            'C2VSimCG_Hydrographs_GW.out'
        )

        if not os.path.exists(test_file):
            pytest.skip("Test data file not available")

        result = iwfm.simhyd_obs(test_file)

        # First data line from truncated test file:
        # 09/30/1973_24:00          28.3519    -35.2681    -16.6453    -46.3417
        # After _24:00 replacement, date becomes "09/30/1973"
        assert "09/30/1973" in result[0][0]
        assert abs(result[0][1] - 28.3519) < 0.001
        assert abs(result[0][2] - (-35.2681)) < 0.001
        assert abs(result[0][3] - (-16.6453)) < 0.001

    def test_real_file_date_transformation(self):
        """Test that _24:00 is properly removed from dates in real file."""
        test_file = os.path.join(
            os.path.dirname(__file__),
            'C2VSimCG-2021',
            'Results',
            'C2VSimCG_Hydrographs_GW.out'
        )

        if not os.path.exists(test_file):
            pytest.skip("Test data file not available")

        result = iwfm.simhyd_obs(test_file)

        # No date should contain _24:00
        for row in result:
            assert "_24:00" not in row[0]

    def test_real_file_consistent_columns(self):
        """Test that all rows have consistent column count."""
        test_file = os.path.join(
            os.path.dirname(__file__),
            'C2VSimCG-2021',
            'Results',
            'C2VSimCG_Hydrographs_GW.out'
        )

        if not os.path.exists(test_file):
            pytest.skip("Test data file not available")

        result = iwfm.simhyd_obs(test_file)

        # All rows should have same number of columns
        first_row_cols = len(result[0])
        for row in result:
            assert len(row) == first_row_cols
