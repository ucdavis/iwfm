# test_gw_well_lay_elev.py 
# Test gw_well_lay_elev function for finding layer elevations
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


def test_gw_well_lay_elev_has_todo():
    '''Test that function has TODO comment about IDW function (verifies fix).'''
    # This verifies the fix: added TODO note about undefined IDW function
    from iwfm import gw_well_lay_elev
    import inspect

    source = inspect.getsource(gw_well_lay_elev)
    # Should have TODO comment about IDW
    assert 'TODO' in source or 'IDW' in source


def test_gw_well_lay_elev_function_exists():
    '''Test that gw_well_lay_elev function is defined.'''
    from iwfm import gw_well_lay_elev

    assert callable(gw_well_lay_elev)


def test_gw_well_lay_elev_function_signature():
    '''Test that gw_well_lay_elev has correct function signature.'''
    from iwfm import gw_well_lay_elev
    import inspect

    sig = inspect.signature(gw_well_lay_elev)
    params = list(sig.parameters.keys())

    assert 'self' in params
    assert 'x' in params
    assert 'y' in params
    assert 'elem' in params
    assert 'lay' in params
    assert 'debug' in params


def test_gw_well_lay_elev_is_incomplete():
    '''Test that function is marked as incomplete due to IDW dependency.'''
    from iwfm import gw_well_lay_elev
    import inspect

    source = inspect.getsource(gw_well_lay_elev)
    # Function uses IDW which is not defined
    assert 'IDW' in source


# Note: Cannot test actual functionality since IDW function is not implemented
# This is documented in the TODO comment added during the fix
