# test_calib_read_settings.py 
# Test calib/read_settings function for reading PEST settings
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
from pathlib import Path


def test_read_settings_imports():
    '''Test that read_settings source code contains only necessary imports (verifies fix).'''
    from iwfm.calib import read_settings
    import inspect

    source = inspect.getsource(read_settings)
    # Verify os is imported (needed for file operations)
    assert 'import os' in source
    # Verify unused imports are removed
    assert 'import sys' not in source
    assert 'import iwfm' not in source


def test_read_settings_handles_invalid_lines():
    '''Test that read_settings handles invalid lines gracefully (verifies fix).'''
    from iwfm.calib import read_settings
    import inspect

    source = inspect.getsource(read_settings)
    # Function should skip blank lines and comments, not call sys.exit()
    assert 'continue' in source
    assert 'startswith' in source or 'skip' in source.lower()


def test_read_settings_function_exists():
    '''Test that read_settings function is defined.'''
    from iwfm.calib.read_settings import read_settings

    assert callable(read_settings)


def test_read_settings_function_signature():
    '''Test that read_settings has correct function signature.'''
    from iwfm.calib.read_settings import read_settings
    import inspect

    sig = inspect.signature(read_settings)
    params = list(sig.parameters.keys())

    assert 'in_file' in params


def test_read_settings_with_valid_file(tmp_path):
    '''Test read_settings with a valid settings file.'''
    from iwfm.calib.read_settings import read_settings

    settings_file = tmp_path / 'settings.fig'

    # Create a valid settings file with expected format
    content = [
        '# Settings file for PEST calibration',
        'date=mm/dd/yyyy',
        'colrow=no',
        '# Other parameters can be here',
        'other_param=value',
    ]
    settings_file.write_text('\n'.join(content))

    datespec, headerspec, idate, iheader = read_settings(str(settings_file))

    # Verify return values
    assert datespec == 2  # mm/dd/yyyy format
    assert headerspec == 'no'
    assert idate == 0  # No date error
    assert iheader == 0  # No header error


def test_read_settings_with_missing_file(tmp_path):
    '''Test read_settings with missing file creates default.'''
    from iwfm.calib.read_settings import read_settings
    import os

    # Use a non-existent file path
    missing_file = tmp_path / 'nonexistent_settings.fig'

    # Verify file doesn't exist before calling
    assert not os.path.isfile(str(missing_file))

    # Function should create a default file and return default values
    datespec, headerspec, idate, iheader = read_settings(str(missing_file))

    # Verify default values returned
    assert datespec == 2  # Default: mm/dd/yyyy
    assert headerspec == 'no'
    assert idate == 0
    assert iheader == 0

    # Verify default file was created
    assert os.path.isfile(str(missing_file))

    # Verify default file content
    content = missing_file.read_text()
    assert 'colrow=no' in content
    assert 'date=mm/dd/yyyy' in content


def test_read_settings_with_dd_mm_yyyy_format(tmp_path):
    '''Test read_settings with dd/mm/yyyy date format.'''
    from iwfm.calib.read_settings import read_settings

    settings_file = tmp_path / 'settings.fig'
    content = [
        'date=dd/mm/yyyy',
        'colrow=yes',
    ]
    settings_file.write_text('\n'.join(content))

    datespec, headerspec, idate, iheader = read_settings(str(settings_file))

    assert datespec == 1  # dd/mm/yyyy format
    assert headerspec == 'yes'
    assert idate == 0
    assert iheader == 0


def test_read_settings_with_comments_and_blank_lines(tmp_path):
    '''Test that read_settings handles comments and blank lines (verifies fix).'''
    from iwfm.calib.read_settings import read_settings

    settings_file = tmp_path / 'settings.fig'
    content = [
        '# This is a comment',
        '',
        '  # Indented comment',
        'date=mm/dd/yyyy',
        '',
        'colrow=no',
        '# Another comment',
        'unknown_setting=value',  # Should be silently skipped
    ]
    settings_file.write_text('\n'.join(content))

    # Should not raise SystemExit
    datespec, headerspec, idate, iheader = read_settings(str(settings_file))

    assert datespec == 2
    assert headerspec == 'no'
    assert idate == 0
    assert iheader == 0


def test_read_settings_with_invalid_date_format(tmp_path):
    '''Test read_settings with invalid date format.'''
    from iwfm.calib.read_settings import read_settings

    settings_file = tmp_path / 'settings.fig'
    content = [
        'date=yyyy/mm/dd',  # Invalid format
        'colrow=no',
    ]
    settings_file.write_text('\n'.join(content))

    datespec, headerspec, idate, iheader = read_settings(str(settings_file))

    assert idate == 1  # Error flag set
    assert headerspec == 'no'


def test_read_settings_with_invalid_colrow_value(tmp_path):
    '''Test read_settings with invalid colrow value.'''
    from iwfm.calib.read_settings import read_settings

    settings_file = tmp_path / 'settings.fig'
    content = [
        'date=mm/dd/yyyy',
        'colrow=maybe',  # Invalid value
    ]
    settings_file.write_text('\n'.join(content))

    datespec, headerspec, idate, iheader = read_settings(str(settings_file))

    assert datespec == 2
    assert iheader == 1  # Error flag set
