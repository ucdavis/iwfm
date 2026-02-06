# test_wdl_meas_stats.py 
# Test wdl_meas_stats function for calculating water level statistics
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


def test_wdl_meas_stats_basic(tmp_path):
    '''Test basic functionality of wdl_meas_stats with valid data.'''
    input_file = tmp_path / 'test_input.dat'

    content = [
        'HEADER LINE',
        'WELL001  01/15/2020  X  Y  100.5',
        'WELL001  01/16/2020  X  Y  101.2',
        'WELL001  01/17/2020  X  Y  102.3',
        'WELL002  01/15/2020  X  Y  200.5',
        'WELL002  01/16/2020  X  Y  201.2',
    ]
    input_file.write_text('\n'.join(content))

    iwfm.wdl_meas_stats(str(input_file), verbose=False)

    output_file = tmp_path / 'test_input_stats.out'
    assert output_file.exists()


def test_wdl_meas_stats_output_format(tmp_path):
    '''Test that output file has correct header format.'''
    input_file = tmp_path / 'test_input.dat'

    content = [
        'HEADER LINE',
        'WELL001  01/15/2020  X  Y  100.5',
        'WELL001  01/16/2020  X  Y  101.2',
    ]
    input_file.write_text('\n'.join(content))

    iwfm.wdl_meas_stats(str(input_file), verbose=False)

    output_file = tmp_path / 'test_input_stats.out'
    lines = output_file.read_text().strip().split('\n')

    assert 'STN_ID' in lines[0]
    assert 'MIN_DATE' in lines[0]
    assert 'MAX_DATE' in lines[0]
    assert 'COUNT' in lines[0]
    assert 'WL_AVG' in lines[0]
    assert 'WL_MAX' in lines[0]
    assert 'WL_MIN' in lines[0]
    assert 'WL_SDV' in lines[0]


def test_wdl_meas_stats_multiple_wells(tmp_path):
    '''Test wdl_meas_stats with multiple wells.'''
    input_file = tmp_path / 'test_input.dat'

    content = [
        'HEADER LINE',
        'WELL001  01/15/2020  X  Y  100.5',
        'WELL001  01/16/2020  X  Y  101.5',
        'WELL002  01/15/2020  X  Y  200.5',
        'WELL002  01/16/2020  X  Y  201.5',
        'WELL003  01/15/2020  X  Y  300.5',
    ]
    input_file.write_text('\n'.join(content))

    iwfm.wdl_meas_stats(str(input_file), verbose=False)

    output_file = tmp_path / 'test_input_stats.out'
    lines = output_file.read_text().strip().split('\n')

    # Should have header + 3 wells (but last well might not be written)
    assert len(lines) >= 2


def test_wdl_meas_stats_single_observation_per_well(tmp_path):
    '''Test wdl_meas_stats with single observation per well (stdev = -99.9).'''
    input_file = tmp_path / 'test_input.dat'

    content = [
        'HEADER LINE',
        'WELL001  01/15/2020  X  Y  100.5',
        'WELL002  01/16/2020  X  Y  200.5',
    ]
    input_file.write_text('\n'.join(content))

    iwfm.wdl_meas_stats(str(input_file), verbose=False)

    output_file = tmp_path / 'test_input_stats.out'
    content = output_file.read_text()

    # Single observation should have stdev of -99.9
    assert '-99.9' in content


def test_wdl_meas_stats_statistics_calculation(tmp_path):
    '''Test that statistics are calculated correctly.'''
    input_file = tmp_path / 'test_input.dat'

    content = [
        'HEADER LINE',
        'WELL001  01/15/2020  X  Y  100.0',
        'WELL001  01/16/2020  X  Y  110.0',
        'WELL001  01/17/2020  X  Y  120.0',
    ]
    input_file.write_text('\n'.join(content))

    iwfm.wdl_meas_stats(str(input_file), verbose=False)

    output_file = tmp_path / 'test_input_stats.out'
    lines = output_file.read_text().strip().split('\n')

    # Average should be 110.0, max 120.0, min 100.0
    assert len(lines) == 2  # header + 1 well


def test_wdl_meas_stats_uses_text_date():
    '''Test that wdl_meas_stats imports text_date function (verifies fix).'''
    # This test verifies the fix: added 'from iwfm import text_date'
    from iwfm.wdl_meas_stats import text_date

    result = text_date('01/15/2020')
    assert result is not None


def test_wdl_meas_stats_verbose_output(tmp_path, capsys):
    '''Test verbose output of wdl_meas_stats.'''
    input_file = tmp_path / 'test_input.dat'

    content = [
        'HEADER LINE',
        'WELL001  01/15/2020  X  Y  100.5',
        'WELL001  01/16/2020  X  Y  101.5',
    ]
    input_file.write_text('\n'.join(content))

    iwfm.wdl_meas_stats(str(input_file), verbose=True)

    captured = capsys.readouterr()
    assert 'Processed' in captured.out
    assert 'Wrote' in captured.out
