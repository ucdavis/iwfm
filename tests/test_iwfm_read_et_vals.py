#!/usr/bin/env python
# test_iwfm_read_et_vals.py
# Unit tests for iwfm_read_et_vals.py
# Copyright (C) 2020-2026 University of California
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
import tempfile
import os


def create_et_file(nevap, factet, nspet, nfqet, dssfl, et_data):
    """Create IWFM Evapotranspiration file for testing.

    Parameters
    ----------
    nevap : int
        Number of ET columns
    factet : float
        Conversion factor for ET rate
    nspet : int
        Number of timesteps to update ET data
    nfqet : int
        Repetition frequency of ET data
    dssfl : str
        DSS file name (or empty string)
    et_data : list of tuples
        Each tuple: (time_string, [et_values...])
        et_values should have nevap-1 floats (first column is time)

    Returns
    -------
    str
        File contents
    """
    content = "C IWFM Evapotranspiration Data File\n"
    content += "C\n"
    content += f"          {nevap}                                        / NEVAP\n"
    content += f"          {factet}                                  / FACTET (in/mon --> ft/mon)\n"
    content += f"          {nspet}                                          / NSPET\n"
    content += f"          {nfqet}                                         / NFQET\n"
    content += f"          {dssfl}                                     / DSSFL\n"
    content += "C\n"
    content += "C   ITEV ;   Time\n"
    content += "C   AEVAP;   Evapotranspiration rate; [L/T]\n"
    content += "C\n"

    # Add ET data
    for time_str, et_values in et_data:
        content += f"{time_str}"
        for val in et_values:
            content += f"\t{val}"
        content += "\n"

    return content


class TestIwfmReadEtVals:
    """Tests for iwfm_read_et_vals function"""

    def test_single_timestep_single_column(self):
        """Test reading single timestep with one ET column"""
        et_data = [
            ("09/30/2020_24:00", [1.234])
        ]

        content = create_et_file(2, 0.0833333, 1, 12, "", et_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_et_vals import iwfm_read_et_vals

            params = iwfm_read_et_vals(temp_file, verbose=False)

            # Verify data
            assert len(params) == 1
            assert params[0][0] == "09/30/2020_24:00"
            assert params[0][1] == 1.234

        finally:
            os.unlink(temp_file)

    def test_single_timestep_multiple_columns(self):
        """Test reading single timestep with multiple ET columns"""
        et_data = [
            ("09/30/2020_24:00", [1.234, 2.345, 3.456, 4.567])
        ]

        content = create_et_file(5, 0.0833333, 1, 12, "", et_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_et_vals import iwfm_read_et_vals

            params = iwfm_read_et_vals(temp_file, verbose=False)

            # Verify data
            assert len(params) == 1
            assert params[0][0] == "09/30/2020_24:00"
            assert params[0][1] == 1.234
            assert params[0][2] == 2.345
            assert params[0][3] == 3.456
            assert params[0][4] == 4.567

        finally:
            os.unlink(temp_file)

    def test_multiple_timesteps(self):
        """Test reading multiple timesteps"""
        et_data = [
            ("09/30/2020_24:00", [1.234, 2.345, 3.456]),
            ("10/31/2020_24:00", [1.111, 2.222, 3.333]),
            ("11/30/2020_24:00", [4.444, 5.555, 6.666])
        ]

        content = create_et_file(4, 0.0833333, 1, 12, "", et_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_et_vals import iwfm_read_et_vals

            params = iwfm_read_et_vals(temp_file, verbose=False)

            # Verify number of timesteps
            assert len(params) == 3

            # Verify first timestep
            assert params[0][0] == "09/30/2020_24:00"
            assert params[0][1] == 1.234

            # Verify second timestep
            assert params[1][0] == "10/31/2020_24:00"
            assert params[1][2] == 2.222

            # Verify third timestep
            assert params[2][0] == "11/30/2020_24:00"
            assert params[2][3] == 6.666

        finally:
            os.unlink(temp_file)

    def test_conversion_factor(self):
        """Test different conversion factors"""
        et_data = [
            ("09/30/2020_24:00", [1.0, 2.0])
        ]

        # Test with different conversion factor
        content = create_et_file(3, 1.0, 1, 12, "", et_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_et_vals import iwfm_read_et_vals

            params = iwfm_read_et_vals(temp_file, verbose=False)

            # Verify data is read correctly
            assert len(params) == 1
            assert params[0][1] == 1.0
            assert params[0][2] == 2.0

        finally:
            os.unlink(temp_file)

    def test_dss_filename(self):
        """Test with DSS filename specified"""
        et_data = [
            ("09/30/2020_24:00", [1.5, 2.5])
        ]

        content = create_et_file(3, 0.0833333, 1, 0, "ET_Data.dss", et_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_et_vals import iwfm_read_et_vals

            params = iwfm_read_et_vals(temp_file, verbose=False)

            # Should still read data even with DSS file specified
            assert len(params) == 1

        finally:
            os.unlink(temp_file)

    def test_many_columns(self):
        """Test reading with many ET columns (like real C2VSimCG with 735)"""
        # Create data with 20 columns for testing
        et_values = [float(i) * 0.1 for i in range(1, 20)]
        et_data = [
            ("09/30/2020_24:00", et_values)
        ]

        content = create_et_file(20, 0.0833333, 1, 12, "", et_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_et_vals import iwfm_read_et_vals

            params = iwfm_read_et_vals(temp_file, verbose=False)

            # Verify all columns read
            assert len(params) == 1
            assert len(params[0]) == 20  # time + 19 ET values
            assert params[0][1] == pytest.approx(0.1, abs=0.001)
            assert params[0][19] == pytest.approx(1.9, abs=0.001)

        finally:
            os.unlink(temp_file)

    def test_zero_et_values(self):
        """Test handling of zero ET values"""
        et_data = [
            ("09/30/2020_24:00", [0.0, 0.0, 0.0])
        ]

        content = create_et_file(4, 0.0833333, 1, 12, "", et_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_et_vals import iwfm_read_et_vals

            params = iwfm_read_et_vals(temp_file, verbose=False)

            # Verify zeros are preserved
            assert params[0][1] == 0.0
            assert params[0][2] == 0.0
            assert params[0][3] == 0.0

        finally:
            os.unlink(temp_file)

    def test_comment_lines_skipped(self):
        """Test that comment lines are properly skipped"""
        content = "C IWFM Evapotranspiration Data File\n"
        content += "c This is a comment\n"
        content += "* Another comment\n"
        content += "# Hash comment\n"
        content += "          3                                        / NEVAP\n"
        content += "C More comments\n"
        content += "          0.0833333                                  / FACTET\n"
        content += "          1                                          / NSPET\n"
        content += "C Comment line\n"
        content += "          12                                         / NFQET\n"
        content += "                                                     / DSSFL\n"
        content += "C\n"
        content += "09/30/2020_24:00\t1.234\t2.345\n"
        content += "10/31/2020_24:00\t3.456\t4.567\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_et_vals import iwfm_read_et_vals

            params = iwfm_read_et_vals(temp_file, verbose=False)

            # Should read correctly despite comment lines
            assert len(params) == 2
            assert params[0][0] == "09/30/2020_24:00"
            assert params[1][0] == "10/31/2020_24:00"

        finally:
            os.unlink(temp_file)

    def test_monthly_data(self):
        """Test reading monthly data (typical use case)"""
        # Create 12 months of data
        months = ["09/30/2020_24:00", "10/31/2020_24:00", "11/30/2020_24:00",
                  "12/31/2020_24:00", "01/31/2021_24:00", "02/28/2021_24:00",
                  "03/31/2021_24:00", "04/30/2021_24:00", "05/31/2021_24:00",
                  "06/30/2021_24:00", "07/31/2021_24:00", "08/31/2021_24:00"]

        et_data = []
        for i, month in enumerate(months):
            et_values = [1.0 + i * 0.1, 2.0 + i * 0.1, 3.0 + i * 0.1]
            et_data.append((month, et_values))

        content = create_et_file(4, 0.0833333, 1, 12, "", et_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_et_vals import iwfm_read_et_vals

            params = iwfm_read_et_vals(temp_file, verbose=False)

            # Verify 12 months of data
            assert len(params) == 12

            # Check first month
            assert params[0][0] == "09/30/2020_24:00"
            assert params[0][1] == pytest.approx(1.0, abs=0.001)

            # Check last month
            assert params[11][0] == "08/31/2021_24:00"
            assert params[11][1] == pytest.approx(2.1, abs=0.001)

        finally:
            os.unlink(temp_file)

    def test_real_file_format(self):
        """Test with format matching real IWFM C2VSimCG file"""
        # Simulate C2VSimCG format with multiple ET values per row
        et_data = [
            ("09/30/1922_24:00", [0.106, 0.112, 1.273, 1.273, 0.112, 0.122, 0.217, 0.110]),
            ("09/30/1923_24:00", [0.096, 0.101, 1.304, 1.304, 0.106, 0.113, 0.207, 0.105]),
            ("09/30/1924_24:00", [0.093, 0.100, 1.435, 1.435, 0.102, 0.109, 0.198, 0.100])
        ]

        content = create_et_file(9, 0.0833333, 1, 12, "", et_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_et_vals import iwfm_read_et_vals

            params = iwfm_read_et_vals(temp_file, verbose=False)

            # Verify data structure
            assert len(params) == 3

            # Verify first row
            assert params[0][0] == "09/30/1922_24:00"
            assert params[0][1] == pytest.approx(0.106, abs=0.001)
            assert params[0][8] == pytest.approx(0.110, abs=0.001)

            # Verify second row
            assert params[1][0] == "09/30/1923_24:00"
            assert params[1][1] == pytest.approx(0.096, abs=0.001)

            # Verify third row
            assert params[2][0] == "09/30/1924_24:00"
            assert params[2][1] == pytest.approx(0.093, abs=0.001)

        finally:
            os.unlink(temp_file)

    def test_large_dataset(self):
        """Test reading large dataset (many timesteps and columns)"""
        # Create 100 timesteps with 10 columns
        et_data = []
        for i in range(100):
            year = 1920 + i // 12
            month = (i % 12) + 1
            time_str = f"{month:02d}/28/{year}_24:00"
            et_values = [float(j + i * 0.01) for j in range(1, 10)]
            et_data.append((time_str, et_values))

        content = create_et_file(10, 0.0833333, 1, 12, "", et_data)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_et_vals import iwfm_read_et_vals

            params = iwfm_read_et_vals(temp_file, verbose=False)

            # Verify all timesteps read
            assert len(params) == 100

            # Spot check first and last
            assert params[0][0] == "01/28/1920_24:00"
            assert params[99][0] == "04/28/1928_24:00"

        finally:
            os.unlink(temp_file)
