# test_headall2dtw.py
# Unit tests for the headall2dtw function in the iwfm package
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
import tempfile
import glob

# Import directly from module since it may not be exported in __init__.py
from iwfm.headall2dtw import headall2dtw

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


class TestHeadall2DtwFunctionExists:
    """Test that the headall2dtw function exists and is callable."""

    def test_headall2dtw_exists(self):
        """Test that headall2dtw function exists and is callable."""
        assert headall2dtw is not None
        assert callable(headall2dtw)


@pytest.mark.skipif(not EXAMPLE_FILES_EXIST, reason="C2VSimCG example files not found")
class TestHeadall2DtwOutputFiles:
    """Test that headall2dtw creates output files."""

    def test_creates_output_files(self):
        """Test that headall2dtw creates CSV output files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = os.path.join(temp_dir, 'dtw_output')

            headall2dtw(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, output_root)

            # Check that at least one CSV file was created
            csv_files = glob.glob(os.path.join(temp_dir, 'dtw_output_*.csv'))
            assert len(csv_files) > 0

    def test_creates_one_file_per_layer(self):
        """Test that headall2dtw creates one CSV file per layer."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = os.path.join(temp_dir, 'dtw_output')

            headall2dtw(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, output_root)

            # C2VSimCG has 4 layers, so should create 4 files
            csv_files = glob.glob(os.path.join(temp_dir, 'dtw_output_*.csv'))
            assert len(csv_files) == 4

    def test_output_files_named_correctly(self):
        """Test that output files are named with layer numbers."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = os.path.join(temp_dir, 'dtw_output')

            headall2dtw(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, output_root)

            # Check for files named _1.csv, _2.csv, _3.csv, _4.csv
            for layer in range(1, 5):
                expected_file = f'{output_root}_{layer}.csv'
                assert os.path.exists(expected_file), f"Expected file {expected_file} not found"


@pytest.mark.skipif(not EXAMPLE_FILES_EXIST, reason="C2VSimCG example files not found")
class TestHeadall2DtwOutputContent:
    """Test the content of headall2dtw output files."""

    def test_output_files_not_empty(self):
        """Test that output files are not empty."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = os.path.join(temp_dir, 'dtw_output')

            headall2dtw(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, output_root)

            csv_files = glob.glob(os.path.join(temp_dir, 'dtw_output_*.csv'))
            for csv_file in csv_files:
                assert os.path.getsize(csv_file) > 0

    def test_output_files_have_header(self):
        """Test that output files have a header row."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = os.path.join(temp_dir, 'dtw_output')

            headall2dtw(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, output_root)

            # Read first file and check header
            csv_file = f'{output_root}_1.csv'
            with open(csv_file, 'r') as f:
                header = f.readline().strip()

            # Header should start with 'Node'
            assert header.startswith('Node')

    def test_output_files_have_node_column(self):
        """Test that output files have a Node column."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = os.path.join(temp_dir, 'dtw_output')

            headall2dtw(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, output_root)

            csv_file = f'{output_root}_1.csv'
            with open(csv_file, 'r') as f:
                header = f.readline().strip()
                columns = header.split(',')

            assert columns[0] == 'Node'

    def test_output_files_have_date_columns(self):
        """Test that output files have date columns after Node."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = os.path.join(temp_dir, 'dtw_output')

            headall2dtw(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, output_root)

            csv_file = f'{output_root}_1.csv'
            with open(csv_file, 'r') as f:
                header = f.readline().strip()
                columns = header.split(',')

            # Should have more than just 'Node' column
            assert len(columns) > 1

            # Second column should be a date
            second_col = columns[1]
            assert '/' in second_col  # Date format MM/DD/YYYY

    def test_output_has_correct_number_of_data_rows(self):
        """Test that output has correct number of data rows (one per node)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = os.path.join(temp_dir, 'dtw_output')

            headall2dtw(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, output_root)

            csv_file = f'{output_root}_1.csv'
            with open(csv_file, 'r') as f:
                lines = f.readlines()

            # C2VSimCG has 1393 nodes, plus 1 header row
            assert len(lines) == 1394


@pytest.mark.skipif(not EXAMPLE_FILES_EXIST, reason="C2VSimCG example files not found")
class TestHeadall2DtwDataValues:
    """Test the data values in headall2dtw output."""

    def test_dtw_values_are_numeric(self):
        """Test that depth to water values are numeric."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = os.path.join(temp_dir, 'dtw_output')

            headall2dtw(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, output_root)

            csv_file = f'{output_root}_1.csv'
            with open(csv_file, 'r') as f:
                lines = f.readlines()

            # Skip header, check first data row
            data_row = lines[1].strip().split(',')

            # Skip first column (Node), check that values are numeric
            for value in data_row[1:]:
                float(value)  # Should not raise exception

    def test_dtw_values_reasonable_range(self):
        """Test that depth to water values are in reasonable range.

        DTW can be negative (artesian conditions) or positive (water below surface).
        Typical range is -100 to +500 feet for California.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = os.path.join(temp_dir, 'dtw_output')

            headall2dtw(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, output_root)

            csv_file = f'{output_root}_1.csv'
            with open(csv_file, 'r') as f:
                lines = f.readlines()

            # Check first few data rows
            for line in lines[1:10]:
                data_row = line.strip().split(',')
                for value in data_row[1:]:
                    dtw = float(value)
                    # DTW typically between -500 and +1000 feet
                    assert -1000 < dtw < 2000

    def test_node_ids_are_integers(self):
        """Test that node IDs are valid integers."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = os.path.join(temp_dir, 'dtw_output')

            headall2dtw(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, output_root)

            csv_file = f'{output_root}_1.csv'
            with open(csv_file, 'r') as f:
                lines = f.readlines()

            # Check node IDs in first few data rows
            for line in lines[1:10]:
                data_row = line.strip().split(',')
                node_id = data_row[0]
                int(node_id)  # Should not raise exception


@pytest.mark.skipif(not EXAMPLE_FILES_EXIST, reason="C2VSimCG example files not found")
class TestHeadall2DtwVerbose:
    """Test the verbose parameter of headall2dtw."""

    def test_verbose_false_no_error(self):
        """Test that verbose=False runs without error."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = os.path.join(temp_dir, 'dtw_output')

            # Should not raise exception
            headall2dtw(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, output_root, verbose=False)

    def test_verbose_true_no_error(self):
        """Test that verbose=True runs without error."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = os.path.join(temp_dir, 'dtw_output')

            # Should not raise exception
            headall2dtw(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, output_root, verbose=True)

    def test_verbose_produces_output(self, capsys):
        """Test that verbose=True produces console output."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = os.path.join(temp_dir, 'dtw_output')

            headall2dtw(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, output_root, verbose=True)

            captured = capsys.readouterr()
            # Verbose mode should print something about writing layers
            assert 'Wrote' in captured.out or 'layer' in captured.out.lower()


@pytest.mark.skipif(not EXAMPLE_FILES_EXIST, reason="C2VSimCG example files not found")
class TestHeadall2DtwReturnValue:
    """Test the return value of headall2dtw."""

    def test_returns_none(self):
        """Test that headall2dtw returns None."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = os.path.join(temp_dir, 'dtw_output')

            result = headall2dtw(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, output_root)

            assert result is None


@pytest.mark.skipif(not EXAMPLE_FILES_EXIST, reason="C2VSimCG example files not found")
class TestHeadall2DtwConsistency:
    """Test consistency of headall2dtw results."""

    def test_multiple_runs_same_output(self):
        """Test that multiple runs produce the same output."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_root1 = os.path.join(temp_dir, 'dtw_output1')
            output_root2 = os.path.join(temp_dir, 'dtw_output2')

            headall2dtw(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, output_root1)
            headall2dtw(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, output_root2)

            # Compare first layer files
            with open(f'{output_root1}_1.csv', 'r') as f1:
                content1 = f1.read()
            with open(f'{output_root2}_1.csv', 'r') as f2:
                content2 = f2.read()

            assert content1 == content2

    def test_all_layers_have_same_structure(self):
        """Test that all layer files have the same structure."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = os.path.join(temp_dir, 'dtw_output')

            headall2dtw(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, output_root)

            # Read headers from all layer files
            headers = []
            row_counts = []
            for layer in range(1, 5):
                csv_file = f'{output_root}_{layer}.csv'
                with open(csv_file, 'r') as f:
                    lines = f.readlines()
                    headers.append(lines[0])
                    row_counts.append(len(lines))

            # All headers should be identical
            for header in headers:
                assert header == headers[0]

            # All files should have same number of rows
            for count in row_counts:
                assert count == row_counts[0]


@pytest.mark.skipif(not EXAMPLE_FILES_EXIST, reason="C2VSimCG example files not found")
class TestHeadall2DtwC2VSimCGSpecific:
    """Test headall2dtw with C2VSimCG-specific expectations."""

    def test_c2vsimcg_creates_4_layer_files(self):
        """Test that C2VSimCG data creates 4 layer files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = os.path.join(temp_dir, 'dtw_output')

            headall2dtw(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, output_root)

            csv_files = glob.glob(os.path.join(temp_dir, 'dtw_output_*.csv'))
            assert len(csv_files) == 4

    def test_c2vsimcg_has_1393_nodes(self):
        """Test that C2VSimCG output has 1393 nodes."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = os.path.join(temp_dir, 'dtw_output')

            headall2dtw(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, output_root)

            csv_file = f'{output_root}_1.csv'
            with open(csv_file, 'r') as f:
                lines = f.readlines()

            # 1393 nodes + 1 header = 1394 lines
            assert len(lines) == 1394


class TestHeadall2DtwErrorHandling:
    """Test error handling in headall2dtw."""

    def test_nonexistent_heads_file_raises_error(self):
        """Test that nonexistent heads file raises an error."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = os.path.join(temp_dir, 'dtw_output')

            with pytest.raises(FileNotFoundError):
                headall2dtw(
                    'nonexistent_headall.out',
                    EXAMPLE_PRE_FILE if EXAMPLE_FILES_EXIST else 'dummy.in',
                    output_root
                )

    @pytest.mark.skipif(not EXAMPLE_FILES_EXIST, reason="C2VSimCG example files not found")
    def test_nonexistent_pre_file_raises_error(self):
        """Test that nonexistent preprocessor file raises an error."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = os.path.join(temp_dir, 'dtw_output')

            with pytest.raises((FileNotFoundError, SystemExit)):
                headall2dtw(
                    EXAMPLE_HEADALL_FILE,
                    'nonexistent_preprocessor.in',
                    output_root
                )


@pytest.mark.skipif(not EXAMPLE_FILES_EXIST, reason="C2VSimCG example files not found")
class TestHeadall2DtwOutputPath:
    """Test output path handling in headall2dtw."""

    def test_output_to_different_directory(self):
        """Test that output can be written to a different directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            subdir = os.path.join(temp_dir, 'subdir')
            os.makedirs(subdir)
            output_root = os.path.join(subdir, 'dtw_output')

            headall2dtw(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, output_root)

            csv_files = glob.glob(os.path.join(subdir, 'dtw_output_*.csv'))
            assert len(csv_files) == 4

    def test_output_with_spaces_in_path(self):
        """Test that output works with spaces in path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            subdir = os.path.join(temp_dir, 'sub dir with spaces')
            os.makedirs(subdir)
            output_root = os.path.join(subdir, 'dtw_output')

            headall2dtw(EXAMPLE_HEADALL_FILE, EXAMPLE_PRE_FILE, output_root)

            csv_files = glob.glob(os.path.join(subdir, 'dtw_output_*.csv'))
            assert len(csv_files) == 4


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
