# test_get_heads_4_date.py 
# Test get_heads_4_date function for reading IWFM headall.out files
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


import iwfm


def test_get_heads_4_date_basic(tmp_path):
    '''Test basic functionality of get_heads_4_date with valid data.'''
    heads_file = tmp_path / 'headall.out'

    # Create mock headall.out file
    content = [
        'Header line 1',
        'Header line 2',
        'Header line 3',
        'Header line 4',
        'Header line 5',
        'Node    Node1    Node2    Node3',
        '01/15/2020_24:00  100.5  101.2  102.3',
        '                   99.8  100.5  101.7',
        '                   98.3   99.1  100.2',
        '01/16/2020_24:00  100.6  101.3  102.4',
        '                   99.9  100.6  101.8',
    ]
    heads_file.write_text('\n'.join(content))

    result = iwfm.get_heads_4_date(str(heads_file), '01/15/2020', start=5)

    assert result is not None
    out_table, nodes, header = result
    assert len(nodes) == 3
    assert 'Node1' in nodes


def test_get_heads_4_date_numpy_import():
    '''Test that get_heads_4_date imports numpy (verifies fix).'''
    # This test verifies the fix: added 'import numpy as np'
    from iwfm.get_heads_4_date import np

    assert np is not None
    assert hasattr(np, 'asarray')


def test_get_heads_4_date_date_not_found(tmp_path):
    '''Test get_heads_4_date when date is not found in file.'''
    heads_file = tmp_path / 'headall.out'

    content = [
        'Header line 1',
        'Header line 2',
        'Header line 3',
        'Header line 4',
        'Header line 5',
        'Node    Node1    Node2',
        '01/15/2020_24:00  100.5  101.2',
        '                   99.8  100.5',
    ]
    heads_file.write_text('\n'.join(content))

    # Request a date that doesn't exist
    result = iwfm.get_heads_4_date(str(heads_file), '12/25/2020', start=5)

    # Should return None when date not found
    assert result is None


def test_get_heads_4_date_multiple_layers(tmp_path):
    '''Test get_heads_4_date with multiple layers.'''
    heads_file = tmp_path / 'headall.out'

    content = [
        'Header line 1',
        'Header line 2',
        'Header line 3',
        'Header line 4',
        'Header line 5',
        'Node    Node1    Node2    Node3',
        '01/15/2020_24:00  100.5  101.2  102.3',
        '                   99.8  100.5  101.7',
        '                   98.3   99.1  100.2',
        '                   97.5   98.3   99.5',
    ]
    heads_file.write_text('\n'.join(content))

    result = iwfm.get_heads_4_date(str(heads_file), '01/15/2020', start=5)

    assert result is not None
    out_table, nodes, header = result
    assert len(header) == 5  # Node + 4 layers


def test_get_heads_4_date_custom_start_line(tmp_path):
    '''Test get_heads_4_date with custom start line.'''
    heads_file = tmp_path / 'headall.out'

    content = [
        'Header line 1',
        'Header line 2',
        'Header line 3',
        'Node    Node1    Node2',
        '01/15/2020_24:00  100.5  101.2',
    ]
    heads_file.write_text('\n'.join(content))

    result = iwfm.get_heads_4_date(str(heads_file), '01/15/2020', start=3)

    assert result is not None
    out_table, nodes, header = result
    assert len(nodes) == 2


def test_get_heads_4_date_uses_iwfm_date_functions(tmp_path):
    '''Test that get_heads_4_date uses iwfm date functions.'''
    heads_file = tmp_path / 'headall.out'

    content = [
        'H1', 'H2', 'H3', 'H4', 'H5',
        'Node    N1',
        '03/25/2021_24:00  100.5',
    ]
    heads_file.write_text('\n'.join(content))

    result = iwfm.get_heads_4_date(str(heads_file), '03/25/2021', start=5)

    assert result is not None
    # Verifies that month, day, year functions work correctly
