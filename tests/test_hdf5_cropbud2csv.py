# test_hdf5_cropbud2csv.py
# Tests for hdf5/cropbud2csv.py - Convert crop budget HDF to CSV
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


class TestCropbud2csvImports:
    """Tests for cropbud2csv imports."""

    def test_import_from_hdf5(self):
        """Test import from iwfm.hdf5."""
        from iwfm.hdf5 import cropbud2csv
        assert callable(cropbud2csv)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.hdf5.cropbud2csv import cropbud2csv
        assert callable(cropbud2csv)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.hdf5.cropbud2csv import cropbud2csv

        assert cropbud2csv.__doc__ is not None
        assert 'crop' in cropbud2csv.__doc__.lower()


class TestCropbud2csvSignature:
    """Tests for cropbud2csv function signature."""

    def test_function_signature(self):
        """Test that cropbud2csv has correct function signature."""
        from iwfm.hdf5.cropbud2csv import cropbud2csv
        import inspect

        sig = inspect.signature(cropbud2csv)
        params = list(sig.parameters.keys())

        assert 'bud_file_ag' in params
        assert 'bud_file_pond' in params
        assert 'outfile' in params
        assert 'write_header' in params
        assert 'verbose' in params

    def test_default_write_header(self):
        """Test that write_header defaults to True."""
        from iwfm.hdf5.cropbud2csv import cropbud2csv
        import inspect

        sig = inspect.signature(cropbud2csv)
        assert sig.parameters['write_header'].default == True

    def test_default_verbose(self):
        """Test that verbose defaults to False."""
        from iwfm.hdf5.cropbud2csv import cropbud2csv
        import inspect

        sig = inspect.signature(cropbud2csv)
        assert sig.parameters['verbose'].default == False


class TestCropbud2csvAdjustHeaders:
    """Tests for adjust_headers helper function in cropbud2csv."""

    def test_import_adjust_headers(self):
        """Test that adjust_headers can be imported."""
        from iwfm.hdf5.cropbud2csv import adjust_headers
        assert callable(adjust_headers)

    def test_replaces_time(self):
        """Test that Time is replaced with Timestep."""
        from iwfm.hdf5.cropbud2csv import adjust_headers

        headers = ['Time', 'Value']
        result = adjust_headers(headers)
        assert 'Timestep' in result

    def test_replaces_area(self):
        """Test that Area (SQ FT) is replaced."""
        from iwfm.hdf5.cropbud2csv import adjust_headers

        headers = ['Area (SQ FT)']
        result = adjust_headers(headers)
        assert 'Area_ac' in result

    def test_replaces_land_water_use_headers(self):
        """Test that land and water use headers are replaced."""
        from iwfm.hdf5.cropbud2csv import adjust_headers

        headers = ['Potential CUAW', 'Supply Requirement', 'ETAW']
        result = adjust_headers(headers)
        assert 'Pot_CUAW' in result
        assert 'Ag_Supp_Req' in result
        assert 'ETaw' in result

    def test_replaces_root_zone_headers(self):
        """Test that root zone headers are replaced."""
        from iwfm.hdf5.cropbud2csv import adjust_headers

        headers = ['Potential ET', 'Beginning Storage (+)', 'Actual ET (-)']
        result = adjust_headers(headers)
        assert 'ETpot' in result
        assert 'BegStor' in result
        assert 'ETa' in result


class TestCropbud2csvProcessBudgetData:
    """Tests for process_budget_data helper function in cropbud2csv."""

    def test_import_process_budget_data(self):
        """Test that process_budget_data can be imported."""
        from iwfm.hdf5.cropbud2csv import process_budget_data
        assert callable(process_budget_data)

    def test_writes_header_with_crop_column(self, tmp_path):
        """Test that header includes Crop column."""
        from iwfm.hdf5.cropbud2csv import process_budget_data

        outfile = tmp_path / "test.csv"

        loc_names = ['Region1_Alfalfa']
        column_headers = [['Time', 'Value1']]

        mock_df = pd.DataFrame({
            'Time': [datetime(2000, 1, 1)],
            'Value1': [100.0]
        })
        loc_values = [mock_df]

        with open(outfile, 'w') as f:
            process_budget_data(f, loc_names, column_headers, loc_values,
                              write_header=True)

        content = outfile.read_text()
        assert 'Subregion' in content
        assert 'Crop' in content

    def test_splits_location_name_into_subregion_and_crop(self, tmp_path):
        """Test that location name is split into subregion and crop."""
        from iwfm.hdf5.cropbud2csv import process_budget_data

        outfile = tmp_path / "test.csv"

        # Location name format: "SubregionName_CropCode"
        loc_names = ['Sacramento Valley_AlfaAlfaHay']
        column_headers = [['Time', 'Value']]

        mock_df = pd.DataFrame({
            'Time': [datetime(2000, 1, 15)],
            'Value': [123.45]
        })
        loc_values = [mock_df]

        with open(outfile, 'w') as f:
            process_budget_data(f, loc_names, column_headers, loc_values)

        content = outfile.read_text()
        # Should contain the subregion and crop as separate values
        assert 'Sacramento Valley' in content
        assert 'AlfaAlfaHay' in content


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
