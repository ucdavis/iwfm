# test_write_smp.py 
# Test write_smp function for writing PEST smp files
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




def test_write_smp_basic(tmp_path):
    '''Test basic functionality of write_smp with valid data.'''
    from iwfm.write_smp import write_smp

    output_file = tmp_path / 'test_output'
    lines = [
        ['WELL001', '01/15/2020', '12:00:00', '123.456'],
        ['WELL002', '01/16/2020', '13:30:00', '234.567'],
        ['WELL003', '01/17/2020', '14:45:00', '345.678'],
    ]

    result = write_smp(str(output_file), lines)

    assert result == 3
    assert (tmp_path / 'test_output.smp').exists()


def test_write_smp_adds_extension(tmp_path):
    '''Test that write_smp automatically adds .smp extension.'''
    from iwfm.write_smp import write_smp

    output_file = tmp_path / 'test_output'
    lines = [['WELL001', '01/15/2020', '12:00:00', '123.456']]

    write_smp(str(output_file), lines)

    assert (tmp_path / 'test_output.smp').exists()


def test_write_smp_preserves_extension(tmp_path):
    '''Test that write_smp preserves .smp extension if already present.'''
    from iwfm.write_smp import write_smp

    output_file = tmp_path / 'test_output.smp'
    lines = [['WELL001', '01/15/2020', '12:00:00', '123.456']]

    write_smp(str(output_file), lines)

    assert (tmp_path / 'test_output.smp').exists()


def test_write_smp_file_content(tmp_path):
    '''Test that write_smp writes correct content format.'''
    from iwfm.write_smp import write_smp

    output_file = tmp_path / 'test_output.smp'
    lines = [
        ['WELL001', '01/15/2020', '12:00:00', '123.456'],
        ['WELL002', '01/16/2020', '13:30:00', '234.567'],
    ]

    write_smp(str(output_file), lines)

    content = output_file.read_text()
    lines_written = content.strip().split('\n')

    assert len(lines_written) == 2
    assert 'WELL001\t01/15/2020\t12:00:00\t123.456' in lines_written[0]
    assert 'WELL002\t01/16/2020\t13:30:00\t234.567' in lines_written[1]


def test_write_smp_empty_list(tmp_path):
    '''Test write_smp with empty list returns 0.'''
    from iwfm.write_smp import write_smp

    output_file = tmp_path / 'test_output.smp'
    lines = []

    result = write_smp(str(output_file), lines)

    assert result == 0
    assert output_file.exists()


def test_write_smp_single_observation(tmp_path):
    '''Test write_smp with single observation.'''
    from iwfm.write_smp import write_smp

    output_file = tmp_path / 'test_output.smp'
    lines = [['WELL001', '01/15/2020', '12:00:00', '123.456']]

    result = write_smp(str(output_file), lines)

    assert result == 1
    content = output_file.read_text()
    assert 'WELL001' in content
    assert '123.456' in content


def test_write_smp_uses_inline_extension_logic():
    '''Test that write_smp uses inline .smp extension logic.'''
    import inspect
    from iwfm import write_smp as write_smp_module
    source = inspect.getsource(write_smp_module)
    assert "endswith('.smp')" in source  # inline extension check
