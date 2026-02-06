# test_read_obs_smp.py
# unit tests for read_obs_smp function
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


def create_smp_file(filepath, observations):
    """Helper to create a PEST-style smp file for testing.

    Parameters
    ----------
    filepath : path
        Path to write the file
    observations : list
        List of tuples: (name, date, time, value)
    """
    lines = []
    for obs in observations:
        name, date, time, value = obs
        lines.append(f" {name}            {date}   {time}   {value}")
    filepath.write_text('\n'.join(lines))


# ---------------------------------------------------------------------------
# Helpers to access polars DataFrame or dict results uniformly
# ---------------------------------------------------------------------------

def _is_polars(result):
    """Return True if result is a polars DataFrame."""
    try:
        import polars as pl
        return isinstance(result, pl.DataFrame)
    except ImportError:
        return False


def _nrows(result):
    """Return number of rows in result (polars DataFrame or dict)."""
    if _is_polars(result):
        return len(result)
    return len(result['site_name'])


def _col(result, col_name, idx=None):
    """Return value(s) from a column.  If idx is None return the list."""
    if _is_polars(result):
        series = result.select(col_name).to_series().to_list()
    else:
        series = result[col_name]
    if idx is not None:
        return series[idx]
    return series


class TestReadObsSmp:
    """Tests for the read_obs_smp function (polars DataFrame or dict return)."""

    def test_basic_single_observation(self, tmp_path):
        """Test reading file with single observation."""
        smp_file = tmp_path / "obs.smp"
        observations = [
            ("WELLNAME", "01/15/2000", "00:00:00", 125.50)
        ]
        create_smp_file(smp_file, observations)

        result = iwfm.read_obs_smp(str(smp_file))

        assert _nrows(result) == 1
        assert _col(result, 'site_name', 0) == "WELLNAME"
        assert _col(result, 'date', 0) == datetime(2000, 1, 15)
        assert _col(result, 'time', 0) == "00:00:00"
        assert _col(result, 'obs_value', 0) == 125.50

    def test_multiple_observations(self, tmp_path):
        """Test reading file with multiple observations."""
        smp_file = tmp_path / "obs.smp"
        observations = [
            ("WELL1", "01/15/2000", "00:00:00", 100.0),
            ("WELL1", "02/15/2000", "00:00:00", 105.0),
            ("WELL2", "01/15/2000", "00:00:00", 200.0),
        ]
        create_smp_file(smp_file, observations)

        result = iwfm.read_obs_smp(str(smp_file))

        assert _nrows(result) == 3

    def test_returns_polars_or_dict(self, tmp_path):
        """Test that function returns a polars DataFrame or dict."""
        smp_file = tmp_path / "obs.smp"
        observations = [("WELL1", "01/15/2000", "00:00:00", 100.0)]
        create_smp_file(smp_file, observations)

        result = iwfm.read_obs_smp(str(smp_file))

        assert _is_polars(result) or isinstance(result, dict)

    def test_has_four_columns(self, tmp_path):
        """Test that result has four columns: site_name, date, time, obs_value."""
        smp_file = tmp_path / "obs.smp"
        observations = [("WELL1", "01/15/2000", "12:30:45", 100.0)]
        create_smp_file(smp_file, observations)

        result = iwfm.read_obs_smp(str(smp_file))

        if _is_polars(result):
            assert set(result.columns) == {'site_name', 'date', 'time', 'obs_value'}
        else:
            assert set(result.keys()) == {'site_name', 'date', 'time', 'obs_value'}

    def test_value_is_float(self, tmp_path):
        """Test that observation value is returned as float."""
        smp_file = tmp_path / "obs.smp"
        observations = [("WELL1", "01/15/2000", "00:00:00", 123.456)]
        create_smp_file(smp_file, observations)

        result = iwfm.read_obs_smp(str(smp_file))

        val = _col(result, 'obs_value', 0)
        assert isinstance(val, float)
        assert abs(val - 123.456) < 0.001

    def test_date_is_datetime(self, tmp_path):
        """Test that dates are parsed to datetime objects."""
        smp_file = tmp_path / "obs.smp"
        observations = [("WELL1", "03/25/2005", "00:00:00", 100.0)]
        create_smp_file(smp_file, observations)

        result = iwfm.read_obs_smp(str(smp_file))

        dt = _col(result, 'date', 0)
        assert isinstance(dt, datetime)
        assert dt == datetime(2005, 3, 25)

    def test_underscore_replacement(self, tmp_path):
        """Test that underscores are replaced with spaces.

        Names without underscores (like real state well numbers) stay intact.
        """
        smp_file = tmp_path / "obs.smp"
        observations = [("11N19W05Q001S", "01/15/2000", "00:00:00", 100.0)]
        create_smp_file(smp_file, observations)

        result = iwfm.read_obs_smp(str(smp_file))

        assert _col(result, 'site_name', 0) == "11N19W05Q001S"
        assert _col(result, 'date', 0) == datetime(2000, 1, 15)
        assert _col(result, 'time', 0) == "00:00:00"
        assert _col(result, 'obs_value', 0) == 100.0

    def test_sorting_by_name(self, tmp_path):
        """Test that observations are sorted by name first."""
        smp_file = tmp_path / "obs.smp"
        observations = [
            ("WELLC", "01/15/2000", "00:00:00", 300.0),
            ("WELLA", "01/15/2000", "00:00:00", 100.0),
            ("WELLB", "01/15/2000", "00:00:00", 200.0),
        ]
        create_smp_file(smp_file, observations)

        result = iwfm.read_obs_smp(str(smp_file))

        names = _col(result, 'site_name')
        assert names[0] == "WELLA"
        assert names[1] == "WELLB"
        assert names[2] == "WELLC"

    def test_sorting_by_date(self, tmp_path):
        """Test that observations are sorted by date within same name."""
        smp_file = tmp_path / "obs.smp"
        observations = [
            ("WELL1", "03/15/2000", "00:00:00", 300.0),
            ("WELL1", "01/15/2000", "00:00:00", 100.0),
            ("WELL1", "02/15/2000", "00:00:00", 200.0),
        ]
        create_smp_file(smp_file, observations)

        result = iwfm.read_obs_smp(str(smp_file))

        dates = _col(result, 'date')
        assert dates[0] == datetime(2000, 1, 15)
        assert dates[1] == datetime(2000, 2, 15)
        assert dates[2] == datetime(2000, 3, 15)

    def test_sorting_by_time(self, tmp_path):
        """Test that observations are sorted by time within same name and date."""
        smp_file = tmp_path / "obs.smp"
        observations = [
            ("WELL1", "01/15/2000", "12:00:00", 120.0),
            ("WELL1", "01/15/2000", "06:00:00", 106.0),
            ("WELL1", "01/15/2000", "18:00:00", 118.0),
        ]
        create_smp_file(smp_file, observations)

        result = iwfm.read_obs_smp(str(smp_file))

        times = _col(result, 'time')
        assert times[0] == "06:00:00"
        assert times[1] == "12:00:00"
        assert times[2] == "18:00:00"

    def test_integer_values(self, tmp_path):
        """Test that integer values are returned as floats."""
        smp_file = tmp_path / "obs.smp"
        observations = [("WELL1", "01/15/2000", "00:00:00", 100)]
        create_smp_file(smp_file, observations)

        result = iwfm.read_obs_smp(str(smp_file))

        val = _col(result, 'obs_value', 0)
        assert isinstance(val, float)
        assert val == 100.0

    def test_negative_values(self, tmp_path):
        """Test reading negative observation values."""
        smp_file = tmp_path / "obs.smp"
        observations = [("WELL1", "01/15/2000", "00:00:00", -50.25)]
        create_smp_file(smp_file, observations)

        result = iwfm.read_obs_smp(str(smp_file))

        assert _col(result, 'obs_value', 0) == -50.25

    def test_zero_value(self, tmp_path):
        """Test reading zero observation value."""
        smp_file = tmp_path / "obs.smp"
        observations = [("WELL1", "01/15/2000", "00:00:00", 0.0)]
        create_smp_file(smp_file, observations)

        result = iwfm.read_obs_smp(str(smp_file))

        assert _col(result, 'obs_value', 0) == 0.0

    def test_large_value(self, tmp_path):
        """Test reading large observation value."""
        smp_file = tmp_path / "obs.smp"
        observations = [("WELL1", "01/15/2000", "00:00:00", 9999999.99)]
        create_smp_file(smp_file, observations)

        result = iwfm.read_obs_smp(str(smp_file))

        assert abs(_col(result, 'obs_value', 0) - 9999999.99) < 0.01

    def test_small_decimal_value(self, tmp_path):
        """Test reading small decimal observation value."""
        smp_file = tmp_path / "obs.smp"
        observations = [("WELL1", "01/15/2000", "00:00:00", 0.00123)]
        create_smp_file(smp_file, observations)

        result = iwfm.read_obs_smp(str(smp_file))

        assert abs(_col(result, 'obs_value', 0) - 0.00123) < 0.00001

    def test_many_observations(self, tmp_path):
        """Test reading file with many observations."""
        smp_file = tmp_path / "obs.smp"
        # Generate 50 observations with valid dates across different months
        observations = [
            (f"WELL{i:02d}", f"{(i % 12) + 1:02d}/15/{2000 + i // 12}", "00:00:00", float(i * 10))
            for i in range(1, 51)
        ]
        create_smp_file(smp_file, observations)

        result = iwfm.read_obs_smp(str(smp_file))

        assert _nrows(result) == 50

    def test_file_not_found_raises_error(self, tmp_path):
        """Test that nonexistent file raises FileNotFoundError."""
        nonexistent = tmp_path / "nonexistent.smp"

        with pytest.raises(FileNotFoundError):
            iwfm.read_obs_smp(str(nonexistent))

    def test_empty_file(self, tmp_path):
        """Test that empty file returns empty result."""
        smp_file = tmp_path / "empty.smp"
        smp_file.write_text("")

        result = iwfm.read_obs_smp(str(smp_file))

        assert _nrows(result) == 0

    def test_whitespace_handling(self, tmp_path):
        """Test handling of various whitespace."""
        smp_file = tmp_path / "obs.smp"
        content = " WELL1       01/15/2000    00:00:00     100.5  "
        smp_file.write_text(content)

        result = iwfm.read_obs_smp(str(smp_file))

        assert _nrows(result) == 1
        assert _col(result, 'site_name', 0) == "WELL1"
        assert _col(result, 'obs_value', 0) == 100.5


class TestReadObsSmpRealFile:
    """Tests using real PEST smp test data files."""

    def test_with_real_gwobs_file(self):
        """Test with actual gwobs.smp file if available."""
        test_file = os.path.join(
            os.path.dirname(__file__),
            'C2VSimCG-2021',
            'gis',
            'gwobs.smp'
        )

        if not os.path.exists(test_file):
            pytest.skip("Test data file not available")

        result = iwfm.read_obs_smp(test_file)

        # Verify we got a polars DataFrame or dict back
        assert _is_polars(result) or isinstance(result, dict)

        # Should have many observations
        assert _nrows(result) > 0

        # Check column types
        assert isinstance(_col(result, 'site_name', 0), str)
        assert isinstance(_col(result, 'date', 0), datetime)
        assert isinstance(_col(result, 'time', 0), str)
        assert isinstance(_col(result, 'obs_value', 0), float)

    def test_real_file_sorting(self):
        """Test that real file is properly sorted."""
        test_file = os.path.join(
            os.path.dirname(__file__),
            'C2VSimCG-2021',
            'gis',
            'gwobs.smp'
        )

        if not os.path.exists(test_file):
            pytest.skip("Test data file not available")

        result = iwfm.read_obs_smp(test_file)

        # Verify sorting: each row should be <= next row
        # by (site_name, date, time) tuple comparison
        names = _col(result, 'site_name')
        dates = _col(result, 'date')
        times = _col(result, 'time')

        for i in range(len(names) - 1):
            key_current = (names[i], dates[i], times[i])
            key_next = (names[i+1], dates[i+1], times[i+1])
            assert key_current <= key_next, \
                f"Sorting error at index {i}: {key_current} > {key_next}"

    def test_real_file_known_values(self):
        """Test known values from the real file."""
        test_file = os.path.join(
            os.path.dirname(__file__),
            'C2VSimCG-2021',
            'gis',
            'gwobs.smp'
        )

        if not os.path.exists(test_file):
            pytest.skip("Test data file not available")

        result = iwfm.read_obs_smp(test_file)

        # Find observation for 11N19W05Q001S on 01/28/1987
        # From file: value should be 108.53
        names = _col(result, 'site_name')
        dates = _col(result, 'date')
        values = _col(result, 'obs_value')

        found = False
        target_date = datetime(1987, 1, 28)
        for i in range(len(names)):
            if names[i] == "11N19W05Q001S" and dates[i] == target_date:
                assert abs(values[i] - 108.53) < 0.01
                found = True
                break

        assert found, "Expected observation 11N19W05Q001S on 01/28/1987 not found"

    def test_real_file_all_values_are_floats(self):
        """Test that all values in real file are floats."""
        test_file = os.path.join(
            os.path.dirname(__file__),
            'C2VSimCG-2021',
            'gis',
            'gwobs.smp'
        )

        if not os.path.exists(test_file):
            pytest.skip("Test data file not available")

        result = iwfm.read_obs_smp(test_file)

        values = _col(result, 'obs_value')
        for i, val in enumerate(values):
            assert isinstance(val, float), \
                f"Observation {i} value is not float: {type(val)}"
