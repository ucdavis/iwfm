# test_lu2csv.py
# unit tests for lu2csv function
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
import csv
import os

import pytest

import iwfm


class TestLu2csv:
    """Tests for the lu2csv function."""

    def test_basic_conversion(self, tmp_path):
        """Test basic conversion of land use file to CSV."""
        # Create a minimal land use file
        input_file = tmp_path / "test_landuse.dat"
        input_content = """\
C This is a comment line
C Another comment
 43560.0                                    / FACTLNNRV
 1                                          / NSPLNVRV
 0                                          / NFQLNVRV
                                            / DSSFL
09/30/1974_24:00	1	450.185	154.017
			2	156.854	91.323
			3	9629.810	45.288
"""
        input_file.write_text(input_content)

        # Run the function
        iwfm.lu2csv(str(input_file))

        # Check output file was created
        output_file = tmp_path / "test_landuse.csv"
        assert output_file.exists()

        # Read and verify CSV content
        with open(output_file, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)

        # Should have 3 data rows
        assert len(rows) == 3

        # First row should have date extracted
        assert rows[0][0] == '1974'  # year
        assert rows[0][1] == '09'    # month
        assert rows[0][2] == '30'    # day
        assert rows[0][3] == '1'     # element number
        assert rows[0][4] == '450.185'
        assert rows[0][5] == '154.017'

        # Second row should inherit date from previous
        assert rows[1][0] == '1974'
        assert rows[1][1] == '09'
        assert rows[1][2] == '30'
        assert rows[1][3] == '2'     # element number
        assert rows[1][4] == '156.854'
        assert rows[1][5] == '91.323'

    def test_skip_parameter(self, tmp_path):
        """Test that skip parameter correctly skips non-comment lines."""
        input_file = tmp_path / "test_skip.dat"
        input_content = """\
C Comment line
 header_line_1
 header_line_2
09/30/1974_24:00	1	100.0	200.0
"""
        input_file.write_text(input_content)

        # Default skip=4, but we only have 2 header lines, so data should be skipped
        iwfm.lu2csv(str(input_file), skip=2)

        output_file = tmp_path / "test_skip.csv"
        assert output_file.exists()

        with open(output_file, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)

        # Should have 1 data row (the date line)
        assert len(rows) == 1
        assert rows[0][0] == '1974'

    def test_multiple_dates(self, tmp_path):
        """Test file with multiple date entries."""
        input_file = tmp_path / "test_multi_date.dat"
        input_content = """\
C Comment
 header1
 header2
 header3
 header4
09/30/1974_24:00	1	100.0	200.0
			2	150.0	250.0
10/31/1974_24:00	1	110.0	210.0
			2	160.0	260.0
"""
        input_file.write_text(input_content)

        iwfm.lu2csv(str(input_file), skip=4)

        output_file = tmp_path / "test_multi_date.csv"
        with open(output_file, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)

        assert len(rows) == 4

        # First two rows should be September
        assert rows[0][1] == '09'
        assert rows[1][1] == '09'

        # Last two rows should be October
        assert rows[2][1] == '10'
        assert rows[2][2] == '31'
        assert rows[3][1] == '10'

    def test_verbose_output(self, tmp_path, capsys):
        """Test verbose output shows line count."""
        input_file = tmp_path / "test_verbose.dat"
        input_content = """\
C Comment
 h1
 h2
 h3
 h4
09/30/1974_24:00	1	100.0	200.0
			2	150.0	250.0
			3	175.0	275.0
"""
        input_file.write_text(input_content)

        iwfm.lu2csv(str(input_file), skip=4, verbose=True)

        captured = capsys.readouterr()
        assert '3' in captured.out  # Should report 3 lines
        assert 'test_verbose.csv' in captured.out

    def test_no_verbose_output(self, tmp_path, capsys):
        """Test that verbose=False produces no output."""
        input_file = tmp_path / "test_quiet.dat"
        input_content = """\
C Comment
 h1
 h2
 h3
 h4
09/30/1974_24:00	1	100.0	200.0
"""
        input_file.write_text(input_content)

        iwfm.lu2csv(str(input_file), skip=4, verbose=False)

        captured = capsys.readouterr()
        assert captured.out == ''

    def test_output_filename_changes_extension(self, tmp_path):
        """Test that output file has .csv extension regardless of input extension."""
        input_file = tmp_path / "landuse.dat"
        input_content = """\
C Comment
 h1
 h2
 h3
 h4
09/30/1974_24:00	1	100.0	200.0
"""
        input_file.write_text(input_content)

        iwfm.lu2csv(str(input_file))

        # Should create .csv file with same base name
        expected_output = tmp_path / "landuse.csv"
        assert expected_output.exists()

    def test_different_comment_characters(self, tmp_path):
        """Test that C, c, *, and # are all recognized as comment characters."""
        input_file = tmp_path / "test_comments.dat"
        input_content = """\
C Capital C comment
c lowercase c comment
* asterisk comment
# hash comment
 h1
 h2
 h3
 h4
09/30/1974_24:00	1	100.0	200.0
"""
        input_file.write_text(input_content)

        iwfm.lu2csv(str(input_file), skip=4)

        output_file = tmp_path / "test_comments.csv"
        with open(output_file, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)

        # Only 1 data row should appear (comments should be skipped)
        assert len(rows) == 1
        assert rows[0][0] == '1974'

    def test_empty_data_section(self, tmp_path):
        """Test file with only comments and headers but no data."""
        input_file = tmp_path / "test_empty.dat"
        input_content = """\
C Comment line 1
C Comment line 2
 h1
 h2
 h3
 h4
"""
        input_file.write_text(input_content)

        iwfm.lu2csv(str(input_file), skip=4)

        output_file = tmp_path / "test_empty.csv"
        assert output_file.exists()

        with open(output_file, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)

        assert len(rows) == 0

    def test_with_real_test_file(self):
        """Test with actual C2VSimCG test data file if available."""
        test_file = os.path.join(
            os.path.dirname(__file__),
            'C2VSimCG-2021',
            'Simulation',
            'RootZone',
            'C2VSimCG_NativeVeg_Area.dat'
        )

        if not os.path.exists(test_file):
            pytest.skip("Test data file not available")

        # Create a temporary output directory
        import tempfile
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Copy input file to temp dir so output goes there
            import shutil
            temp_input = os.path.join(tmp_dir, 'C2VSimCG_NativeVeg_Area.dat')
            shutil.copy(test_file, temp_input)

            # Run conversion
            iwfm.lu2csv(temp_input, verbose=False)

            # Check output exists
            output_file = os.path.join(tmp_dir, 'C2VSimCG_NativeVeg_Area.csv')
            assert os.path.exists(output_file)

            # Verify CSV content structure
            with open(output_file, 'r') as f:
                reader = csv.reader(f)
                rows = list(reader)

            # Should have data rows
            assert len(rows) > 0

            # First row should have year, month, day, element, and values
            assert len(rows[0]) >= 5
            # Year should be 4 digits
            assert len(rows[0][0]) == 4
            # Month should be 2 digits
            assert len(rows[0][1]) == 2

    def test_date_parsing_various_formats(self, tmp_path):
        """Test date parsing extracts month, day, year correctly."""
        input_file = tmp_path / "test_dates.dat"
        input_content = """\
C Comment
 h1
 h2
 h3
 h4
01/15/2000_24:00	1	100.0	200.0
12/31/1999_24:00	2	150.0	250.0
"""
        input_file.write_text(input_content)

        iwfm.lu2csv(str(input_file), skip=4)

        output_file = tmp_path / "test_dates.csv"
        with open(output_file, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)

        # First row: 01/15/2000
        assert rows[0][0] == '2000'  # year
        assert rows[0][1] == '01'    # month
        assert rows[0][2] == '15'    # day

        # Second row: 12/31/1999
        assert rows[1][0] == '1999'
        assert rows[1][1] == '12'
        assert rows[1][2] == '31'

    def test_skip_zero(self, tmp_path):
        """Test with skip=0 to process all non-comment lines."""
        input_file = tmp_path / "test_skip_zero.dat"
        input_content = """\
C Comment
09/30/1974_24:00	1	100.0	200.0
			2	150.0	250.0
"""
        input_file.write_text(input_content)

        iwfm.lu2csv(str(input_file), skip=0)

        output_file = tmp_path / "test_skip_zero.csv"
        with open(output_file, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)

        assert len(rows) == 2
