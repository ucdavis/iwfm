# test_calib_get_hyd_names.py
# Unit tests for calib/get_hyd_names.py - Get hydrograph names from IWFM input file
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
from unittest.mock import patch


class TestGetHydNames:
    """Tests for get_hyd_names function"""

    def test_returns_list(self):
        """Test that function returns a list of hydrograph names."""
        from iwfm.calib.get_hyd_names import get_hyd_names

        with patch('iwfm.calib.get_hyd_info') as mock_get_hyd_info:
            mock_get_hyd_info.return_value = ('hyd.out', ['NAME_A', 'NAME_B', 'NAME_C'])
            
            result = get_hyd_names('Groundwater', {})
            
            assert isinstance(result, list)
            assert result == ['NAME_A', 'NAME_B', 'NAME_C']

    def test_returns_only_names_not_filename(self):
        """Test that only names are returned, not the filename."""
        from iwfm.calib.get_hyd_names import get_hyd_names

        with patch('iwfm.calib.get_hyd_info') as mock_get_hyd_info:
            mock_get_hyd_info.return_value = ('should_not_return.out', ['HYD_001'])
            
            result = get_hyd_names('Streams', {})
            
            assert result == ['HYD_001']
            assert 'should_not_return.out' not in result

    def test_calls_get_hyd_info(self):
        """Test that function calls get_hyd_info with correct arguments."""
        from iwfm.calib.get_hyd_names import get_hyd_names

        file_dict = {'Groundwater': ['gw.dat', 1, 2, 3]}
        
        with patch('iwfm.calib.get_hyd_info') as mock_get_hyd_info:
            mock_get_hyd_info.return_value = ('output.hyd', ['NAME1'])
            
            get_hyd_names('Groundwater', file_dict)
            
            mock_get_hyd_info.assert_called_once_with('Groundwater', file_dict)

    def test_verbose_output(self, capsys):
        """Test verbose output."""
        from iwfm.calib.get_hyd_names import get_hyd_names

        file_dict = {'Streams': ['streams.dat']}
        
        with patch('iwfm.calib.get_hyd_info') as mock_get_hyd_info:
            mock_get_hyd_info.return_value = ('hyd.out', ['S1', 'S2', 'S3'])
            
            get_hyd_names('Streams', file_dict, verbose=True)
            
            captured = capsys.readouterr()
            assert 'Reading' in captured.out
            assert 'Streams' in captured.out
            assert '3' in captured.out  # number of hydrographs

    def test_verbose_false_no_output(self, capsys):
        """Test that verbose=False produces no output."""
        from iwfm.calib.get_hyd_names import get_hyd_names

        with patch('iwfm.calib.get_hyd_info') as mock_get_hyd_info:
            mock_get_hyd_info.return_value = ('hyd.out', ['S1'])
            
            get_hyd_names('Groundwater', {}, verbose=False)
            
            captured = capsys.readouterr()
            assert captured.out == ''

    def test_empty_names_list(self):
        """Test with empty hydrograph names list."""
        from iwfm.calib.get_hyd_names import get_hyd_names

        with patch('iwfm.calib.get_hyd_info') as mock_get_hyd_info:
            mock_get_hyd_info.return_value = ('hyd.out', [])
            
            result = get_hyd_names('Groundwater', {})
            
            assert result == []

    def test_many_names(self):
        """Test with many hydrograph names."""
        from iwfm.calib.get_hyd_names import get_hyd_names

        names = [f'HYD_{i:04d}' for i in range(100)]
        
        with patch('iwfm.calib.get_hyd_info') as mock_get_hyd_info:
            mock_get_hyd_info.return_value = ('hyd.out', names)
            
            result = get_hyd_names('Groundwater', {})
            
            assert len(result) == 100
            assert result[0] == 'HYD_0000'
            assert result[99] == 'HYD_0099'

    def test_function_signature(self):
        """Test function has correct parameters."""
        from iwfm.calib.get_hyd_names import get_hyd_names
        import inspect
        
        sig = inspect.signature(get_hyd_names)
        params = list(sig.parameters.keys())
        
        assert 'ftype' in params
        assert 'file_dict' in params
        assert 'verbose' in params

    def test_verbose_default_false(self):
        """Test that verbose parameter defaults to False."""
        from iwfm.calib.get_hyd_names import get_hyd_names
        import inspect
        
        sig = inspect.signature(get_hyd_names)
        
        assert sig.parameters['verbose'].default == False


class TestGetHydNamesImports:
    """Tests for function imports."""

    def test_import_from_calib(self):
        """Test import from iwfm.calib."""
        from iwfm.calib import get_hyd_names
        assert callable(get_hyd_names)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.calib.get_hyd_names import get_hyd_names
        assert callable(get_hyd_names)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.calib.get_hyd_names import get_hyd_names
        
        assert get_hyd_names.__doc__ is not None
        assert 'hyd_names' in get_hyd_names.__doc__


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
