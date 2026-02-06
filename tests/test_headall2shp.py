# test_headall2shp.py
# Unit tests for the headall2shp function in the iwfm package
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
Tests for headall2shp() function which reads headall.out file and creates
shapefiles of heads with point geometry for each node.
"""

import pytest
import os
import tempfile
import glob

# Check if pyshp (shapefile) is available
try:
    import shapefile
    SHAPEFILE_AVAILABLE = True
except ImportError:
    SHAPEFILE_AVAILABLE = False

# Import directly from module since it may not be exported in __init__.py
from iwfm.headall2shp import headall2shp

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

# Combined check for all dependencies
ALL_DEPS_AVAILABLE = SHAPEFILE_AVAILABLE and EXAMPLE_FILES_EXIST


class TestHeadall2ShpFunctionExists:
    """Test that the headall2shp function exists and is callable."""

    def test_headall2shp_exists(self):
        """Test that headall2shp function exists and is callable."""
        assert headall2shp is not None
        assert callable(headall2shp)

    def test_function_has_docstring(self):
        """Test that headall2shp has a docstring."""
        assert headall2shp.__doc__ is not None
        assert len(headall2shp.__doc__) > 0

    def test_function_signature(self):
        """Test that headall2shp has expected parameters."""
        import inspect
        sig = inspect.signature(headall2shp)
        params = list(sig.parameters.keys())
        assert 'heads_file' in params
        assert 'pre_file' in params
        assert 'out_date' in params
        assert 'basename' in params

    def test_function_has_default_parameters(self):
        """Test that headall2shp has expected default parameters."""
        import inspect
        sig = inspect.signature(headall2shp)
        params = sig.parameters
        # Check defaults for optional parameters
        assert params['label'].default == 'Heads'
        assert params['units'].default == 'ft'
        assert params['epsg'].default == 26910  # NAD 83 UTM Zone 10N (California)
        assert params['verbose'].default == True


@pytest.mark.skipif(not ALL_DEPS_AVAILABLE,
                    reason="pyshp or example files not available")
class TestHeadall2ShpOutputFiles:
    """Test that headall2shp creates output files."""

    def test_creates_shapefile(self):
        """Test that headall2shp creates shapefile output."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_shp')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[0]

            headall2shp(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE,
                       out_date, basename)

            # Check that shapefile was created (at least .shp file)
            shp_files = glob.glob(os.path.join(temp_dir, '*.shp'))
            assert len(shp_files) > 0

    def test_creates_all_shapefile_components(self):
        """Test that headall2shp creates all shapefile components (.shp, .shx, .dbf)."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_shp')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[0]
            out_date_text = out_date.replace('/', '_')

            headall2shp(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE,
                       out_date, basename)

            # Shapefile components
            expected_basename = f'{basename}_{out_date_text}_Nodal_Heads'
            assert os.path.exists(f'{expected_basename}.shp'), "Missing .shp file"
            assert os.path.exists(f'{expected_basename}.shx'), "Missing .shx file"
            assert os.path.exists(f'{expected_basename}.dbf'), "Missing .dbf file"

    def test_creates_prj_file(self):
        """Test that headall2shp creates projection file (.prj)."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_shp')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[0]
            out_date_text = out_date.replace('/', '_')

            headall2shp(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE,
                       out_date, basename)

            expected_basename = f'{basename}_{out_date_text}_Nodal_Heads'
            assert os.path.exists(f'{expected_basename}.prj'), "Missing .prj file"


@pytest.mark.skipif(not ALL_DEPS_AVAILABLE,
                    reason="pyshp or example files not available")
class TestHeadall2ShpOutputContent:
    """Test the content of headall2shp output files."""

    def test_shapefile_has_correct_record_count(self):
        """Test that shapefile has correct number of records (nodes)."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_shp')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[0]
            out_date_text = out_date.replace('/', '_')

            headall2shp(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE,
                       out_date, basename)

            expected_basename = f'{basename}_{out_date_text}_Nodal_Heads'
            sf = shapefile.Reader(expected_basename)
            assert len(sf.records()) == len(nodes)

    def test_shapefile_has_correct_fields(self):
        """Test that shapefile has correct attribute fields."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_shp')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[0]
            out_date_text = out_date.replace('/', '_')

            headall2shp(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE,
                       out_date, basename)

            expected_basename = f'{basename}_{out_date_text}_Nodal_Heads'
            sf = shapefile.Reader(expected_basename)
            field_names = [field[0] for field in sf.fields[1:]]  # Skip DeletionFlag

            # Should have node_id field
            assert 'node_id' in field_names

            # Should have one Heads field per layer
            for layer in range(1, layers + 1):
                assert f'Heads_{layer}' in field_names

    def test_shapefile_geometry_is_point(self):
        """Test that shapefile geometry type is POINT."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_shp')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[0]
            out_date_text = out_date.replace('/', '_')

            headall2shp(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE,
                       out_date, basename)

            expected_basename = f'{basename}_{out_date_text}_Nodal_Heads'
            sf = shapefile.Reader(expected_basename)
            assert sf.shapeType == shapefile.POINT

    def test_shapefile_not_empty(self):
        """Test that shapefile files are not empty."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_shp')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[0]
            out_date_text = out_date.replace('/', '_')

            headall2shp(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE,
                       out_date, basename)

            expected_basename = f'{basename}_{out_date_text}_Nodal_Heads'
            for ext in ['.shp', '.shx', '.dbf']:
                filepath = f'{expected_basename}{ext}'
                assert os.path.getsize(filepath) > 0, f"Empty file: {filepath}"

    def test_shapefile_head_values_are_numeric(self):
        """Test that head values in shapefile are numeric."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_shp')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[0]
            out_date_text = out_date.replace('/', '_')

            headall2shp(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE,
                       out_date, basename)

            expected_basename = f'{basename}_{out_date_text}_Nodal_Heads'
            sf = shapefile.Reader(expected_basename)

            # Check first record has numeric values
            rec = sf.record(0)
            # First field is node_id, rest are head values
            for i in range(1, len(rec)):
                assert isinstance(rec[i], (int, float)), f"Field {i} is not numeric"


@pytest.mark.skipif(not ALL_DEPS_AVAILABLE,
                    reason="pyshp or example files not available")
class TestHeadall2ShpParameters:
    """Test headall2shp with different parameters."""

    def test_custom_label(self):
        """Test headall2shp with custom label."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_shp')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[0]
            out_date_text = out_date.replace('/', '_')

            headall2shp(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE,
                       out_date, basename, label='GWHeads')

            # Check that shapefile was created with custom label in name
            expected_basename = f'{basename}_{out_date_text}_Nodal_GWHeads'
            assert os.path.exists(f'{expected_basename}.shp')

    def test_custom_label_affects_field_names(self):
        """Test that custom label affects field names in shapefile."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_shp')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[0]
            out_date_text = out_date.replace('/', '_')

            headall2shp(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE,
                       out_date, basename, label='GWHeads')

            expected_basename = f'{basename}_{out_date_text}_Nodal_GWHeads'
            sf = shapefile.Reader(expected_basename)
            field_names = [field[0] for field in sf.fields[1:]]

            # Should have GWHeads_1, GWHeads_2, etc. instead of Heads_1, etc.
            assert 'GWHeads_1' in field_names

    def test_custom_epsg(self):
        """Test headall2shp with custom EPSG code."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_shp')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[0]

            # EPSG 4326 is WGS 84 (lat/lon)
            headall2shp(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE,
                       out_date, basename, epsg=4326)

            shp_files = glob.glob(os.path.join(temp_dir, '*.shp'))
            assert len(shp_files) > 0

    def test_verbose_false(self):
        """Test headall2shp with verbose=False."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_shp')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[0]

            # Should not raise exception
            headall2shp(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE,
                       out_date, basename, verbose=False)

            shp_files = glob.glob(os.path.join(temp_dir, '*.shp'))
            assert len(shp_files) > 0

    def test_verbose_true(self):
        """Test headall2shp with verbose=True."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_shp')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[0]

            # Should not raise exception
            headall2shp(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE,
                       out_date, basename, verbose=True)

            shp_files = glob.glob(os.path.join(temp_dir, '*.shp'))
            assert len(shp_files) > 0


@pytest.mark.skipif(not ALL_DEPS_AVAILABLE,
                    reason="pyshp or example files not available")
class TestHeadall2ShpDateSelection:
    """Test headall2shp date selection."""

    def test_first_date(self):
        """Test headall2shp with first available date."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_shp')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[0]  # First date

            headall2shp(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE,
                       out_date, basename)

            shp_files = glob.glob(os.path.join(temp_dir, '*.shp'))
            assert len(shp_files) > 0

    def test_last_date(self):
        """Test headall2shp with last available date."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_shp')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[-1]  # Last date

            headall2shp(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE,
                       out_date, basename)

            shp_files = glob.glob(os.path.join(temp_dir, '*.shp'))
            assert len(shp_files) > 0

    def test_middle_date(self):
        """Test headall2shp with a middle date."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_shp')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[len(dates) // 2]  # Middle date

            headall2shp(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE,
                       out_date, basename)

            shp_files = glob.glob(os.path.join(temp_dir, '*.shp'))
            assert len(shp_files) > 0

    def test_date_in_filename(self):
        """Test that output filename includes the date."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_shp')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[0]
            out_date_text = out_date.replace('/', '_')  # e.g., 09_30_1973

            headall2shp(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE,
                       out_date, basename)

            # Check that date is in filename
            shp_files = glob.glob(os.path.join(temp_dir, f'*{out_date_text}*.shp'))
            assert len(shp_files) > 0

    def test_invalid_date_prints_error_and_returns(self, capsys):
        """Test that invalid date prints error message and returns without creating shapefile."""
        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_shp')

            # Use a date that definitely doesn't exist in the data
            # C2VSimCG data runs from 09/30/1973 to 09/30/2015
            invalid_date = '01/01/1900'

            # Should return without raising an exception
            result = headall2shp(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE,
                                invalid_date, basename)

            # Should return None (early return)
            assert result is None

            # Should print error message
            captured = capsys.readouterr()
            assert 'Error' in captured.out
            assert invalid_date in captured.out

            # Should not create any shapefile
            shp_files = glob.glob(os.path.join(temp_dir, '*.shp'))
            assert len(shp_files) == 0


@pytest.mark.skipif(not ALL_DEPS_AVAILABLE,
                    reason="pyshp or example files not available")
class TestHeadall2ShpReturnValue:
    """Test the return value of headall2shp."""

    def test_returns_none(self):
        """Test that headall2shp returns None."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_shp')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[0]

            result = headall2shp(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE,
                                out_date, basename)

            assert result is None


@pytest.mark.skipif(not ALL_DEPS_AVAILABLE,
                    reason="pyshp or example files not available")
class TestHeadall2ShpOutputPath:
    """Test output path handling in headall2shp."""

    def test_output_to_subdirectory(self):
        """Test that output can be written to a subdirectory."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            subdir = os.path.join(temp_dir, 'shapefiles')
            os.makedirs(subdir)
            basename = os.path.join(subdir, 'heads_shp')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[0]

            headall2shp(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE,
                       out_date, basename)

            shp_files = glob.glob(os.path.join(subdir, '*.shp'))
            assert len(shp_files) > 0

    def test_output_with_spaces_in_path(self):
        """Test that output works with spaces in path."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            subdir = os.path.join(temp_dir, 'output shapefiles')
            os.makedirs(subdir)
            basename = os.path.join(subdir, 'heads shp')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[0]

            headall2shp(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE,
                       out_date, basename)

            shp_files = glob.glob(os.path.join(subdir, '*.shp'))
            assert len(shp_files) > 0


@pytest.mark.skipif(not ALL_DEPS_AVAILABLE,
                    reason="pyshp or example files not available")
class TestHeadall2ShpC2VSimCGSpecific:
    """Test headall2shp with C2VSimCG-specific expectations."""

    def test_c2vsimcg_shapefile_has_1393_records(self):
        """Test that C2VSimCG shapefile has 1393 records (nodes)."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_shp')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[0]
            out_date_text = out_date.replace('/', '_')

            headall2shp(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE,
                       out_date, basename)

            expected_basename = f'{basename}_{out_date_text}_Nodal_Heads'
            sf = shapefile.Reader(expected_basename)
            assert len(sf.records()) == 1393

    def test_c2vsimcg_shapefile_has_4_layer_fields(self):
        """Test that C2VSimCG shapefile has 4 layer fields."""
        import iwfm

        with tempfile.TemporaryDirectory() as temp_dir:
            basename = os.path.join(temp_dir, 'heads_shp')

            data, layers, dates, nodes = iwfm.headall_read(EXAMPLE_HEADALL_FILE)
            out_date = dates[0]
            out_date_text = out_date.replace('/', '_')

            headall2shp(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE,
                       out_date, basename)

            expected_basename = f'{basename}_{out_date_text}_Nodal_Heads'
            sf = shapefile.Reader(expected_basename)
            field_names = [field[0] for field in sf.fields[1:]]

            # Should have Heads_1, Heads_2, Heads_3, Heads_4
            for layer in range(1, 5):
                assert f'Heads_{layer}' in field_names

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
