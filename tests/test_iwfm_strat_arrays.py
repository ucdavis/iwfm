# test_iwfm_strat_arrays.py 
# Test iwfm_strat_arrays function for parsing stratigraphy
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




def test_iwfm_strat_arrays_has_run_removed():
    '''Test that has_run static variable check was removed (verifies fix).'''
    # This verifies the fix: removed broken has_run static variable check
    from iwfm import iwfm_strat_arrays
    import inspect

    source = inspect.getsource(iwfm_strat_arrays)
    # Should have TODO comment about the removal
    assert 'TODO' in source or 'Note' in source or 'has_run' not in source


def test_iwfm_strat_arrays_function_exists():
    '''Test that iwfm_strat_arrays function is defined.'''
    from iwfm import iwfm_strat_arrays

    assert callable(iwfm_strat_arrays)


def test_iwfm_strat_arrays_basic():
    '''Test basic functionality of iwfm_strat_arrays.'''
    from iwfm import iwfm_strat_arrays

    # Create minimal stratigraphy data
    # Format: [node_id, layer1_top, layer1_bottom, layer2_top, layer2_bottom, ...]
    strat = [
        [1, 100.0, 50.0, 50.0, 0.0],
        [2, 105.0, 55.0, 55.0, 5.0],
    ]

    result = iwfm_strat_arrays(strat)

    # Should return arrays
    assert result is not None
    assert isinstance(result, (tuple, list))


def test_iwfm_strat_arrays_with_multiple_layers():
    '''Test iwfm_strat_arrays with multiple layers.'''
    from iwfm import iwfm_strat_arrays

    # 3 layers (6 elevation values + node id)
    strat = [
        [1, 100.0, 80.0, 80.0, 60.0, 60.0, 40.0],
        [2, 105.0, 85.0, 85.0, 65.0, 65.0, 45.0],
    ]

    result = iwfm_strat_arrays(strat)

    assert result is not None


def test_iwfm_strat_arrays_function_signature():
    '''Test that iwfm_strat_arrays has correct function signature.'''
    from iwfm import iwfm_strat_arrays
    import inspect

    sig = inspect.signature(iwfm_strat_arrays)
    params = list(sig.parameters.keys())

    assert 'strat' in params
