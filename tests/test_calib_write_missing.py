# test_calib_write_missing.py
# Unit tests for calib/write_missing.py - Write missing observation IDs to file
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
import os


class TestWriteMissing:
    """Tests for write_missing function"""

    def test_creates_output_file(self, tmp_path):
        """Test that output file is created."""
        from iwfm.calib.write_missing import write_missing

        missing = ['WELL001', 'WELL002']
        obs_file = 'observations.smp'
        fname = str(tmp_path / 'missing.tmp')

        write_missing(missing, obs_file, fname=fname)

        assert os.path.exists(fname)

    def test_writes_missing_sites(self, tmp_path):
        """Test that missing sites are written to file."""
        from iwfm.calib.write_missing import write_missing

        missing = ['WELL001', 'WELL002', 'WELL003']
        obs_file = 'observations.smp'
        fname = str(tmp_path / 'missing.tmp')

        write_missing(missing, obs_file, fname=fname)

        with open(fname, 'r') as f:
            content = f.read()

        assert 'WELL001' in content
        assert 'WELL002' in content
        assert 'WELL003' in content

    def test_writes_header_with_obs_file(self, tmp_path):
        """Test that header includes observation file name."""
        from iwfm.calib.write_missing import write_missing

        missing = ['WELL001']
        obs_file = 'my_observations.smp'
        fname = str(tmp_path / 'missing.tmp')

        write_missing(missing, obs_file, fname=fname)

        with open(fname, 'r') as f:
            content = f.read()

        assert 'my_observations.smp' in content

    def test_sorts_missing_sites(self, tmp_path):
        """Test that missing sites are sorted."""
        from iwfm.calib.write_missing import write_missing

        missing = ['WELL003', 'WELL001', 'WELL002']
        obs_file = 'observations.smp'
        fname = str(tmp_path / 'missing.tmp')

        write_missing(missing, obs_file, fname=fname)

        with open(fname, 'r') as f:
            lines = f.readlines()

        # Find the site lines (skip header)
        site_lines = [l.strip() for l in lines if l.strip().startswith('WELL')]
        
        assert site_lines == sorted(site_lines)

    def test_empty_missing_list(self, tmp_path):
        """Test with empty missing list (no file created)."""
        from iwfm.calib.write_missing import write_missing

        missing = []
        obs_file = 'observations.smp'
        fname = str(tmp_path / 'missing.tmp')

        write_missing(missing, obs_file, fname=fname)

        # File should not be created when missing list is empty
        assert not os.path.exists(fname)

    def test_appends_to_existing_file(self, tmp_path):
        """Test that function appends to existing file."""
        from iwfm.calib.write_missing import write_missing

        fname = str(tmp_path / 'missing.tmp')
        
        # Create initial content
        with open(fname, 'w') as f:
            f.write('Initial content\n')

        missing = ['WELL001']
        obs_file = 'observations.smp'

        write_missing(missing, obs_file, fname=fname)

        with open(fname, 'r') as f:
            content = f.read()

        assert 'Initial content' in content
        assert 'WELL001' in content

    def test_single_missing_site(self, tmp_path):
        """Test with single missing site."""
        from iwfm.calib.write_missing import write_missing

        missing = ['SINGLE_WELL']
        obs_file = 'observations.smp'
        fname = str(tmp_path / 'missing.tmp')

        write_missing(missing, obs_file, fname=fname)

        with open(fname, 'r') as f:
            content = f.read()

        assert 'SINGLE_WELL' in content

    def test_many_missing_sites(self, tmp_path):
        """Test with many missing sites."""
        from iwfm.calib.write_missing import write_missing

        missing = [f'WELL{i:03d}' for i in range(100)]
        obs_file = 'observations.smp'
        fname = str(tmp_path / 'missing.tmp')

        write_missing(missing, obs_file, fname=fname)

        with open(fname, 'r') as f:
            content = f.read()

        assert 'WELL000' in content
        assert 'WELL099' in content


class TestWriteMissingImports:
    """Tests for function imports."""

    def test_import_from_calib(self):
        """Test import from iwfm.calib."""
        from iwfm.calib import write_missing
        assert callable(write_missing)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.calib.write_missing import write_missing
        assert callable(write_missing)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.calib.write_missing import write_missing
        
        assert write_missing.__doc__ is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
