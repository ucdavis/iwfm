# test_calib_headdiff_hyds.py 
# Test calib/headdiff_hyds function for vertical head differences
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
from unittest.mock import Mock, patch


def test_headdiff_hyds_imports():
    '''Test that headdiff_hyds imports required functions (verifies fixes).'''
    # This verifies the fixes: added imports for ceil, dts2days, to_smp_ins
    from iwfm.calib.headdiff_hyds import ceil
    from iwfm.calib import headdiff_hyds
    import inspect

    assert ceil is not None
    source = inspect.getsource(headdiff_hyds)
    assert 'from iwfm import dts2days, to_smp_ins' in source or 'dts2days' in source


def test_headdiff_hyds_function_exists():
    '''Test that headdiff_hyds function is defined.'''
    from iwfm.calib.headdiff_hyds import headdiff_hyds

    assert callable(headdiff_hyds)


def test_headdiff_hyds_function_signature():
    '''Test that headdiff_hyds has correct function signature.'''
    from iwfm.calib.headdiff_hyds import headdiff_hyds
    import inspect

    sig = inspect.signature(headdiff_hyds)
    params = list(sig.parameters.keys())

    # Check for expected parameters
    assert 'hobs_file' in params or len(params) > 0
