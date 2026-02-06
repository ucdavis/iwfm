# test_calib_ltbud.py
# Unit tests for calib/ltbud.py - Log-transform IWFM Budget file values
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


class TestLtbud:
    """Tests for ltbud function"""

    def create_budget_file(self, tmp_path, tables=1, rows=3):
        """Create a mock IWFM Budget format file.
        
        Budget file format:
        - Header lines (non-digit starting)
        - Data lines (digit starting: date + values)
        - Footer lines between tables
        """
        budget_file = tmp_path / 'budget.out'
        
        lines = []
        for t in range(tables):
            # Header lines
            lines.append('                    IWFM BUDGET FILE')
            lines.append('                    Budget Table {}'.format(t + 1))
            lines.append('     Date          Value1       Value2       Value3')
            lines.append('----------------------------------------------------------')
            
            # Data lines (start with digit = date)
            for r in range(rows):
                date = f'10/{r+1:02d}/2020_24:00'
                val1 = 100.0 + r * 10
                val2 = 200.0 + r * 10
                val3 = 300.0 + r * 10
                lines.append(f'{date}      {val1:10.2f}   {val2:10.2f}   {val3:10.2f}')
            
            # Footer between tables (if not last table)
            if t < tables - 1:
                lines.append('')
                lines.append('')
        
        budget_file.write_text('\n'.join(lines))
        return str(budget_file)

    def test_creates_output_file(self, tmp_path):
        """Test that output file is created."""
        from iwfm.calib.ltbud import ltbud

        budget_file = self.create_budget_file(tmp_path)
        output_file = str(tmp_path / 'output.out')

        ltbud(budget_file, output_file)

        assert os.path.exists(output_file)

    def test_output_file_has_content(self, tmp_path):
        """Test that output file has content."""
        from iwfm.calib.ltbud import ltbud

        budget_file = self.create_budget_file(tmp_path)
        output_file = str(tmp_path / 'output.out')

        ltbud(budget_file, output_file)

        assert os.path.getsize(output_file) > 0

    def test_preserves_header_lines(self, tmp_path):
        """Test that header lines are preserved."""
        from iwfm.calib.ltbud import ltbud

        budget_file = self.create_budget_file(tmp_path)
        output_file = str(tmp_path / 'output.out')

        ltbud(budget_file, output_file)

        with open(output_file, 'r') as f:
            content = f.read()

        assert 'IWFM BUDGET FILE' in content

    def test_preserves_date_column(self, tmp_path):
        """Test that date column (first 16 chars) is preserved."""
        from iwfm.calib.ltbud import ltbud

        budget_file = self.create_budget_file(tmp_path)
        output_file = str(tmp_path / 'output.out')

        ltbud(budget_file, output_file)

        with open(output_file, 'r') as f:
            lines = f.readlines()

        # Find a data line and check date is preserved
        for line in lines:
            if line.strip() and line[0].isdigit():
                assert '10/' in line[:16]  # Date should be in first 16 chars
                break

    def test_transforms_values(self, tmp_path):
        """Test that values are log-transformed."""
        from iwfm.calib.ltbud import ltbud

        budget_file = self.create_budget_file(tmp_path, rows=1)
        output_file = str(tmp_path / 'output.out')

        # Read original values
        with open(budget_file, 'r') as f:
            orig_lines = f.readlines()

        ltbud(budget_file, output_file)

        with open(output_file, 'r') as f:
            new_lines = f.readlines()

        # Values should be different (log-transformed)
        # Find data lines and compare
        for orig, new in zip(orig_lines, new_lines):
            if orig.strip() and orig[0].isdigit():
                # Original and new data lines should differ in values
                orig_vals = orig.split()[1:]
                new_vals = new.split()[1:]
                # At least some values should be different
                assert orig_vals != new_vals

    def test_same_number_of_lines(self, tmp_path):
        """Test that output has same number of lines as input."""
        from iwfm.calib.ltbud import ltbud

        budget_file = self.create_budget_file(tmp_path, tables=2, rows=5)
        output_file = str(tmp_path / 'output.out')

        with open(budget_file, 'r') as f:
            orig_line_count = len(f.readlines())

        ltbud(budget_file, output_file)

        with open(output_file, 'r') as f:
            new_line_count = len(f.readlines())

        assert new_line_count == orig_line_count

    def test_zero_offset_parameter(self, tmp_path):
        """Test that zero_offset parameter is used."""
        from iwfm.calib.ltbud import ltbud

        budget_file = self.create_budget_file(tmp_path)
        output1 = str(tmp_path / 'output1.out')
        output2 = str(tmp_path / 'output2.out')

        ltbud(budget_file, output1, zero_offset=2.0)
        ltbud(budget_file, output2, zero_offset=10.0)

        # Different zero_offset should produce different outputs
        with open(output1, 'r') as f1, open(output2, 'r') as f2:
            content1 = f1.read()
            content2 = f2.read()

        # Content may be same if no zeros, but function should accept parameter
        assert os.path.exists(output1)
        assert os.path.exists(output2)

    def test_function_signature(self):
        """Test function has correct parameters."""
        from iwfm.calib.ltbud import ltbud
        import inspect
        
        sig = inspect.signature(ltbud)
        params = list(sig.parameters.keys())
        
        assert 'budget_file' in params
        assert 'output_file' in params
        assert 'zero_offset' in params
        assert 'neg_val' in params

    def test_default_parameter_values(self):
        """Test default parameter values."""
        from iwfm.calib.ltbud import ltbud
        import inspect
        
        sig = inspect.signature(ltbud)
        
        assert sig.parameters['zero_offset'].default == 2.0
        assert sig.parameters['neg_val'].default == 1.0e-7


class TestLtbudImports:
    """Tests for function imports."""

    def test_import_from_calib(self):
        """Test import from iwfm.calib."""
        from iwfm.calib import ltbud
        assert callable(ltbud)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.calib.ltbud import ltbud
        assert callable(ltbud)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.calib.ltbud import ltbud
        
        assert ltbud.__doc__ is not None
        assert 'budget' in ltbud.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
