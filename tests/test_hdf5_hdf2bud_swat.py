# test_hdf5_hdf2bud_swat.py
# Tests for hdf5/hdf2bud_swat.py - Convert IWFM Small Watersheds Budget HDF5 to text format
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
import inspect


class TestHdf2budSwatImports:
    """Tests for hdf2bud_swat imports."""

    def test_import_from_hdf5(self):
        """Test import from iwfm.hdf5."""
        from iwfm.hdf5 import hdf2bud_swat
        assert callable(hdf2bud_swat)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.hdf5.hdf2bud_swat import hdf2bud_swat
        assert callable(hdf2bud_swat)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.hdf5.hdf2bud_swat import hdf2bud_swat

        assert hdf2bud_swat.__doc__ is not None
        assert 'watershed' in hdf2bud_swat.__doc__.lower() or 'hdf5' in hdf2bud_swat.__doc__.lower()


class TestHdf2budSwatSignature:
    """Tests for hdf2bud_swat function signature."""

    def test_function_signature(self):
        """Test that hdf2bud_swat has correct function signature."""
        from iwfm.hdf5.hdf2bud_swat import hdf2bud_swat

        sig = inspect.signature(hdf2bud_swat)
        params = list(sig.parameters.keys())

        # Required parameters
        assert 'hdf_file' in params
        assert 'output_file' in params

        # Optional parameters with defaults
        assert 'len_fact' in params
        assert 'len_units' in params
        assert 'area_fact' in params
        assert 'area_units' in params
        assert 'vol_fact' in params
        assert 'vol_units' in params
        assert 'verbose' in params
        assert 'debug' in params

    def test_default_len_fact(self):
        """Test that len_fact defaults to 1.0."""
        from iwfm.hdf5.hdf2bud_swat import hdf2bud_swat

        sig = inspect.signature(hdf2bud_swat)
        assert sig.parameters['len_fact'].default == 1.0

    def test_default_len_units(self):
        """Test that len_units defaults to FEET."""
        from iwfm.hdf5.hdf2bud_swat import hdf2bud_swat

        sig = inspect.signature(hdf2bud_swat)
        assert sig.parameters['len_units'].default == 'FEET'

    def test_default_area_fact(self):
        """Test that area_fact defaults to 0.000022957."""
        from iwfm.hdf5.hdf2bud_swat import hdf2bud_swat

        sig = inspect.signature(hdf2bud_swat)
        assert abs(sig.parameters['area_fact'].default - 0.000022957) < 1e-10

    def test_default_area_units(self):
        """Test that area_units defaults to AC."""
        from iwfm.hdf5.hdf2bud_swat import hdf2bud_swat

        sig = inspect.signature(hdf2bud_swat)
        assert sig.parameters['area_units'].default == 'AC'

    def test_default_vol_fact(self):
        """Test that vol_fact defaults to 0.000022957."""
        from iwfm.hdf5.hdf2bud_swat import hdf2bud_swat

        sig = inspect.signature(hdf2bud_swat)
        assert abs(sig.parameters['vol_fact'].default - 0.000022957) < 1e-10

    def test_default_vol_units(self):
        """Test that vol_units defaults to ACFT."""
        from iwfm.hdf5.hdf2bud_swat import hdf2bud_swat

        sig = inspect.signature(hdf2bud_swat)
        assert sig.parameters['vol_units'].default == 'ACFT'

    def test_default_verbose(self):
        """Test that verbose defaults to False."""
        from iwfm.hdf5.hdf2bud_swat import hdf2bud_swat

        sig = inspect.signature(hdf2bud_swat)
        assert sig.parameters['verbose'].default == False

    def test_default_debug(self):
        """Test that debug defaults to False."""
        from iwfm.hdf5.hdf2bud_swat import hdf2bud_swat

        sig = inspect.signature(hdf2bud_swat)
        assert sig.parameters['debug'].default == False


class TestHdf2budSwatDependencies:
    """Tests for hdf2bud_swat dependencies."""

    def test_h5py_available(self):
        """Test that h5py is available."""
        try:
            import h5py  # noqa: F401
            assert h5py is not None
        except ImportError:
            pytest.skip("h5py not available")

    def test_numpy_available(self):
        """Test that numpy is available."""
        import numpy as np
        assert np is not None

    def test_loguru_available(self):
        """Test that loguru is available."""
        try:
            from loguru import logger  # noqa: F401
            assert logger is not None
        except ImportError:
            pytest.skip("loguru not available")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
