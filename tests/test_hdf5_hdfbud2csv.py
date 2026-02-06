# test_hdf5_hdfbud2csv.py
# Tests for hdf5/hdfbud2csv.py - Convert HDF Budget to CSV
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
import pandas as pd
from datetime import datetime


class TestHdfbud2csvImports:
    """Tests for hdfbud2csv imports."""

    def test_import_from_hdf5(self):
        """Test import from iwfm.hdf5."""
        from iwfm.hdf5 import hdfbud2csv
        assert callable(hdfbud2csv)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.hdf5.hdfbud2csv import hdfbud2csv
        assert callable(hdfbud2csv)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.hdf5.hdfbud2csv import hdfbud2csv

        assert hdfbud2csv.__doc__ is not None
        assert 'csv' in hdfbud2csv.__doc__.lower()


class TestHdfbud2csvSignature:
    """Tests for hdfbud2csv function signature."""

    def test_function_signature(self):
        """Test that hdfbud2csv has correct function signature."""
        from iwfm.hdf5.hdfbud2csv import hdfbud2csv
        import inspect

        sig = inspect.signature(hdfbud2csv)
        params = list(sig.parameters.keys())

        assert 'bud_file' in params
        assert 'outfile' in params
        assert 'write_header' in params
        assert 'verbose' in params

    def test_default_write_header(self):
        """Test that write_header defaults to True."""
        from iwfm.hdf5.hdfbud2csv import hdfbud2csv
        import inspect

        sig = inspect.signature(hdfbud2csv)
        assert sig.parameters['write_header'].default == True

    def test_default_verbose(self):
        """Test that verbose defaults to False."""
        from iwfm.hdf5.hdfbud2csv import hdfbud2csv
        import inspect

        sig = inspect.signature(hdfbud2csv)
        assert sig.parameters['verbose'].default == False


class TestAdjustHeaders:
    """Tests for adjust_headers helper function."""

    def test_import_adjust_headers(self):
        """Test that adjust_headers can be imported."""
        from iwfm.hdf5.hdfbud2csv import adjust_headers
        assert callable(adjust_headers)

    def test_replaces_time(self):
        """Test that Time is replaced with Timestep."""
        from iwfm.hdf5.hdfbud2csv import adjust_headers

        headers = ['Time', 'Value']
        result = adjust_headers(headers)
        assert 'Timestep' in result
        assert 'Time' not in result

    def test_replaces_area(self):
        """Test that Area (SQ FT) is replaced."""
        from iwfm.hdf5.hdfbud2csv import adjust_headers

        headers = ['Area (SQ FT)']
        result = adjust_headers(headers)
        assert 'Area_ac' in result

    def test_replaces_ag_headers(self):
        """Test that agricultural headers are replaced."""
        from iwfm.hdf5.hdfbud2csv import adjust_headers

        headers = ['Ag. Pumping', 'Ag. Deliveries']
        result = adjust_headers(headers)
        assert 'Ag_Pumping' in result
        assert 'Ag_Deliveries' in result

    def test_replaces_urban_headers(self):
        """Test that urban headers are replaced."""
        from iwfm.hdf5.hdfbud2csv import adjust_headers

        headers = ['Urban Pumping', 'Urban Deliveries']
        result = adjust_headers(headers)
        assert 'Ur_Pumping' in result
        assert 'Ur_Deliveries' in result

    def test_replaces_groundwater_headers(self):
        """Test that groundwater headers are replaced."""
        from iwfm.hdf5.hdfbud2csv import adjust_headers

        headers = ['Beginning Storage (+)', 'Deep Percolation (+)']
        result = adjust_headers(headers)
        assert 'BegStor' in result
        assert 'DeepPerc' in result

    def test_replaces_stream_headers(self):
        """Test that stream headers are replaced."""
        from iwfm.hdf5.hdfbud2csv import adjust_headers

        headers = ['Upstream Inflow (+)', 'Downstream Outflow (-)']
        result = adjust_headers(headers)
        assert 'UpstreamIn' in result
        assert 'DownstreamOut' in result


class TestProcessBudgetData:
    """Tests for process_budget_data helper function."""

    def test_import_process_budget_data(self):
        """Test that process_budget_data can be imported."""
        from iwfm.hdf5.hdfbud2csv import process_budget_data
        assert callable(process_budget_data)

    def test_writes_header_when_requested(self, tmp_path):
        """Test that header is written when write_header=True."""
        from iwfm.hdf5.hdfbud2csv import process_budget_data

        outfile = tmp_path / "test.csv"

        # Create mock data
        loc_names = ['Location1']
        column_headers = [['Time', 'Value1']]

        # Create mock dataframe
        mock_df = pd.DataFrame({
            'Time': [datetime(2000, 1, 1)],
            'Value1': [100.0]
        })
        loc_values = [mock_df]
        titles = [('Type', 'GROUNDWATER Budget', 'Title')]

        with open(outfile, 'w') as f:
            process_budget_data(f, loc_names, column_headers, loc_values, titles,
                              write_header=True)

        content = outfile.read_text()
        assert 'Subregion' in content

    def test_writes_data_rows(self, tmp_path):
        """Test that data rows are written."""
        from iwfm.hdf5.hdfbud2csv import process_budget_data

        outfile = tmp_path / "test.csv"

        loc_names = ['TestLocation']
        column_headers = [['Time', 'Value']]

        mock_df = pd.DataFrame({
            'Time': [datetime(2000, 1, 15)],
            'Value': [123.45]
        })
        loc_values = [mock_df]
        titles = [('Type', 'GROUNDWATER Budget', 'Title')]

        with open(outfile, 'w') as f:
            process_budget_data(f, loc_names, column_headers, loc_values, titles)

        content = outfile.read_text()
        assert 'TestLocation' in content
        assert '01/15/2000' in content


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
