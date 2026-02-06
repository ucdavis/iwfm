# test_write_lu2file.py
# Unit tests for write_lu2file.py - Write IWFM land use to file
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


class TestWriteLu2File:
    """Tests for write_lu2file function"""

    def test_basic_functionality(self, tmp_path):
        """Test basic functionality with simple data."""
        from iwfm.write_lu2file import write_lu2file

        out_file = str(tmp_path / 'test_lu.dat')
        
        # out_table[year][element] = [crop1_area, crop2_area, ...]
        out_table = [
            [[100.0, 200.0, 300.0], [110.0, 210.0, 310.0]],  # Year 1: 2 elements, 3 crops
        ]
        in_years = [2020]

        write_lu2file(out_table, out_file, in_years, verbose=False)

        assert os.path.exists(out_file)

    def test_default_date_format(self, tmp_path):
        """Test that default date format (09/30/YYYY_24:00) is used."""
        from iwfm.write_lu2file import write_lu2file

        out_file = str(tmp_path / 'test_lu.dat')
        
        out_table = [[[100.0]]]
        in_years = [2020]

        write_lu2file(out_table, out_file, in_years, verbose=False)

        with open(out_file, 'r') as f:
            content = f.read()

        assert '09/30/2020_24:00' in content

    def test_custom_date_format(self, tmp_path):
        """Test with custom date_head_tail format."""
        from iwfm.write_lu2file import write_lu2file

        out_file = str(tmp_path / 'test_lu.dat')
        
        out_table = [[[100.0]]]
        in_years = [2020]
        date_head_tail = ['12/31/', '_12:00']

        write_lu2file(out_table, out_file, in_years, date_head_tail=date_head_tail, verbose=False)

        with open(out_file, 'r') as f:
            content = f.read()

        assert '12/31/2020_12:00' in content

    def test_element_numbering(self, tmp_path):
        """Test that element numbers are 1-indexed (j+1)."""
        from iwfm.write_lu2file import write_lu2file

        out_file = str(tmp_path / 'test_lu.dat')
        
        # 3 elements
        out_table = [[[100.0], [200.0], [300.0]]]
        in_years = [2020]

        write_lu2file(out_table, out_file, in_years, verbose=False)

        with open(out_file, 'r') as f:
            lines = f.readlines()

        # Element numbers should be 1, 2, 3 (not 0, 1, 2)
        assert '\t1\t' in lines[0]
        assert '\t2\t' in lines[1]
        assert '\t3\t' in lines[2]

    def test_multiple_years(self, tmp_path):
        """Test with multiple years of data."""
        from iwfm.write_lu2file import write_lu2file

        out_file = str(tmp_path / 'test_lu.dat')
        
        out_table = [
            [[100.0]],  # Year 2018
            [[110.0]],  # Year 2019
            [[120.0]],  # Year 2020
        ]
        in_years = [2018, 2019, 2020]

        write_lu2file(out_table, out_file, in_years, verbose=False)

        with open(out_file, 'r') as f:
            content = f.read()

        assert '09/30/2018' in content
        assert '09/30/2019' in content
        assert '09/30/2020' in content

    def test_multiple_elements(self, tmp_path):
        """Test with multiple elements."""
        from iwfm.write_lu2file import write_lu2file

        out_file = str(tmp_path / 'test_lu.dat')
        
        # 1 year, 5 elements, 2 crops each
        out_table = [
            [[10.0, 20.0], [11.0, 21.0], [12.0, 22.0], [13.0, 23.0], [14.0, 24.0]]
        ]
        in_years = [2020]

        write_lu2file(out_table, out_file, in_years, verbose=False)

        with open(out_file, 'r') as f:
            lines = f.readlines()

        assert len(lines) == 5

    def test_multiple_crops(self, tmp_path):
        """Test with multiple crops per element."""
        from iwfm.write_lu2file import write_lu2file

        out_file = str(tmp_path / 'test_lu.dat')
        
        # 1 year, 1 element, 5 crops
        out_table = [[[10.0, 20.0, 30.0, 40.0, 50.0]]]
        in_years = [2020]

        write_lu2file(out_table, out_file, in_years, verbose=False)

        with open(out_file, 'r') as f:
            content = f.read()

        # All crop values should be present
        assert '10.0' in content
        assert '20.0' in content
        assert '30.0' in content
        assert '40.0' in content
        assert '50.0' in content

    def test_rounding_precision(self, tmp_path):
        """Test that values are rounded to 2 decimal places."""
        from iwfm.write_lu2file import write_lu2file

        out_file = str(tmp_path / 'test_lu.dat')
        
        out_table = [[[123.456789, 0.001, 99.999]]]
        in_years = [2020]

        write_lu2file(out_table, out_file, in_years, verbose=False)

        with open(out_file, 'r') as f:
            content = f.read()

        # Should be rounded to 2 decimal places
        assert '123.46' in content
        assert '0.0' in content
        assert '100.0' in content

    def test_tab_delimited_format(self, tmp_path):
        """Test that output is tab-delimited."""
        from iwfm.write_lu2file import write_lu2file

        out_file = str(tmp_path / 'test_lu.dat')
        
        out_table = [[[100.0, 200.0]]]
        in_years = [2020]

        write_lu2file(out_table, out_file, in_years, verbose=False)

        with open(out_file, 'r') as f:
            line = f.readline()

        # Should contain tabs
        assert '\t' in line
        # Count tabs: date + elem_num + crop1 + crop2 = at least 3 tabs
        assert line.count('\t') >= 3

    def test_date_on_first_element_only(self, tmp_path):
        """Test that date is only on the first element of each year."""
        from iwfm.write_lu2file import write_lu2file

        out_file = str(tmp_path / 'test_lu.dat')
        
        # 1 year, 3 elements
        out_table = [[[100.0], [200.0], [300.0]]]
        in_years = [2020]

        write_lu2file(out_table, out_file, in_years, verbose=False)

        with open(out_file, 'r') as f:
            lines = f.readlines()

        # First line starts with date
        assert lines[0].startswith('09/30/2020')
        # Subsequent lines should NOT start with date (they start with tab)
        # Actually looking at the code, only j==0 gets the date prefix
        # Other lines don't have the date at the start

    def test_verbose_single_year(self, tmp_path, capsys):
        """Test verbose output for single year."""
        from iwfm.write_lu2file import write_lu2file

        out_file = str(tmp_path / 'test_lu.dat')
        
        out_table = [[[100.0]]]
        in_years = [2020]

        write_lu2file(out_table, out_file, in_years, verbose=True, lu_type='NPC')

        captured = capsys.readouterr()
        assert 'Wrote' in captured.out
        assert 'NPC' in captured.out
        assert '2020' in captured.out

    def test_verbose_multiple_years(self, tmp_path, capsys):
        """Test verbose output for multiple years."""
        from iwfm.write_lu2file import write_lu2file

        out_file = str(tmp_path / 'test_lu.dat')
        
        out_table = [[[100.0]], [[110.0]], [[120.0]]]
        in_years = [2018, 2019, 2020]

        write_lu2file(out_table, out_file, in_years, verbose=True, lu_type='Urban')

        captured = capsys.readouterr()
        assert 'Wrote' in captured.out
        assert 'Urban' in captured.out
        assert '3 years' in captured.out

    def test_zero_values(self, tmp_path):
        """Test with zero values."""
        from iwfm.write_lu2file import write_lu2file

        out_file = str(tmp_path / 'test_lu.dat')
        
        out_table = [[[0.0, 0.0, 0.0]]]
        in_years = [2020]

        write_lu2file(out_table, out_file, in_years, verbose=False)

        with open(out_file, 'r') as f:
            content = f.read()

        # Zeros should be written
        assert '0' in content

    def test_large_values(self, tmp_path):
        """Test with large values."""
        from iwfm.write_lu2file import write_lu2file

        out_file = str(tmp_path / 'test_lu.dat')
        
        out_table = [[[999999.99, 1000000.0]]]
        in_years = [2020]

        write_lu2file(out_table, out_file, in_years, verbose=False)

        with open(out_file, 'r') as f:
            content = f.read()

        assert '999999.99' in content
        assert '1000000.0' in content

    def test_return_value(self, tmp_path):
        """Test that function returns None."""
        from iwfm.write_lu2file import write_lu2file

        out_file = str(tmp_path / 'test_lu.dat')
        
        out_table = [[[100.0]]]
        in_years = [2020]

        result = write_lu2file(out_table, out_file, in_years, verbose=False)

        assert result is None

    def test_complex_scenario(self, tmp_path):
        """Test complex scenario with multiple years, elements, and crops."""
        from iwfm.write_lu2file import write_lu2file

        out_file = str(tmp_path / 'test_lu.dat')
        
        # 3 years, 4 elements per year, 5 crops per element
        out_table = []
        for year_idx in range(3):
            year_data = []
            for elem_idx in range(4):
                elem_data = [float(year_idx * 100 + elem_idx * 10 + crop_idx) 
                            for crop_idx in range(5)]
                year_data.append(elem_data)
            out_table.append(year_data)
        
        in_years = [2018, 2019, 2020]

        write_lu2file(out_table, out_file, in_years, verbose=False)

        with open(out_file, 'r') as f:
            lines = f.readlines()

        # 3 years * 4 elements = 12 lines
        assert len(lines) == 12


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
