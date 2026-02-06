# test_gis_dd2dms.py
# Tests for gis/dd2dms.py - Convert decimal degrees to degree-minute-second
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


class TestDd2Dms:
    """Tests for dd2dms function."""

    def test_returns_string(self):
        """Test that function returns a string."""
        from iwfm.gis.dd2dms import dd2dms
        
        result = dd2dms(34.0522, -118.2437)
        
        assert isinstance(result, str)

    def test_contains_degrees_symbol(self):
        """Test that result contains degree symbol."""
        from iwfm.gis.dd2dms import dd2dms
        
        result = dd2dms(34.0522, -118.2437)
        
        assert 'º' in result or '°' in result

    def test_contains_compass_directions(self):
        """Test that result contains compass directions."""
        from iwfm.gis.dd2dms import dd2dms
        
        result = dd2dms(34.0522, -118.2437)
        
        # Should have N/S for latitude and E/W for longitude
        assert 'N' in result or 'S' in result
        assert 'E' in result or 'W' in result

    def test_northern_latitude(self):
        """Test northern latitude shows N."""
        from iwfm.gis.dd2dms import dd2dms
        
        result = dd2dms(34.0522, -118.2437)
        
        assert 'N' in result

    def test_southern_latitude(self):
        """Test southern latitude shows S."""
        from iwfm.gis.dd2dms import dd2dms
        
        result = dd2dms(-33.8688, 151.2093)  # Sydney
        
        assert 'S' in result

    def test_eastern_longitude(self):
        """Test eastern longitude shows E."""
        from iwfm.gis.dd2dms import dd2dms
        
        result = dd2dms(-33.8688, 151.2093)  # Sydney
        
        assert 'E' in result

    def test_western_longitude(self):
        """Test western longitude shows W."""
        from iwfm.gis.dd2dms import dd2dms
        
        result = dd2dms(34.0522, -118.2437)  # Los Angeles
        
        assert 'W' in result

    def test_whole_degrees(self):
        """Test with whole degree values."""
        from iwfm.gis.dd2dms import dd2dms
        
        result = dd2dms(45.0, -90.0)
        
        assert '45' in result
        assert '90' in result

    def test_zero_coordinates(self):
        """Test with zero coordinates (equator/prime meridian)."""
        from iwfm.gis.dd2dms import dd2dms
        
        result = dd2dms(0.0, 0.0)
        
        # Should handle zero without error
        assert isinstance(result, str)

    def test_contains_minutes_and_seconds(self):
        """Test that result contains minutes (') and seconds (\")."""
        from iwfm.gis.dd2dms import dd2dms
        
        result = dd2dms(34.5, -118.5)
        
        assert "'" in result
        assert '"' in result


class TestDd2DmsImports:
    """Tests for dd2dms imports."""

    def test_import_from_gis(self):
        """Test import from iwfm.gis."""
        from iwfm.gis import dd2dms
        assert callable(dd2dms)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.gis.dd2dms import dd2dms
        assert callable(dd2dms)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.gis.dd2dms import dd2dms
        
        assert dd2dms.__doc__ is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
