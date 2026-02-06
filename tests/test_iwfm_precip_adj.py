# test_iwfm_precip_adj.py
# unit test for iwfm_precip_adj function in the iwfm package
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

import iwfm


# ============================================================================
# Test iwfm_precip_adj with synthetic data
# ============================================================================

def test_iwfm_precip_adj_creates_output(tmp_path):
    '''Test that iwfm_precip_adj creates output file.'''
    import os
    original_cwd = os.getcwd()
    os.chdir(tmp_path)

    try:
        # Create test precipitation file
        precip_file = tmp_path / 'precip.dat'
        precip_lines = [
            'C Precipitation file',
            'C Comment 2',
            'C Comment 3',
            '     2.000000                                 / FACT',
            '     1                                        / NFQCP',
            '     0                                        / Header 3',
            '     0                                        / Header 4',
            '     0                                        / Header 5',
            '10/01/1990_24:00\t1.50\t2.00',
            '10/02/1990_24:00\t1.25\t1.75',
            '10/03/1990_24:00\t2.00\t2.50'
        ]
        precip_file.write_text('\n'.join(precip_lines))

        # Create element-VIC linkage file
        elem_vic_file = tmp_path / 'elem_vic.csv'
        elem_vic_content = '''Column,VIC_ID,Region,Name
1,1,Region1,VIC1
2,2,Region1,VIC2
'''
        elem_vic_file.write_text(elem_vic_content)

        # Create factors file
        factors_file = tmp_path / 'factors.csv'
        factors_content = '''Date,VIC1,VIC2
10/01/1990,1.1,1.2
10/02/1990,1.0,1.1
10/03/1990,0.9,1.0
'''
        factors_file.write_text(factors_content)

        # Create years file
        years_file = tmp_path / 'years.csv'
        years_content = '''Year,Region1
1990,1990
'''
        years_file.write_text(years_content)

        output_file = tmp_path / 'output_precip.dat'

        # Run function
        iwfm.iwfm_precip_adj(
            str(precip_file),
            str(elem_vic_file),
            str(factors_file),
            str(years_file),
            str(output_file),
            verbose=False
        )

        # Verify output file was created
        assert output_file.exists()

        # Verify factors file was created
        factors_dat = tmp_path / 'factors.dat'
        assert factors_dat.exists()

    finally:
        os.chdir(original_cwd)


def test_iwfm_precip_adj_applies_factors_correctly(tmp_path):
    '''Test that precipitation values are adjusted correctly.'''
    # Create test precipitation file
    precip_file = tmp_path / 'precip.dat'
    precip_lines = [
        'C Precipitation file',
        'C Comment 2',
        'C Comment 3',
        '     2.000000                                 / FACT',
        '     1                                        / NFQCP',
        '     0                                        / Header 3',
        '     0                                        / Header 4',
        '     0                                        / Header 5',
        '10/01/1990_24:00\t10.0\t20.0'
    ]
    precip_file.write_text('\n'.join(precip_lines))

    # Create element-VIC linkage file
    elem_vic_file = tmp_path / 'elem_vic.csv'
    elem_vic_content = '''Column,VIC_ID,Region,Name
1,1,Region1,VIC1
2,2,Region1,VIC2
'''
    elem_vic_file.write_text(elem_vic_content)

    # Create factors file with specific multipliers
    factors_file = tmp_path / 'factors.csv'
    factors_content = '''Date,VIC1,VIC2
10/01/1990,2.0,0.5
'''
    factors_file.write_text(factors_content)

    # Create years file
    years_file = tmp_path / 'years.csv'
    years_content = '''Year,Region1
1990,1990
'''
    years_file.write_text(years_content)

    output_file = tmp_path / 'output_precip.dat'

    # Run function
    iwfm.iwfm_precip_adj(
        str(precip_file),
        str(elem_vic_file),
        str(factors_file),
        str(years_file),
        str(output_file),
        verbose=False
    )

    # Read output file
    output_content = output_file.read_text()
    lines = output_content.strip().split('\n')

    # Find the data line (skip header)
    data_line = None
    for line in lines:
        if '10/01/1990_24:00' in line:
            data_line = line
            break

    assert data_line is not None, 'Data line not found in output'

    # Parse values: 10.0 * 2.0 = 20.0, 20.0 * 0.5 = 10.0
    parts = data_line.split()
    assert len(parts) >= 3
    value1 = float(parts[1])
    value2 = float(parts[2])

    # Allow small floating point differences
    assert abs(value1 - 20.0) < 0.01
    assert abs(value2 - 10.0) < 0.01


def test_iwfm_precip_adj_handles_missing_vic_column(tmp_path):
    '''Test handling of precipitation columns without VIC ID (bare except fix).'''
    # Create test precipitation file with 3 columns
    precip_file = tmp_path / 'precip.dat'
    precip_lines = [
        'C Precipitation file',
        'C Comment 2',
        'C Comment 3',
        '     2.000000                                 / FACT',
        '     1                                        / NFQCP',
        '     0                                        / Header 3',
        '     0                                        / Header 4',
        '     0                                        / Header 5',
        '10/01/1990_24:00\t10.0\t20.0\t30.0'
    ]
    precip_file.write_text('\n'.join(precip_lines))

    # Create element-VIC linkage file - only columns 1 and 2, not 3
    elem_vic_file = tmp_path / 'elem_vic.csv'
    elem_vic_content = '''Column,VIC_ID,Region,Name
1,1,Region1,VIC1
2,2,Region1,VIC2
'''
    elem_vic_file.write_text(elem_vic_content)

    # Create factors file
    factors_file = tmp_path / 'factors.csv'
    factors_content = '''Date,VIC1,VIC2
10/01/1990,1.5,2.0
'''
    factors_file.write_text(factors_content)

    # Create years file
    years_file = tmp_path / 'years.csv'
    years_content = '''Year,Region1
1990,1990
'''
    years_file.write_text(years_content)

    output_file = tmp_path / 'output_precip.dat'

    # Run function - should not raise exception for missing column 3
    iwfm.iwfm_precip_adj(
        str(precip_file),
        str(elem_vic_file),
        str(factors_file),
        str(years_file),
        str(output_file),
        verbose=False
    )

    # Read output file
    output_content = output_file.read_text()
    lines = output_content.strip().split('\n')

    # Find the data line
    data_line = None
    for line in lines:
        if '10/01/1990_24:00' in line:
            data_line = line
            break

    assert data_line is not None

    # Parse values: col1 * 1.5 = 15.0, col2 * 2.0 = 40.0, col3 * 1.0 = 30.0 (no change)
    parts = data_line.split()
    assert len(parts) >= 4
    value1 = float(parts[1])
    value2 = float(parts[2])
    value3 = float(parts[3])

    assert abs(value1 - 15.0) < 0.01
    assert abs(value2 - 40.0) < 0.01
    assert abs(value3 - 30.0) < 0.01  # Column 3 should remain unchanged


def test_iwfm_precip_adj_handles_replacement_years(tmp_path):
    '''Test handling of years without VIC factors using replacement years.'''
    # Create test precipitation file for year 1991 (not in factors)
    precip_file = tmp_path / 'precip.dat'
    precip_lines = [
        'C Precipitation file',
        'C Comment 2',
        'C Comment 3',
        '     2.000000                                 / FACT',
        '     1                                        / NFQCP',
        '     0                                        / Header 3',
        '     0                                        / Header 4',
        '     0                                        / Header 5',
        '10/01/1991_24:00\t10.0\t20.0'
    ]
    precip_file.write_text('\n'.join(precip_lines))

    # Create element-VIC linkage file
    elem_vic_file = tmp_path / 'elem_vic.csv'
    elem_vic_content = '''Column,VIC_ID,Region,Name
1,1,Region1,VIC1
2,2,Region1,VIC2
'''
    elem_vic_file.write_text(elem_vic_content)

    # Create factors file - only has 1990, not 1991
    factors_file = tmp_path / 'factors.csv'
    factors_content = '''Date,VIC1,VIC2
10/01/1990,2.0,3.0
'''
    factors_file.write_text(factors_content)

    # Create years file - map 1991 to 1990
    years_file = tmp_path / 'years.csv'
    years_content = '''Year,Region1
1990,1990
1991,1990
'''
    years_file.write_text(years_content)

    output_file = tmp_path / 'output_precip.dat'

    # Run function
    iwfm.iwfm_precip_adj(
        str(precip_file),
        str(elem_vic_file),
        str(factors_file),
        str(years_file),
        str(output_file),
        verbose=False
    )

    # Read output file
    output_content = output_file.read_text()
    lines = output_content.strip().split('\n')

    # Find the data line
    data_line = None
    for line in lines:
        if '10/01/1991_24:00' in line:
            data_line = line
            break

    assert data_line is not None

    # Parse values - should use 1990 factors: 10.0 * 2.0 = 20.0, 20.0 * 3.0 = 60.0
    parts = data_line.split()
    value1 = float(parts[1])
    value2 = float(parts[2])

    assert abs(value1 - 20.0) < 0.01
    assert abs(value2 - 60.0) < 0.01


def test_iwfm_precip_adj_preserves_header(tmp_path):
    '''Test that output file preserves header from input.'''
    # Create test precipitation file
    precip_file = tmp_path / 'precip.dat'
    precip_lines = [
        'C Precipitation file with special header',
        'C Important comment line',
        'C Another important line',
        '     2.000000                                 / FACT',
        '     1                                        / NFQCP',
        '     0                                        / Header 3',
        '     0                                        / Header 4',
        '     0                                        / Header 5',
        '10/01/1990_24:00\t10.0'
    ]
    precip_file.write_text('\n'.join(precip_lines))

    # Create minimal other files
    elem_vic_file = tmp_path / 'elem_vic.csv'
    elem_vic_file.write_text('Column,VIC_ID,Region,Name\n1,1,Region1,VIC1\n')

    factors_file = tmp_path / 'factors.csv'
    factors_file.write_text('Date,VIC1\n10/01/1990,1.0\n')

    years_file = tmp_path / 'years.csv'
    years_file.write_text('Year,Region1\n1990,1990\n')

    output_file = tmp_path / 'output_precip.dat'

    # Run function
    iwfm.iwfm_precip_adj(
        str(precip_file),
        str(elem_vic_file),
        str(factors_file),
        str(years_file),
        str(output_file),
        verbose=False
    )

    # Read output
    output_content = output_file.read_text()

    # Verify header lines are preserved
    assert 'Precipitation file with special header' in output_content
    assert 'Important comment line' in output_content
    assert 'Another important line' in output_content
    assert '2.000000' in output_content
    assert 'FACT' in output_content


def test_iwfm_precip_adj_verbose_mode(tmp_path, capsys):
    '''Test that verbose mode produces output.'''
    # Create minimal test files
    precip_file = tmp_path / 'precip.dat'
    precip_lines = [
        'C Precipitation',
        'C Comment',
        'C Comment',
        '     2.0        / FACT',
        '     1          / NFQCP',
        '     0          / Header 3',
        '     0          / Header 4',
        '     0          / Header 5',
        '10/01/1990_24:00\t10.0',
        '10/02/1990_24:00\t11.0'
    ]
    precip_file.write_text('\n'.join(precip_lines))

    elem_vic_file = tmp_path / 'elem_vic.csv'
    elem_vic_file.write_text('Column,VIC_ID,Region,Name\n1,1,Region1,VIC1\n')

    factors_file = tmp_path / 'factors.csv'
    factors_file.write_text('Date,VIC1\n10/01/1990,1.0\n10/02/1990,1.0\n')

    years_file = tmp_path / 'years.csv'
    years_file.write_text('Year,Region1\n1990,1990\n')

    output_file = tmp_path / 'output_precip.dat'

    # Run with verbose=True
    iwfm.iwfm_precip_adj(
        str(precip_file),
        str(elem_vic_file),
        str(factors_file),
        str(years_file),
        str(output_file),
        verbose=True
    )

    # Check verbose output
    captured = capsys.readouterr()
    assert 'Processing' in captured.out or '10/01/1990' in captured.out


def test_iwfm_precip_adj_rounds_output_correctly(tmp_path):
    '''Test that output values are rounded to 2 decimal places.'''
    # Create test precipitation file
    precip_file = tmp_path / 'precip.dat'
    precip_lines = [
        'C Precipitation file',
        'C Comment 2',
        'C Comment 3',
        '     2.0        / FACT',
        '     1          / NFQCP',
        '     0          / Header 3',
        '     0          / Header 4',
        '     0          / Header 5',
        '10/01/1990_24:00\t10.123456'
    ]
    precip_file.write_text('\n'.join(precip_lines))

    elem_vic_file = tmp_path / 'elem_vic.csv'
    elem_vic_file.write_text('Column,VIC_ID,Region,Name\n1,1,Region1,VIC1\n')

    # Factor that will create long decimal
    factors_file = tmp_path / 'factors.csv'
    factors_file.write_text('Date,VIC1\n10/01/1990,1.333333\n')

    years_file = tmp_path / 'years.csv'
    years_file.write_text('Year,Region1\n1990,1990\n')

    output_file = tmp_path / 'output_precip.dat'

    iwfm.iwfm_precip_adj(
        str(precip_file),
        str(elem_vic_file),
        str(factors_file),
        str(years_file),
        str(output_file),
        verbose=False
    )

    # Read output
    output_content = output_file.read_text()
    lines = output_content.strip().split('\n')

    data_line = None
    for line in lines:
        if '10/01/1990_24:00' in line:
            data_line = line
            break

    assert data_line is not None

    # Value should be rounded: 10.123456 * 1.333333 ≈ 13.50
    parts = data_line.split()
    value = parts[1]

    # Check that value has at most 2 decimal places
    if '.' in value:
        decimal_part = value.split('.')[1]
        assert len(decimal_part) <= 2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
