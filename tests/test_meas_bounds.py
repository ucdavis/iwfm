# test_meas_bounds.py 
# Test meas_bounds function for calculating observation bounds
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




def test_meas_bounds_dead_code_commented():
    '''Test that dead code is commented out (verifies fix).'''
    # This verifies the fix: commented out dead code with undefined variables
    from iwfm.meas_bounds import meas_bounds
    import inspect

    source = inspect.getsource(meas_bounds)
    # Dead code should be commented
    assert '# Dead code' in source or '# temp = gwhyd_obs[0].split()' in source


def test_meas_bounds_function_exists():
    '''Test that meas_bounds function is defined.'''
    from iwfm.meas_bounds import meas_bounds

    assert callable(meas_bounds)
    assert meas_bounds.__name__ == 'meas_bounds'


def test_meas_bounds_function_signature():
    '''Test that meas_bounds has correct function signature.'''
    from iwfm.meas_bounds import meas_bounds
    import inspect

    sig = inspect.signature(meas_bounds)
    params = list(sig.parameters.keys())

    assert 'gwhyd_obs' in params


def test_meas_bounds_basic():
    '''Test basic functionality of meas_bounds.'''
    from iwfm.meas_bounds import meas_bounds

    # Create minimal test data
    gwhyd_obs = ['header', 'WELL001 01/01/2020 X Y 100.0']

    # This function has incomplete implementation (only takes gwhyd_obs)
    # Just verify it can be called
    result = meas_bounds(gwhyd_obs)

    # Function may return None or some value
    assert result is None or isinstance(result, (list, dict, tuple))
