# test_write_results.py
# Unit tests for write_results.py - Write simulated and observed values to file
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

import pytest
import os


class TestWriteResults:
    """Tests for write_results function"""

    def test_basic_functionality(self, tmp_path):
        """Test basic functionality with simple data."""
        from iwfm.write_results import write_results

        name = str(tmp_path / 'test_well')
        date = [1, 2, 3]  # Day indices from start_date
        meas = [100.5, 101.5, 102.5]
        sim = [100.0, 101.0, 102.0]
        start_date = '01/01/2020'

        write_results(name, date, meas, sim, start_date)

        output_file = str(tmp_path / 'test_well_obs.out')
        assert os.path.exists(output_file)

    def test_output_filename(self, tmp_path):
        """Test that output filename has _obs.out suffix."""
        from iwfm.write_results import write_results

        name = str(tmp_path / 'my_observation_well')
        date = [1]
        meas = [100.0]
        sim = [100.0]
        start_date = '01/01/2020'

        write_results(name, date, meas, sim, start_date)

        expected_file = str(tmp_path / 'my_observation_well_obs.out')
        assert os.path.exists(expected_file)

    def test_header_format(self, tmp_path):
        """Test that output file has correct header lines."""
        from iwfm.write_results import write_results

        name = str(tmp_path / 'WELL_001')
        date = [1]
        meas = [100.0]
        sim = [100.0]
        start_date = '01/01/2020'

        write_results(name, date, meas, sim, start_date)

        output_file = str(tmp_path / 'WELL_001_obs.out')
        with open(output_file, 'r') as f:
            lines = f.readlines()

        # First line should be comment with well name
        assert lines[0].startswith('#')
        assert 'WELL_001' in lines[0]
        
        # Second line should be column headers
        assert 'Date' in lines[1]
        assert 'Observed' in lines[1]
        assert 'Modeled' in lines[1]

    def test_data_rows(self, tmp_path):
        """Test that data rows contain date, observed, and modeled values."""
        from iwfm.write_results import write_results

        name = str(tmp_path / 'test_well')
        date = [1, 2, 3]
        meas = [100.5, 101.5, 102.5]
        sim = [100.0, 101.0, 102.0]
        start_date = '01/01/2020'

        write_results(name, date, meas, sim, start_date)

        output_file = str(tmp_path / 'test_well_obs.out')
        with open(output_file, 'r') as f:
            lines = f.readlines()

        # Skip header lines (2), check data lines
        assert len(lines) == 5  # 2 headers + 3 data rows
        
        # Check that values are present (exact format depends on date_index)
        content = ''.join(lines[2:])
        assert '100.5' in content
        assert '101.5' in content
        assert '102.5' in content
        assert '100.0' in content or '100' in content

    def test_tab_separated(self, tmp_path):
        """Test that output uses tab separation."""
        from iwfm.write_results import write_results

        name = str(tmp_path / 'test_well')
        date = [1]
        meas = [100.0]
        sim = [99.0]
        start_date = '01/01/2020'

        write_results(name, date, meas, sim, start_date)

        output_file = str(tmp_path / 'test_well_obs.out')
        with open(output_file, 'r') as f:
            lines = f.readlines()

        # Data line should be tab-separated
        data_line = lines[2]
        assert '\t' in data_line

    def test_multiple_observations(self, tmp_path):
        """Test with many observations."""
        from iwfm.write_results import write_results

        name = str(tmp_path / 'test_well')
        num_obs = 100
        date = list(range(1, num_obs + 1))
        meas = [float(i) for i in range(num_obs)]
        sim = [float(i) + 0.1 for i in range(num_obs)]
        start_date = '01/01/2020'

        write_results(name, date, meas, sim, start_date)

        output_file = str(tmp_path / 'test_well_obs.out')
        with open(output_file, 'r') as f:
            lines = f.readlines()

        # 2 header lines + 100 data lines
        assert len(lines) == 102

    def test_single_observation(self, tmp_path):
        """Test with single observation."""
        from iwfm.write_results import write_results

        name = str(tmp_path / 'test_well')
        date = [365]  # Day 365 from start
        meas = [150.0]
        sim = [149.5]
        start_date = '01/01/2019'

        write_results(name, date, meas, sim, start_date)

        output_file = str(tmp_path / 'test_well_obs.out')
        with open(output_file, 'r') as f:
            lines = f.readlines()

        assert len(lines) == 3  # 2 headers + 1 data

    def test_negative_values(self, tmp_path):
        """Test with negative values (e.g., depth to water)."""
        from iwfm.write_results import write_results

        name = str(tmp_path / 'test_well')
        date = [1, 2]
        meas = [-50.5, -55.0]  # Depth to water (negative)
        sim = [-51.0, -54.5]
        start_date = '01/01/2020'

        write_results(name, date, meas, sim, start_date)

        output_file = str(tmp_path / 'test_well_obs.out')
        with open(output_file, 'r') as f:
            content = f.read()

        assert '-50.5' in content
        assert '-55' in content

    def test_large_values(self, tmp_path):
        """Test with large elevation values."""
        from iwfm.write_results import write_results

        name = str(tmp_path / 'test_well')
        date = [1]
        meas = [1500.123]
        sim = [1499.876]
        start_date = '01/01/2020'

        write_results(name, date, meas, sim, start_date)

        output_file = str(tmp_path / 'test_well_obs.out')
        with open(output_file, 'r') as f:
            content = f.read()

        assert '1500.123' in content
        assert '1499.876' in content

    def test_well_name_in_header(self, tmp_path):
        """Test that well name appears in file header."""
        from iwfm.write_results import write_results

        name = str(tmp_path / 'S_380313N1219426W001')
        date = [1]
        meas = [100.0]
        sim = [100.0]
        start_date = '01/01/2020'

        write_results(name, date, meas, sim, start_date)

        output_file = str(tmp_path / 'S_380313N1219426W001_obs.out')
        with open(output_file, 'r') as f:
            first_line = f.readline()

        assert 'S_380313N1219426W001' in first_line

    def test_date_index_conversion(self, tmp_path):
        """Test that date indices are converted to dates."""
        from iwfm.write_results import write_results

        name = str(tmp_path / 'test_well')
        # Day 1 from 01/01/2020 should be 01/02/2020
        date = [1]
        meas = [100.0]
        sim = [100.0]
        start_date = '01/01/2020'

        write_results(name, date, meas, sim, start_date)

        output_file = str(tmp_path / 'test_well_obs.out')
        with open(output_file, 'r') as f:
            lines = f.readlines()

        # The date_index function should convert index to date string
        # Exact format depends on date_index implementation
        data_line = lines[2]
        # Should contain some date representation
        assert len(data_line.split('\t')) >= 3

    def test_return_value(self, tmp_path):
        """Test that function returns None."""
        from iwfm.write_results import write_results

        name = str(tmp_path / 'test_well')
        date = [1]
        meas = [100.0]
        sim = [100.0]
        start_date = '01/01/2020'

        result = write_results(name, date, meas, sim, start_date)

        assert result is None

    def test_uses_date_index_function(self):
        """Test that write_results imports and uses date_index function."""
        # This test verifies the dependency on iwfm.date_index
        import iwfm
        
        # date_index should be available
        assert hasattr(iwfm, 'date_index')
        
        # Basic test of date_index functionality
        result = iwfm.date_index(1, '01/01/2020')
        assert result is not None


class TestWriteResultsEdgeCases:
    """Edge case tests for write_results function"""

    def test_empty_lists(self, tmp_path):
        """Test with empty data lists."""
        from iwfm.write_results import write_results

        name = str(tmp_path / 'test_well')
        date = []
        meas = []
        sim = []
        start_date = '01/01/2020'

        write_results(name, date, meas, sim, start_date)

        output_file = str(tmp_path / 'test_well_obs.out')
        with open(output_file, 'r') as f:
            lines = f.readlines()

        # Should have only header lines, no data
        assert len(lines) == 2

    def test_float_date_indices(self, tmp_path):
        """Test with float date indices (converted to int)."""
        from iwfm.write_results import write_results

        name = str(tmp_path / 'test_well')
        date = [1.0, 2.5, 3.9]  # Will be converted to int
        meas = [100.0, 101.0, 102.0]
        sim = [100.0, 101.0, 102.0]
        start_date = '01/01/2020'

        write_results(name, date, meas, sim, start_date)

        output_file = str(tmp_path / 'test_well_obs.out')
        assert os.path.exists(output_file)

    def test_special_characters_in_name(self, tmp_path):
        """Test with special characters in well name."""
        from iwfm.write_results import write_results

        # Well name with underscores and numbers (common pattern)
        name = str(tmp_path / 'WELL_123_ABC')
        date = [1]
        meas = [100.0]
        sim = [100.0]
        start_date = '01/01/2020'

        write_results(name, date, meas, sim, start_date)

        output_file = str(tmp_path / 'WELL_123_ABC_obs.out')
        assert os.path.exists(output_file)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
