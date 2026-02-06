# test_gis_method_fns.py 
# Test gis/method_fns function for listing shapefile methods
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


from unittest.mock import Mock


def test_method_fns_imports():
    '''Test that method_fns imports getmembers from inspect (verifies fix).'''
    # This verifies the fix: added 'from inspect import getmembers'
    from iwfm.gis.method_fns import getmembers

    assert getmembers is not None


def test_method_fns_basic():
    '''Test basic functionality of method_fns.'''
    from iwfm.gis.method_fns import method_fns

    # Create a mock shapefile object
    mock_shp = Mock()
    mock_shp.test_method = lambda: None
    mock_shp.another_method = lambda: None

    result = method_fns('test.shp', mock_shp)

    # Should return list of methods
    assert isinstance(result, list)


def test_method_fns_function_signature():
    '''Test that method_fns has correct function signature.'''
    from iwfm.gis.method_fns import method_fns
    import inspect

    sig = inspect.signature(method_fns)
    params = list(sig.parameters.keys())

    assert 'shpfile' in params
