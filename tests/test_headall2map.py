# test_headall2map.py
# Unit tests for the headall2map function in the iwfm package
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
Tests for headall2map() function which reads headall.out file and creates
TIFF map images (node maps, contour maps, filled contour maps) for each layer.
"""

import pytest
import os
import tempfile
import glob

# Check if matplotlib is available
try:
    import matplotlib
    matplotlib.use('Agg')  # Use non-interactive backend for testing
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

# Check if shapely is available (required for bounding polygon)
try:
    import shapely  # noqa: F401
    del shapely
    SHAPELY_AVAILABLE = True
except ImportError:
    SHAPELY_AVAILABLE = False

# Import directly from module since it may not be exported in __init__.py
from iwfm.headall2map import headall2map

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

EXAMPLE_BNDS_FILE = os.path.join(
    os.path.dirname(__file__),
    'C2VSimCG-2021',
    'gis',
    'C2VSimCG_BoundaryNodes.csv'
)

# Check if the example files exist for tests that require them
EXAMPLE_FILES_EXIST = (
    os.path.exists(EXAMPLE_HEADALL_FILE) and
    os.path.exists(EXAMPLE_PRE_FILE) and
    os.path.exists(EXAMPLE_BNDS_FILE)
)

# Combined check for all dependencies
ALL_DEPS_AVAILABLE = MATPLOTLIB_AVAILABLE and SHAPELY_AVAILABLE and EXAMPLE_FILES_EXIST


class TestHeadall2MapFunctionExists:
    """Test that the headall2map function exists and is callable."""

    def test_headall2map_exists(self):
        """Test that headall2map function exists and is callable."""
        assert headall2map is not None
        assert callable(headall2map)

    def test_function_has_docstring(self):
        """Test that headall2map has a docstring."""
        assert headall2map.__doc__ is not None
        assert len(headall2map.__doc__) > 0

    def test_function_signature(self):
        """Test that headall2map has expected parameters."""
        import inspect
        sig = inspect.signature(headall2map)
        params = list(sig.parameters.keys())
        assert 'heads_file' in params
        assert 'pre_file' in params
        assert 'bnds_file' in params
        assert 'out_date' in params
        assert 'basename' in params

    def test_function_has_default_parameters(self):
        """Test that headall2map has expected default parameters."""
        import inspect
        sig = inspect.signature(headall2map)
        params = sig.parameters
        # Check defaults for optional parameters
        assert params['label'].default == 'Heads'
        assert params['units'].default == 'ft'
        assert params['verbose'].default == False


@pytest.mark.skipif(not ALL_DEPS_AVAILABLE,
                    reason="matplotlib, shapely, or example files not available")
class TestHeadall2MapOutputFiles:
    """Test that headall2map creates output files."""

    def test_creates_output_files(self):
        """Test that headall2map creates TIFF output files."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_map')

            # Get first available date from headall file
            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[0]

            headall2map(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, EXAMPLE_BNDS_FILE,
                       out_date, basename)

            # Check that TIFF files were created
            tiff_files = glob.glob(os.path.join(temp_dir, '*.tiff'))
            assert len(tiff_files) > 0

    def test_creates_files_for_each_layer(self):
        """Test that headall2map creates files for each layer."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_map')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[0]

            headall2map(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, EXAMPLE_BNDS_FILE,
                       out_date, basename)

            # Should create 3 files per layer (nodes, contour, contourf)
            # C2VSimCG has 4 layers, so 12 files total
            tiff_files = glob.glob(os.path.join(temp_dir, '*.tiff'))
            assert len(tiff_files) == layers * 3

    def test_creates_node_map_files(self):
        """Test that headall2map creates node map files."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_map')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[0]

            headall2map(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, EXAMPLE_BNDS_FILE,
                       out_date, basename)

            # Check for node map files
            for layer in range(1, layers + 1):
                node_file = f'{basename}_Layer_{layer}_nodes.tiff'
                assert os.path.exists(node_file), f"Missing node map for layer {layer}"

    def test_creates_contour_map_files(self):
        """Test that headall2map creates contour map files."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_map')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[0]

            headall2map(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, EXAMPLE_BNDS_FILE,
                       out_date, basename)

            # Check for contour map files
            for layer in range(1, layers + 1):
                contour_file = f'{basename}_Layer_{layer}_contour.tiff'
                assert os.path.exists(contour_file), f"Missing contour map for layer {layer}"

    def test_creates_filled_contour_map_files(self):
        """Test that headall2map creates filled contour map files."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_map')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[0]

            headall2map(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, EXAMPLE_BNDS_FILE,
                       out_date, basename)

            # Check for filled contour map files
            for layer in range(1, layers + 1):
                contourf_file = f'{basename}_Layer_{layer}_contourf.tiff'
                assert os.path.exists(contourf_file), f"Missing filled contour map for layer {layer}"


@pytest.mark.skipif(not ALL_DEPS_AVAILABLE,
                    reason="matplotlib, shapely, or example files not available")
class TestHeadall2MapOutputContent:
    """Test the content of headall2map output files."""

    def test_output_files_not_empty(self):
        """Test that output files are not empty."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_map')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[0]

            headall2map(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, EXAMPLE_BNDS_FILE,
                       out_date, basename)

            tiff_files = glob.glob(os.path.join(temp_dir, '*.tiff'))
            for tiff_file in tiff_files:
                assert os.path.getsize(tiff_file) > 0, f"Empty file: {tiff_file}"

    def test_output_files_are_valid_images(self):
        """Test that output files are valid image files."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_map')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[0]

            headall2map(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, EXAMPLE_BNDS_FILE,
                       out_date, basename)

            # Try to read first image file to verify it's valid
            node_file = f'{basename}_Layer_1_nodes.tiff'
            if os.path.exists(node_file):
                # Check file starts with TIFF magic bytes
                with open(node_file, 'rb') as f:
                    header = f.read(4)
                # TIFF files start with II (little-endian) or MM (big-endian)
                assert header[:2] in [b'II', b'MM'], "File is not a valid TIFF"


@pytest.mark.skipif(not ALL_DEPS_AVAILABLE,
                    reason="matplotlib, shapely, or example files not available")
class TestHeadall2MapParameters:
    """Test headall2map with different parameters."""

    def test_custom_label(self):
        """Test headall2map with custom label."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_map')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[0]

            # Should not raise exception
            headall2map(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, EXAMPLE_BNDS_FILE,
                       out_date, basename, label='Groundwater Heads')

            tiff_files = glob.glob(os.path.join(temp_dir, '*.tiff'))
            assert len(tiff_files) > 0

    def test_custom_units(self):
        """Test headall2map with custom units."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_map')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[0]

            # Should not raise exception
            headall2map(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, EXAMPLE_BNDS_FILE,
                       out_date, basename, units='meters')

            tiff_files = glob.glob(os.path.join(temp_dir, '*.tiff'))
            assert len(tiff_files) > 0

    def test_verbose_false(self):
        """Test headall2map with verbose=False."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_map')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[0]

            # Should not raise exception
            headall2map(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, EXAMPLE_BNDS_FILE,
                       out_date, basename, verbose=False)

            tiff_files = glob.glob(os.path.join(temp_dir, '*.tiff'))
            assert len(tiff_files) > 0

    def test_verbose_true(self):
        """Test headall2map with verbose=True."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_map')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[0]

            # Should not raise exception
            headall2map(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, EXAMPLE_BNDS_FILE,
                       out_date, basename, verbose=True)

            tiff_files = glob.glob(os.path.join(temp_dir, '*.tiff'))
            assert len(tiff_files) > 0


@pytest.mark.skipif(not ALL_DEPS_AVAILABLE,
                    reason="matplotlib, shapely, or example files not available")
class TestHeadall2MapDateSelection:
    """Test headall2map date selection."""

    def test_first_date(self):
        """Test headall2map with first available date."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_map')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[0]  # First date

            headall2map(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, EXAMPLE_BNDS_FILE,
                       out_date, basename)

            tiff_files = glob.glob(os.path.join(temp_dir, '*.tiff'))
            assert len(tiff_files) > 0

    def test_last_date(self):
        """Test headall2map with last available date."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_map')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[-1]  # Last date

            headall2map(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, EXAMPLE_BNDS_FILE,
                       out_date, basename)

            tiff_files = glob.glob(os.path.join(temp_dir, '*.tiff'))
            assert len(tiff_files) > 0

    def test_middle_date(self):
        """Test headall2map with a middle date."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_map')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[len(dates) // 2]  # Middle date

            headall2map(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, EXAMPLE_BNDS_FILE,
                       out_date, basename)

            tiff_files = glob.glob(os.path.join(temp_dir, '*.tiff'))
            assert len(tiff_files) > 0

    def test_invalid_date_prints_error_and_returns(self, capsys):
        """Test that invalid date prints error message and returns without creating files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_map')

            # Use a date that definitely doesn't exist in the data
            # C2VSimCG data runs from 09/30/1973 to 09/30/2015
            invalid_date = '01/01/1900'

            # Should return without raising an exception
            result = headall2map(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, EXAMPLE_BNDS_FILE,
                                invalid_date, basename)

            # Should return None (early return)
            assert result is None

            # Should print error message
            captured = capsys.readouterr()
            assert 'Error' in captured.out
            assert invalid_date in captured.out

            # Should not create any TIFF files
            tiff_files = glob.glob(os.path.join(temp_dir, '*.tiff'))
            assert len(tiff_files) == 0


@pytest.mark.skipif(not ALL_DEPS_AVAILABLE,
                    reason="matplotlib, shapely, or example files not available")
class TestHeadall2MapReturnValue:
    """Test the return value of headall2map."""

    def test_returns_none(self):
        """Test that headall2map returns None."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_map')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[0]

            result = headall2map(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, EXAMPLE_BNDS_FILE,
                                out_date, basename)

            assert result is None


@pytest.mark.skipif(not ALL_DEPS_AVAILABLE,
                    reason="matplotlib, shapely, or example files not available")
class TestHeadall2MapOutputPath:
    """Test output path handling in headall2map."""

    def test_output_to_subdirectory(self):
        """Test that output can be written to a subdirectory."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            subdir = os.path.join(temp_dir, 'maps')
            os.makedirs(subdir)
            basename = os.path.join(subdir, 'heads_map')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[0]

            headall2map(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, EXAMPLE_BNDS_FILE,
                       out_date, basename)

            tiff_files = glob.glob(os.path.join(subdir, '*.tiff'))
            assert len(tiff_files) > 0

    def test_output_with_spaces_in_path(self):
        """Test that output works with spaces in path."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            subdir = os.path.join(temp_dir, 'output maps')
            os.makedirs(subdir)
            basename = os.path.join(subdir, 'heads map')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[0]

            headall2map(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, EXAMPLE_BNDS_FILE,
                       out_date, basename)

            tiff_files = glob.glob(os.path.join(subdir, '*.tiff'))
            assert len(tiff_files) > 0


@pytest.mark.skipif(not ALL_DEPS_AVAILABLE,
                    reason="matplotlib, shapely, or example files not available")
class TestHeadall2MapC2VSimCGSpecific:
    """Test headall2map with C2VSimCG-specific expectations."""

    def test_c2vsimcg_creates_12_files(self):
        """Test that C2VSimCG data creates 12 files (3 per layer x 4 layers)."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_map')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[0]

            headall2map(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, EXAMPLE_BNDS_FILE,
                       out_date, basename)

            tiff_files = glob.glob(os.path.join(temp_dir, '*.tiff'))
            # 4 layers * 3 map types = 12 files
            assert len(tiff_files) == 12

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
