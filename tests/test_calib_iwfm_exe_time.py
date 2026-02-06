# test_calib_iwfm_exe_time.py
# Unit tests for calib/iwfm_exe_time function
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


def test_iwfm_exe_time_basic(tmp_path):
    '''Test basic functionality of iwfm_exe_time.'''
    from iwfm.calib.iwfm_exe_time import iwfm_exe_time

    infile = tmp_path / 'SimulationMessages.out'
    outfile = tmp_path / 'exe_time.smp'

    # Create a valid SimulationMessages.out file
    content = [
        'IWFM Simulation Messages',
        'Starting simulation...',
        'Processing...',
        'TOTAL RUN TIME:     2 HOURS    30 MINUTES    15 SECONDS',
        'Simulation complete.',
    ]
    infile.write_text('\n'.join(content))

    result = iwfm_exe_time(str(infile), str(outfile))

    # 2 hours + 30 minutes + 15 seconds = 7200 + 1800 + 15 = 9015 seconds
    assert result == 9015.0
    assert outfile.exists()


def test_iwfm_exe_time_minutes_only(tmp_path):
    '''Test iwfm_exe_time with only minutes and seconds.'''
    from iwfm.calib.iwfm_exe_time import iwfm_exe_time

    infile = tmp_path / 'SimulationMessages.out'
    outfile = tmp_path / 'exe_time.smp'

    content = [
        'IWFM Simulation Messages',
        'TOTAL RUN TIME:     45 MINUTES    30 SECONDS',
    ]
    infile.write_text('\n'.join(content))

    result = iwfm_exe_time(str(infile), str(outfile))

    # 45 minutes + 30 seconds = 2700 + 30 = 2730 seconds
    assert result == 2730.0


def test_iwfm_exe_time_seconds_only(tmp_path):
    '''Test iwfm_exe_time with only seconds.'''
    from iwfm.calib.iwfm_exe_time import iwfm_exe_time

    infile = tmp_path / 'SimulationMessages.out'
    outfile = tmp_path / 'exe_time.smp'

    content = [
        'IWFM Simulation Messages',
        'TOTAL RUN TIME:     123 SECONDS',
    ]
    infile.write_text('\n'.join(content))

    result = iwfm_exe_time(str(infile), str(outfile))

    assert result == 123.0


def test_iwfm_exe_time_output_format(tmp_path):
    '''Test that output file has correct SMP format.'''
    from iwfm.calib.iwfm_exe_time import iwfm_exe_time

    infile = tmp_path / 'SimulationMessages.out'
    outfile = tmp_path / 'exe_time.smp'

    content = [
        'TOTAL RUN TIME:     1 HOURS    0 MINUTES    0 SECONDS',
    ]
    infile.write_text('\n'.join(content))

    iwfm_exe_time(str(infile), str(outfile))

    output_content = outfile.read_text()
    assert 'EXETIME' in output_content
    assert '10/31/1985' in output_content
    assert '3600' in output_content  # 1 hour = 3600 seconds


def test_iwfm_exe_time_text_not_found(tmp_path):
    '''Test that iwfm_exe_time writes error message when TOTAL RUN TIME not found (verifies fix).'''
    from iwfm.calib.iwfm_exe_time import iwfm_exe_time

    infile = tmp_path / 'SimulationMessages.out'
    outfile = tmp_path / 'exe_time.smp'

    # File without 'TOTAL RUN TIME' line
    content = [
        'IWFM Simulation Messages',
        'Starting simulation...',
        'Simulation complete.',
    ]
    infile.write_text('\n'.join(content))

    # Should return -999.0 and write error message to output file
    result = iwfm_exe_time(str(infile), str(outfile))

    assert result == -999.0
    assert outfile.exists()

    output_content = outfile.read_text()
    assert "'TOTAL RUN TIME' not found" in output_content
    assert str(infile) in output_content


def test_iwfm_exe_time_empty_file(tmp_path):
    '''Test that iwfm_exe_time handles empty file (verifies fix).'''
    from iwfm.calib.iwfm_exe_time import iwfm_exe_time

    infile = tmp_path / 'SimulationMessages.out'
    outfile = tmp_path / 'exe_time.smp'

    # Empty file
    infile.write_text('')

    # Should return -999.0 and write error message
    result = iwfm_exe_time(str(infile), str(outfile))

    assert result == -999.0
    assert outfile.exists()

    output_content = outfile.read_text()
    assert "'TOTAL RUN TIME' not found" in output_content


def test_iwfm_exe_time_missing_file():
    '''Test that iwfm_exe_time handles missing input file.'''
    from iwfm.calib.iwfm_exe_time import iwfm_exe_time

    # Should raise an error (file_test will catch it)
    with pytest.raises((FileNotFoundError, SystemExit)):
        iwfm_exe_time('nonexistent_file.out', 'output.smp')


def test_iwfm_exe_time_function_signature():
    '''Test that iwfm_exe_time has correct function signature.'''
    from iwfm.calib.iwfm_exe_time import iwfm_exe_time
    import inspect

    sig = inspect.signature(iwfm_exe_time)
    params = list(sig.parameters.keys())

    assert 'infile' in params
    assert 'outfile' in params
    assert sig.parameters['infile'].default == 'SimulationMessages.out'
    assert sig.parameters['outfile'].default == 'exe_time.smp'
