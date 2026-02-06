# test_headall2surfer.py
# Unit tests for the headall2surfer function in the iwfm package
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

"""
Tests for headall2surfer() function which writes IWFM Headall.out data
to surfer-format files (.sfr) for specified time steps.
"""

import pytest
import os
import tempfile
import glob

# Import directly from module since it may not be exported in __init__.py
from iwfm.headall2surfer import headall2surfer

# Path to the example C2VSimCG files
EXAMPLE_HEADALL_FILE = os.path.join(
    os.path.dirname(__file__),
    'C2VSimCG-2021',
    'Results',
    'C2VSimCG_GW_HeadAll.out'
)

EXAMPLE_PRE_FILE = os.path.join(
    os.path.dirname(__file__),
    'C2VSimCG-2021',
    'Preprocessor',
    'C2VSimCG_Preprocessor.in'
)

# Check if the example files exist for tests that require them
EXAMPLE_FILES_EXIST = (
    os.path.exists(EXAMPLE_HEADALL_FILE) and
    os.path.exists(EXAMPLE_PRE_FILE)
)


class TestHeadall2SurferFunctionExists:
    """Test that the headall2surfer function exists and is callable."""

    def test_headall2surfer_exists(self):
        """Test that headall2surfer function exists and is callable."""
        assert headall2surfer is not None
        assert callable(headall2surfer)

    def test_function_has_docstring(self):
        """Test that headall2surfer has a docstring."""
        assert headall2surfer.__doc__ is not None
        assert len(headall2surfer.__doc__) > 0

    def test_function_signature(self):
        """Test that headall2surfer has expected parameters."""
        import inspect
        sig = inspect.signature(headall2surfer)
        params = list(sig.parameters.keys())
        assert 'node_coords' in params
        assert 'data' in params
        assert 'dates' in params
        assert 'out_dates' in params
        assert 'output_base' in params

    def test_function_has_default_parameters(self):
        """Test that headall2surfer has expected default parameters."""
        import inspect
        sig = inspect.signature(headall2surfer)
        params = sig.parameters
        # Check defaults for optional parameters
        assert params['verbose'].default == False


@pytest.mark.skipif(not EXAMPLE_FILES_EXIST, reason="Example files not found")
class TestHeadall2SurferOutputFiles:
    """Test that headall2surfer creates output files."""

    def test_creates_surfer_file(self):
        """Test that headall2surfer creates surfer output file."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads')

            # Read headall data
            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)

            # Get node coordinates
            pre_path, _ = os.path.split(EXAMPLE_PRE_FILE)
            pre_dict, _ = iwfm.iwfm_read_preproc(EXAMPLE_PRE_FILE)
            node_file = os.path.join(pre_path, pre_dict['node_file'])
            node_coords, node_list, factor = iwfm.iwfm_read_nodes(node_file)

            # Use first date
            out_dates = [dates[0]]

            count = headall2surfer(node_coords, data, dates, out_dates, output_base)

            # Check that surfer file was created
            sfr_files = glob.glob(os.path.join(temp_dir, '*.sfr'))
            assert len(sfr_files) == 1
            assert count == 1

    def test_creates_multiple_surfer_files(self):
        """Test that headall2surfer creates multiple surfer files for multiple dates."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads')

            # Read headall data
            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)

            # Get node coordinates
            pre_path, _ = os.path.split(EXAMPLE_PRE_FILE)
            pre_dict, _ = iwfm.iwfm_read_preproc(EXAMPLE_PRE_FILE)
            node_file = os.path.join(pre_path, pre_dict['node_file'])
            node_coords, node_list, factor = iwfm.iwfm_read_nodes(node_file)

            # Use first 3 dates
            out_dates = dates[:3]

            count = headall2surfer(node_coords, data, dates, out_dates, output_base)

            # Check that 3 surfer files were created
            sfr_files = glob.glob(os.path.join(temp_dir, '*.sfr'))
            assert len(sfr_files) == 3
            assert count == 3

    def test_filename_contains_date(self):
        """Test that output filename contains the date."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads')

            # Read headall data
            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)

            # Get node coordinates
            pre_path, _ = os.path.split(EXAMPLE_PRE_FILE)
            pre_dict, _ = iwfm.iwfm_read_preproc(EXAMPLE_PRE_FILE)
            node_file = os.path.join(pre_path, pre_dict['node_file'])
            node_coords, node_list, factor = iwfm.iwfm_read_nodes(node_file)

            # Use first date
            out_date = dates[0]
            out_dates = [out_date]
            date_text = out_date.replace('/', '_')

            count = headall2surfer(node_coords, data, dates, out_dates, output_base)

            # Check that filename contains date
            expected_file = f'{output_base}_{date_text}.sfr'
            assert os.path.exists(expected_file)


@pytest.mark.skipif(not EXAMPLE_FILES_EXIST, reason="Example files not found")
class TestHeadall2SurferOutputContent:
    """Test the content of headall2surfer output files."""

    def test_output_file_not_empty(self):
        """Test that output file is not empty."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads')

            # Read headall data
            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)

            # Get node coordinates
            pre_path, _ = os.path.split(EXAMPLE_PRE_FILE)
            pre_dict, _ = iwfm.iwfm_read_preproc(EXAMPLE_PRE_FILE)
            node_file = os.path.join(pre_path, pre_dict['node_file'])
            node_coords, node_list, factor = iwfm.iwfm_read_nodes(node_file)

            out_dates = [dates[0]]
            headall2surfer(node_coords, data, dates, out_dates, output_base)

            sfr_files = glob.glob(os.path.join(temp_dir, '*.sfr'))
            for sfr_file in sfr_files:
                assert os.path.getsize(sfr_file) > 0, f"Empty file: {sfr_file}"

    def test_output_file_has_header(self):
        """Test that output file has header row."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads')

            # Read headall data
            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)

            # Get node coordinates
            pre_path, _ = os.path.split(EXAMPLE_PRE_FILE)
            pre_dict, _ = iwfm.iwfm_read_preproc(EXAMPLE_PRE_FILE)
            node_file = os.path.join(pre_path, pre_dict['node_file'])
            node_coords, node_list, factor = iwfm.iwfm_read_nodes(node_file)

            out_dates = [dates[0]]
            headall2surfer(node_coords, data, dates, out_dates, output_base)

            sfr_files = glob.glob(os.path.join(temp_dir, '*.sfr'))
            with open(sfr_files[0], 'r') as f:
                header = f.readline()

            # Header should contain NodeID, X, Y
            assert 'NodeID' in header
            assert 'X' in header
            assert 'Y' in header

    def test_output_file_has_layer_columns(self):
        """Test that output file has layer columns in header."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads')

            # Read headall data
            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)

            # Get node coordinates
            pre_path, _ = os.path.split(EXAMPLE_PRE_FILE)
            pre_dict, _ = iwfm.iwfm_read_preproc(EXAMPLE_PRE_FILE)
            node_file = os.path.join(pre_path, pre_dict['node_file'])
            node_coords, node_list, factor = iwfm.iwfm_read_nodes(node_file)

            out_dates = [dates[0]]
            headall2surfer(node_coords, data, dates, out_dates, output_base)

            sfr_files = glob.glob(os.path.join(temp_dir, '*.sfr'))
            with open(sfr_files[0], 'r') as f:
                header = f.readline()

            # Header should have Layer columns (C2VSimCG has 4 layers)
            assert 'Layer 1' in header
            assert 'Layer 4' in header

    def test_output_file_has_correct_row_count(self):
        """Test that output file has correct number of data rows (one per node)."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads')

            # Read headall data
            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)

            # Get node coordinates
            pre_path, _ = os.path.split(EXAMPLE_PRE_FILE)
            pre_dict, _ = iwfm.iwfm_read_preproc(EXAMPLE_PRE_FILE)
            node_file = os.path.join(pre_path, pre_dict['node_file'])
            node_coords, node_list, factor = iwfm.iwfm_read_nodes(node_file)

            out_dates = [dates[0]]
            headall2surfer(node_coords, data, dates, out_dates, output_base)

            sfr_files = glob.glob(os.path.join(temp_dir, '*.sfr'))
            with open(sfr_files[0], 'r') as f:
                lines = f.readlines()

            # Should have header + one row per node
            assert len(lines) == len(node_coords) + 1

    def test_output_file_is_csv_format(self):
        """Test that output file is comma-separated."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads')

            # Read headall data
            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)

            # Get node coordinates
            pre_path, _ = os.path.split(EXAMPLE_PRE_FILE)
            pre_dict, _ = iwfm.iwfm_read_preproc(EXAMPLE_PRE_FILE)
            node_file = os.path.join(pre_path, pre_dict['node_file'])
            node_coords, node_list, factor = iwfm.iwfm_read_nodes(node_file)

            out_dates = [dates[0]]
            headall2surfer(node_coords, data, dates, out_dates, output_base)

            sfr_files = glob.glob(os.path.join(temp_dir, '*.sfr'))
            with open(sfr_files[0], 'r') as f:
                lines = f.readlines()

            # Each line should have commas
            for line in lines:
                assert ',' in line


@pytest.mark.skipif(not EXAMPLE_FILES_EXIST, reason="Example files not found")
class TestHeadall2SurferReturnValue:
    """Test the return value of headall2surfer."""

    def test_returns_count(self):
        """Test that headall2surfer returns count of files written."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads')

            # Read headall data
            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)

            # Get node coordinates
            pre_path, _ = os.path.split(EXAMPLE_PRE_FILE)
            pre_dict, _ = iwfm.iwfm_read_preproc(EXAMPLE_PRE_FILE)
            node_file = os.path.join(pre_path, pre_dict['node_file'])
            node_coords, node_list, factor = iwfm.iwfm_read_nodes(node_file)

            out_dates = dates[:5]
            count = headall2surfer(node_coords, data, dates, out_dates, output_base)

            assert count == 5
            assert isinstance(count, int)

    def test_returns_zero_for_no_matching_dates(self):
        """Test that headall2surfer returns 0 when no dates match."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads')

            # Read headall data
            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)

            # Get node coordinates
            pre_path, _ = os.path.split(EXAMPLE_PRE_FILE)
            pre_dict, _ = iwfm.iwfm_read_preproc(EXAMPLE_PRE_FILE)
            node_file = os.path.join(pre_path, pre_dict['node_file'])
            node_coords, node_list, factor = iwfm.iwfm_read_nodes(node_file)

            # Use dates that don't exist in data
            out_dates = ['01/01/1900', '02/01/1900']
            count = headall2surfer(node_coords, data, dates, out_dates, output_base)

            assert count == 0


@pytest.mark.skipif(not EXAMPLE_FILES_EXIST, reason="Example files not found")
class TestHeadall2SurferDateHandling:
    """Test date handling in headall2surfer."""

    def test_first_date(self):
        """Test headall2surfer with first available date."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)

            pre_path, _ = os.path.split(EXAMPLE_PRE_FILE)
            pre_dict, _ = iwfm.iwfm_read_preproc(EXAMPLE_PRE_FILE)
            node_file = os.path.join(pre_path, pre_dict['node_file'])
            node_coords, node_list, factor = iwfm.iwfm_read_nodes(node_file)

            out_dates = [dates[0]]
            count = headall2surfer(node_coords, data, dates, out_dates, output_base)

            assert count == 1

    def test_last_date(self):
        """Test headall2surfer with last available date."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)

            pre_path, _ = os.path.split(EXAMPLE_PRE_FILE)
            pre_dict, _ = iwfm.iwfm_read_preproc(EXAMPLE_PRE_FILE)
            node_file = os.path.join(pre_path, pre_dict['node_file'])
            node_coords, node_list, factor = iwfm.iwfm_read_nodes(node_file)

            out_dates = [dates[-1]]
            count = headall2surfer(node_coords, data, dates, out_dates, output_base)

            assert count == 1

    def test_invalid_date_skipped_silently(self):
        """Test that invalid dates are skipped and don't create files."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)

            pre_path, _ = os.path.split(EXAMPLE_PRE_FILE)
            pre_dict, _ = iwfm.iwfm_read_preproc(EXAMPLE_PRE_FILE)
            node_file = os.path.join(pre_path, pre_dict['node_file'])
            node_coords, node_list, factor = iwfm.iwfm_read_nodes(node_file)

            # Mix of valid and invalid dates
            invalid_date = '01/01/1900'
            out_dates = [dates[0], invalid_date, dates[1]]
            count = headall2surfer(node_coords, data, dates, out_dates, output_base)

            # Should only create 2 files (for valid dates)
            assert count == 2
            sfr_files = glob.glob(os.path.join(temp_dir, '*.sfr'))
            assert len(sfr_files) == 2

    def test_all_invalid_dates_returns_zero(self):
        """Test that all invalid dates returns count of 0."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)

            pre_path, _ = os.path.split(EXAMPLE_PRE_FILE)
            pre_dict, _ = iwfm.iwfm_read_preproc(EXAMPLE_PRE_FILE)
            node_file = os.path.join(pre_path, pre_dict['node_file'])
            node_coords, node_list, factor = iwfm.iwfm_read_nodes(node_file)

            # All invalid dates
            out_dates = ['01/01/1900', '02/01/1900', '03/01/1900']
            count = headall2surfer(node_coords, data, dates, out_dates, output_base)

            assert count == 0
            sfr_files = glob.glob(os.path.join(temp_dir, '*.sfr'))
            assert len(sfr_files) == 0

    def test_empty_out_dates_returns_zero(self):
        """Test that empty out_dates list returns count of 0."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)

            pre_path, _ = os.path.split(EXAMPLE_PRE_FILE)
            pre_dict, _ = iwfm.iwfm_read_preproc(EXAMPLE_PRE_FILE)
            node_file = os.path.join(pre_path, pre_dict['node_file'])
            node_coords, node_list, factor = iwfm.iwfm_read_nodes(node_file)

            out_dates = []
            count = headall2surfer(node_coords, data, dates, out_dates, output_base)

            assert count == 0


@pytest.mark.skipif(not EXAMPLE_FILES_EXIST, reason="Example files not found")
class TestHeadall2SurferVerbose:
    """Test verbose output of headall2surfer."""

    def test_verbose_false_no_output(self, capsys):
        """Test that verbose=False produces no output."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)

            pre_path, _ = os.path.split(EXAMPLE_PRE_FILE)
            pre_dict, _ = iwfm.iwfm_read_preproc(EXAMPLE_PRE_FILE)
            node_file = os.path.join(pre_path, pre_dict['node_file'])
            node_coords, node_list, factor = iwfm.iwfm_read_nodes(node_file)

            out_dates = [dates[0]]
            headall2surfer(node_coords, data, dates, out_dates, output_base, verbose=False)

            captured = capsys.readouterr()
            assert captured.out == ''

    def test_verbose_true_produces_output(self, capsys):
        """Test that verbose=True produces output."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)

            pre_path, _ = os.path.split(EXAMPLE_PRE_FILE)
            pre_dict, _ = iwfm.iwfm_read_preproc(EXAMPLE_PRE_FILE)
            node_file = os.path.join(pre_path, pre_dict['node_file'])
            node_coords, node_list, factor = iwfm.iwfm_read_nodes(node_file)

            out_dates = [dates[0]]
            headall2surfer(node_coords, data, dates, out_dates, output_base, verbose=True)

            captured = capsys.readouterr()
            assert 'Wrote' in captured.out
            assert dates[0] in captured.out


@pytest.mark.skipif(not EXAMPLE_FILES_EXIST, reason="Example files not found")
class TestHeadall2SurferOutputPath:
    """Test output path handling in headall2surfer."""

    def test_output_to_subdirectory(self):
        """Test that output can be written to a subdirectory."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            subdir = os.path.join(temp_dir, 'surfer_output')
            os.makedirs(subdir)
            output_base = os.path.join(subdir, 'heads')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)

            pre_path, _ = os.path.split(EXAMPLE_PRE_FILE)
            pre_dict, _ = iwfm.iwfm_read_preproc(EXAMPLE_PRE_FILE)
            node_file = os.path.join(pre_path, pre_dict['node_file'])
            node_coords, node_list, factor = iwfm.iwfm_read_nodes(node_file)

            out_dates = [dates[0]]
            count = headall2surfer(node_coords, data, dates, out_dates, output_base)

            sfr_files = glob.glob(os.path.join(subdir, '*.sfr'))
            assert len(sfr_files) == 1

    def test_output_with_spaces_in_path(self):
        """Test that output works with spaces in path."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            subdir = os.path.join(temp_dir, 'surfer output')
            os.makedirs(subdir)
            output_base = os.path.join(subdir, 'heads output')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)

            pre_path, _ = os.path.split(EXAMPLE_PRE_FILE)
            pre_dict, _ = iwfm.iwfm_read_preproc(EXAMPLE_PRE_FILE)
            node_file = os.path.join(pre_path, pre_dict['node_file'])
            node_coords, node_list, factor = iwfm.iwfm_read_nodes(node_file)

            out_dates = [dates[0]]
            count = headall2surfer(node_coords, data, dates, out_dates, output_base)

            sfr_files = glob.glob(os.path.join(subdir, '*.sfr'))
            assert len(sfr_files) == 1


@pytest.mark.skipif(not EXAMPLE_FILES_EXIST, reason="Example files not found")
class TestHeadall2SurferC2VSimCGSpecific:
    """Test headall2surfer with C2VSimCG-specific expectations."""

    def test_c2vsimcg_file_has_1393_data_rows(self):
        """Test that C2VSimCG surfer file has 1393 data rows (one per node)."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)

            pre_path, _ = os.path.split(EXAMPLE_PRE_FILE)
            pre_dict, _ = iwfm.iwfm_read_preproc(EXAMPLE_PRE_FILE)
            node_file = os.path.join(pre_path, pre_dict['node_file'])
            node_coords, node_list, factor = iwfm.iwfm_read_nodes(node_file)

            out_dates = [dates[0]]
            headall2surfer(node_coords, data, dates, out_dates, output_base)

            sfr_files = glob.glob(os.path.join(temp_dir, '*.sfr'))
            with open(sfr_files[0], 'r') as f:
                lines = f.readlines()

            # 1 header + 1393 data rows
            assert len(lines) == 1394

    def test_c2vsimcg_file_has_7_columns(self):
        """Test that C2VSimCG surfer file has 7 columns (NodeID, X, Y, Layer1-4)."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            output_base = os.path.join(temp_dir, 'heads')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)

            pre_path, _ = os.path.split(EXAMPLE_PRE_FILE)
            pre_dict, _ = iwfm.iwfm_read_preproc(EXAMPLE_PRE_FILE)
            node_file = os.path.join(pre_path, pre_dict['node_file'])
            node_coords, node_list, factor = iwfm.iwfm_read_nodes(node_file)

            out_dates = [dates[0]]
            headall2surfer(node_coords, data, dates, out_dates, output_base)

            sfr_files = glob.glob(os.path.join(temp_dir, '*.sfr'))
            with open(sfr_files[0], 'r') as f:
                lines = f.readlines()

            # Check header has 7 columns
            header_cols = lines[0].count(',') + 1
            assert header_cols == 7

            # Check data row has 7 columns
            data_cols = lines[1].count(',') + 1
            assert data_cols == 7

    def test_c2vsimcg_layer_count(self):
        """Test that C2VSimCG model has 4 layers."""
        import iwfm

        data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
        assert layers == 4

    def test_c2vsimcg_node_count(self):
        """Test that C2VSimCG model has expected number of nodes."""
        import iwfm

        data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
        # C2VSimCG has 1393 nodes, nodes is a list of node IDs
        assert len(nodes) == 1393


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
