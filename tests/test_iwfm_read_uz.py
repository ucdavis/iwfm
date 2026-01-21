#!/usr/bin/env python
# test_iwfm_read_uz.py
# Unit tests for iwfm_read_uz.py
# Copyright (C) 2020-2026 University of California
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
import tempfile
import os


class TestIwfmReadUz:
    """Tests for iwfm_read_uz function"""

    def test_basic_structure_with_parameter_grid(self):
        """Test reading unsaturated zone file with parameter grid"""
        content = "C IWFM Unsaturated Zone File\n"
        content += "#4.2\n"
        content += " 3\n"
        content += " 0.001\n"
        content += " 50\n"
        content += " Budget.hdf\n"
        content += " ZBudget.hdf\n"
        content += " FinalCond.out\n"
        content += " 4\n"
        content += " 1.0 2.0 3.0\n"
        content += " 1MON\n"
        content += "C Parameter Grid Data\n"
        content += " 10\n"
        content += " 5\n"
        content += " 1 2 3 4\n"
        content += " 2 3 4 5\n"
        content += " 3 4 5 6\n"
        content += " 4 5 6 7\n"
        content += " 5 6 7 8\n"
        content += "C Parameter values\n"
        # 10 nodes, 3 layers each
        for node in range(1, 11):
            for layer in range(3):
                if layer == 0:
                    content += f" {node}  {node*10}  {node*20}  1.0  0.3  0.2  0.5  0.1\n"
                else:
                    content += f" 1.5  0.35  0.25  0.6  0.15\n"
        content += "C Initial Conditions\n"
        content += " 1  0.5  0.6  0.7\n"
        content += " 2  0.5  0.6  0.7\n"
        content += "\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_uz import iwfm_read_uz

            uz_dict, params = iwfm_read_uz(temp_file, verbose=False)

            # Verify dictionary
            assert uz_dict['bud'] == 'Budget.hdf'
            assert uz_dict['zbud'] == 'ZBudget.hdf'
            assert uz_dict['fcond'] == 'FinalCond.out'

            # Verify params structure: [pd, pn, pi, pk, prhc, ic]
            assert len(params) == 6

            # Check parameter arrays
            pd, pn, pi, pk, prhc, ic = params
            assert len(pd) == 10  # 10 nodes
            assert len(pd[0]) == 3  # 3 layers

        finally:
            os.unlink(temp_file)

    def test_basic_structure_without_parameter_grid(self):
        """Test reading unsaturated zone file without parameter grid (ngroup=0)"""
        content = "C IWFM Unsaturated Zone File\n"
        content += "#4.2\n"
        content += " 2\n"
        content += " 0.001\n"
        content += " 50\n"
        content += " Budget.hdf\n"
        content += " ZBudget.hdf\n"
        content += " FinalCond.out\n"
        content += " 0\n"
        content += " 1.0 2.0 3.0\n"
        content += " 1MON\n"
        content += "C Parameter values\n"
        content += " 1  1.0  0.3  0.2  0.5  0.1  1.5  0.35  0.25  0.6  0.15\n"
        content += " 2  1.0  0.3  0.2  0.5  0.1  1.5  0.35  0.25  0.6  0.15\n"
        content += "C Initial Conditions\n"
        content += " 1  0.5  0.6\n"
        content += " 2  0.5  0.6\n"
        content += "\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_uz import iwfm_read_uz

            uz_dict, params = iwfm_read_uz(temp_file, verbose=False)

            # Verify dictionary
            assert uz_dict['bud'] == 'Budget.hdf'
            assert uz_dict['zbud'] == 'ZBudget.hdf'
            assert uz_dict['fcond'] == 'FinalCond.out'

            # Verify params structure
            assert len(params) == 6

            # Check parameter arrays
            pd, pn, pi, pk, prhc, ic = params
            assert len(pd) == 2  # 2 elements
            assert len(pd[0]) == 2  # 2 layers

        finally:
            os.unlink(temp_file)

    def test_return_structure(self):
        """Test that function returns correct tuple structure"""
        content = "C IWFM Unsaturated Zone File\n"
        content += "#4.2\n"
        content += " 1\n"
        content += " 0.001\n"
        content += " 50\n"
        content += " Budget.hdf\n"
        content += " ZBudget.hdf\n"
        content += " FinalCond.out\n"
        content += " 0\n"
        content += " 1.0 2.0 3.0\n"
        content += " 1MON\n"
        content += " 1  1.0  0.3  0.2  0.5  0.1\n"
        content += "C Initial Conditions\n"
        content += " 1  0.5\n"
        content += "\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_uz import iwfm_read_uz

            result = iwfm_read_uz(temp_file, verbose=False)

            # Verify return is tuple of 2 elements
            assert isinstance(result, tuple)
            assert len(result) == 2

            uz_dict, params = result

            # Verify types
            assert isinstance(uz_dict, dict)
            assert isinstance(params, list)
            assert len(params) == 6

        finally:
            os.unlink(temp_file)

    def test_comment_lines_skipped(self):
        """Test that comment lines are properly skipped"""
        content = "C IWFM Unsaturated Zone File\n"
        content += "c This is a comment\n"
        content += "* Another comment\n"
        content += "#4.2\n"
        content += "# Comment\n"
        content += " 1\n"
        content += "C More comments\n"
        content += " 0.001\n"
        content += " 50\n"
        content += " Budget.hdf\n"
        content += " ZBudget.hdf\n"
        content += " FinalCond.out\n"
        content += " 0\n"
        content += " 1.0 2.0 3.0\n"
        content += " 1MON\n"
        content += " 1  1.0  0.3  0.2  0.5  0.1\n"
        content += "C Initial Conditions\n"
        content += " 1  0.5\n"
        content += "\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_uz import iwfm_read_uz

            uz_dict, params = iwfm_read_uz(temp_file, verbose=False)

            # Should read correctly despite comment lines
            assert uz_dict['bud'] == 'Budget.hdf'
            assert uz_dict['zbud'] == 'ZBudget.hdf'

        finally:
            os.unlink(temp_file)

    def test_no_file_names(self):
        """Test handling of missing optional file names"""
        content = "C IWFM Unsaturated Zone File\n"
        content += "#4.2\n"
        content += " 1\n"
        content += " 0.001\n"
        content += " 50\n"
        content += " /\n"
        content += " /\n"
        content += " /\n"
        content += " 0\n"
        content += " 1.0 2.0 3.0\n"
        content += " 1MON\n"
        content += " 1  1.0  0.3  0.2  0.5  0.1\n"
        content += "C Initial Conditions\n"
        content += " 1  0.5\n"
        content += "\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_uz import iwfm_read_uz

            uz_dict, params = iwfm_read_uz(temp_file, verbose=False)

            # Verify missing files are marked as 'none'
            assert uz_dict['bud'] == 'none'
            assert uz_dict['zbud'] == 'none'
            assert uz_dict['fcond'] == 'none'

        finally:
            os.unlink(temp_file)

    def test_multiple_layers(self):
        """Test reading file with multiple unsaturated zone layers"""
        content = "C IWFM Unsaturated Zone File\n"
        content += "#4.2\n"
        content += " 4\n"
        content += " 0.001\n"
        content += " 50\n"
        content += " Budget.hdf\n"
        content += " ZBudget.hdf\n"
        content += " FinalCond.out\n"
        content += " 0\n"
        content += " 1.0 2.0 3.0\n"
        content += " 1MON\n"
        # Element with 4 layers: elem_id, then 5 params * 4 layers = 20 params
        content += " 1  1.0 0.3 0.2 0.5 0.1  1.5 0.35 0.25 0.6 0.15  2.0 0.4 0.3 0.7 0.2  2.5 0.45 0.35 0.8 0.25\n"
        content += "C Initial Conditions\n"
        content += " 1  0.5  0.6  0.7  0.8\n"
        content += "\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_uz import iwfm_read_uz

            uz_dict, params = iwfm_read_uz(temp_file, verbose=False)

            # Verify params structure
            pd, pn, pi, pk, prhc, ic = params
            assert len(pd) == 1  # 1 element
            assert len(pd[0]) == 4  # 4 layers

            # Verify layer values
            assert pd[0][0] == 1.0
            assert pd[0][1] == 1.5
            assert pd[0][2] == 2.0
            assert pd[0][3] == 2.5

        finally:
            os.unlink(temp_file)

    def test_initial_conditions_ie_zero(self):
        """Test reading initial conditions with IE=0 (all elements same)"""
        content = "C IWFM Unsaturated Zone File\n"
        content += "#4.2\n"
        content += " 2\n"
        content += " 0.001\n"
        content += " 50\n"
        content += " Budget.hdf\n"
        content += " ZBudget.hdf\n"
        content += " FinalCond.out\n"
        content += " 0\n"
        content += " 1.0 2.0 3.0\n"
        content += " 1MON\n"
        content += " 1  1.0  0.3  0.2  0.5  0.1  1.5  0.35  0.25  0.6  0.15\n"
        content += " 2  1.0  0.3  0.2  0.5  0.1  1.5  0.35  0.25  0.6  0.15\n"
        content += "C Initial Conditions\n"
        content += " 0  0.5  0.6\n"
        content += "\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_uz import iwfm_read_uz

            uz_dict, params = iwfm_read_uz(temp_file, verbose=False)

            # Verify IC with IE=0 format
            pd, pn, pi, pk, prhc, ic = params

            # IC should be a list starting with 0 (indicating all elements use same values)
            assert isinstance(ic, list)
            assert ic[0] == 0
            assert ic[1] == 0.5
            assert ic[2] == 0.6

        finally:
            os.unlink(temp_file)

    def test_verbose_mode(self):
        """Test verbose mode output"""
        content = "C IWFM Unsaturated Zone File\n"
        content += "#4.2\n"
        content += " 1\n"
        content += " 0.001\n"
        content += " 50\n"
        content += " Budget.hdf\n"
        content += " ZBudget.hdf\n"
        content += " FinalCond.out\n"
        content += " 0\n"
        content += " 1.0 2.0 3.0\n"
        content += " 1MON\n"
        content += " 1  1.0  0.3  0.2  0.5  0.1\n"
        content += "C Initial Conditions\n"
        content += " 1  0.5\n"
        content += "\n"

        with tempfile.NamedTemporaryFile(mode='w', suffix='.dat', delete=False) as f:
            f.write(content)
            temp_file = f.name

        try:
            from iwfm.iwfm_read_uz import iwfm_read_uz
            import io
            import sys

            # Capture stdout
            captured_output = io.StringIO()
            sys.stdout = captured_output

            uz_dict, params = iwfm_read_uz(temp_file, verbose=True)

            # Restore stdout
            sys.stdout = sys.__stdout__

            output = captured_output.getvalue()
            assert "Entered iwfm_read_uz()" in output
            assert "Leaving iwfm_read_uz()" in output

        finally:
            os.unlink(temp_file)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
