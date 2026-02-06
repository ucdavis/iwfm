# test_calib_get_hyd_fname.py
# Unit tests for calib/get_hyd_fname.py - Get hydrograph file name from IWFM file
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


class TestGetHydFname:
    """Tests for get_hyd_fname function"""

    def test_returns_string(self):
        """Test that function returns a string (file name)."""
        from iwfm.calib.get_hyd_fname import get_hyd_fname

        # Mock get_hyd_info to return expected values
        with patch('iwfm.calib.get_hyd_info') as mock_get_hyd_info:
            mock_get_hyd_info.return_value = ('test_hyd.out', ['HYD_001', 'HYD_002'])
            
            result = get_hyd_fname('Groundwater', {})
            
            assert isinstance(result, str)
            assert result == 'test_hyd.out'

    def test_calls_get_hyd_info(self):
        """Test that function calls get_hyd_info with correct arguments."""
        from iwfm.calib.get_hyd_fname import get_hyd_fname

        file_dict = {'Groundwater': ['gw.dat', 1, 2, 3]}
        
        with patch('iwfm.calib.get_hyd_info') as mock_get_hyd_info:
            mock_get_hyd_info.return_value = ('output.hyd', ['NAME1'])
            
            get_hyd_fname('Groundwater', file_dict)
            
            mock_get_hyd_info.assert_called_once_with('Groundwater', file_dict)

    def test_returns_only_filename_not_names(self):
        """Test that only the filename is returned, not the hydrograph names."""
        from iwfm.calib.get_hyd_fname import get_hyd_fname

        with patch('iwfm.calib.get_hyd_info') as mock_get_hyd_info:
            mock_get_hyd_info.return_value = ('myfile.out', ['A', 'B', 'C', 'D'])
            
            result = get_hyd_fname('Streams', {})
            
            # Should return only the filename
            assert result == 'myfile.out'
            assert not isinstance(result, tuple)

    def test_function_signature(self):
        """Test function has correct parameters."""
        from iwfm.calib.get_hyd_fname import get_hyd_fname
        import inspect
        
        sig = inspect.signature(get_hyd_fname)
        params = list(sig.parameters.keys())
        
        assert 'ftype' in params
        assert 'file_dict' in params
        assert 'debug' in params

    def test_debug_default_value(self):
        """Test that debug parameter defaults to 0."""
        from iwfm.calib.get_hyd_fname import get_hyd_fname
        import inspect
        
        sig = inspect.signature(get_hyd_fname)
        
        assert sig.parameters['debug'].default == 0


class TestGetHydFnameImports:
    """Tests for function imports."""

    def test_import_from_calib(self):
        """Test import from iwfm.calib."""
        from iwfm.calib import get_hyd_fname
        assert callable(get_hyd_fname)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.calib.get_hyd_fname import get_hyd_fname
        assert callable(get_hyd_fname)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
