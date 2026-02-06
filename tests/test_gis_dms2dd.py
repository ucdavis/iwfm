# test_gis_dms2dd.py
# Tests for gis/dms2dd.py - Convert degree-minute-second to decimal degrees
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


class TestDms2Dd:
    """Tests for dms2dd function."""

    def test_returns_tuple(self):
        """Test that function returns a tuple."""
        from iwfm.gis.dms2dd import dms2dd
        
        result = dms2dd("34°3'11\"N", "118°14'37\"W")
        
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_returns_floats(self):
        """Test that function returns floats."""
        from iwfm.gis.dms2dd import dms2dd
        
        lat_dd, lon_dd = dms2dd("34°3'11\"N", "118°14'37\"W")
        
        assert isinstance(lat_dd, float)
        assert isinstance(lon_dd, float)

    def test_northern_latitude_positive(self):
        """Test that northern latitude is positive."""
        from iwfm.gis.dms2dd import dms2dd
        
        lat_dd, lon_dd = dms2dd("34°3'11\"N", "118°14'37\"W")
        
        assert lat_dd > 0

    def test_southern_latitude_negative(self):
        """Test that southern latitude is negative."""
        from iwfm.gis.dms2dd import dms2dd
        
        lat_dd, lon_dd = dms2dd("33°52'10\"S", "151°12'30\"E")
        
        assert lat_dd < 0

    def test_eastern_longitude_positive(self):
        """Test that eastern longitude is positive."""
        from iwfm.gis.dms2dd import dms2dd
        
        lat_dd, lon_dd = dms2dd("33°52'10\"S", "151°12'30\"E")
        
        assert lon_dd > 0

    def test_western_longitude_negative(self):
        """Test that western longitude is negative."""
        from iwfm.gis.dms2dd import dms2dd
        
        lat_dd, lon_dd = dms2dd("34°3'11\"N", "118°14'37\"W")
        
        assert lon_dd < 0

    def test_known_conversion(self):
        """Test with known DMS to DD conversion."""
        from iwfm.gis.dms2dd import dms2dd
        
        # 34° 3' 0" N = 34.05 DD
        lat_dd, lon_dd = dms2dd("34°3'0\"N", "118°15'0\"W")
        
        assert abs(lat_dd - 34.05) < 0.01
        assert abs(lon_dd - (-118.25)) < 0.01

    def test_whole_degrees(self):
        """Test with whole degrees (0 minutes, 0 seconds)."""
        from iwfm.gis.dms2dd import dms2dd
        
        lat_dd, lon_dd = dms2dd("45°0'0\"N", "90°0'0\"W")
        
        assert abs(lat_dd - 45.0) < 0.001
        assert abs(lon_dd - (-90.0)) < 0.001

    def test_invalid_format_raises_error(self):
        """Test that invalid format raises ValueError."""
        from iwfm.gis.dms2dd import dms2dd
        
        with pytest.raises(ValueError):
            dms2dd("invalid", "also invalid")


class TestDms2DdImports:
    """Tests for dms2dd imports."""

    def test_import_from_gis(self):
        """Test import from iwfm.gis."""
        from iwfm.gis import dms2dd
        assert callable(dms2dd)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.gis.dms2dd import dms2dd
        assert callable(dms2dd)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.gis.dms2dd import dms2dd
        
        assert dms2dd.__doc__ is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
