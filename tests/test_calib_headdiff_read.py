# test_calib_headdiff_read.py
# Unit tests for calib/headdiff_read.py - Read paired locations for head differences
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


class TestHeaddiffRead:
    """Tests for headdiff_read function"""

    def create_headdiff_file(self, tmp_path, pairs):
        """Create a mock head difference pairs file.
        
        Parameters
        ----------
        pairs : list of tuples/lists
            Each item is (site1, site2, optional_id...)
        """
        headdiff_file = tmp_path / 'headdiff.dat'
        lines = []
        for pair in pairs:
            lines.append('  '.join(str(x) for x in pair))
        headdiff_file.write_text('\n'.join(lines))
        return str(headdiff_file)

    def test_returns_three_items(self, tmp_path):
        """Test that function returns hdiff_sites, hdiff_pairs, hdiff_link."""
        from iwfm.calib.headdiff_read import headdiff_read

        headdiff_file = self.create_headdiff_file(tmp_path, [
            ('WELL_A', 'WELL_B', 'HDIFF_01'),
        ])

        result = headdiff_read(headdiff_file)

        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_hdiff_sites_contains_both_wells(self, tmp_path):
        """Test that hdiff_sites contains both wells from each pair."""
        from iwfm.calib.headdiff_read import headdiff_read

        headdiff_file = self.create_headdiff_file(tmp_path, [
            ('WELL_A', 'WELL_B', 'HDIFF_01'),
        ])

        hdiff_sites, hdiff_pairs, hdiff_link = headdiff_read(headdiff_file)

        assert 'WELL_A' in hdiff_sites
        assert 'WELL_B' in hdiff_sites

    def test_hdiff_pairs_structure(self, tmp_path):
        """Test that hdiff_pairs contains the parsed line items."""
        from iwfm.calib.headdiff_read import headdiff_read

        headdiff_file = self.create_headdiff_file(tmp_path, [
            ('WELL_A', 'WELL_B', 'HDIFF_01'),
        ])

        hdiff_sites, hdiff_pairs, hdiff_link = headdiff_read(headdiff_file)

        assert len(hdiff_pairs) == 1
        assert hdiff_pairs[0][0] == 'WELL_A'
        assert hdiff_pairs[0][1] == 'WELL_B'
        assert hdiff_pairs[0][2] == 'HDIFF_01'

    def test_hdiff_link_structure(self, tmp_path):
        """Test that hdiff_link contains [site2, site1] pairs."""
        from iwfm.calib.headdiff_read import headdiff_read

        headdiff_file = self.create_headdiff_file(tmp_path, [
            ('WELL_A', 'WELL_B', 'HDIFF_01'),
        ])

        hdiff_sites, hdiff_pairs, hdiff_link = headdiff_read(headdiff_file)

        assert len(hdiff_link) == 1
        # Link is [item[1], item[0]] = [WELL_B, WELL_A]
        assert hdiff_link[0][0] == 'WELL_B'
        assert hdiff_link[0][1] == 'WELL_A'

    def test_multiple_pairs(self, tmp_path):
        """Test with multiple head difference pairs."""
        from iwfm.calib.headdiff_read import headdiff_read

        headdiff_file = self.create_headdiff_file(tmp_path, [
            ('WELL_A', 'WELL_B', 'HDIFF_01'),
            ('WELL_C', 'WELL_D', 'HDIFF_02'),
            ('WELL_E', 'WELL_F', 'HDIFF_03'),
        ])

        hdiff_sites, hdiff_pairs, hdiff_link = headdiff_read(headdiff_file)

        assert len(hdiff_pairs) == 3
        assert len(hdiff_link) == 3
        # 3 pairs * 2 sites each = 6 sites
        assert len(hdiff_sites) == 6

    def test_skips_comment_lines(self, tmp_path):
        """Test that lines starting with # are skipped."""
        from iwfm.calib.headdiff_read import headdiff_read

        headdiff_file = tmp_path / 'headdiff.dat'
        content = """# This is a comment
# Another comment
WELL_A  WELL_B  HDIFF_01
# Comment in middle
WELL_C  WELL_D  HDIFF_02
"""
        headdiff_file.write_text(content)

        hdiff_sites, hdiff_pairs, hdiff_link = headdiff_read(str(headdiff_file))

        # Should only have 2 pairs (comments skipped)
        assert len(hdiff_pairs) == 2

    def test_sites_sorted(self, tmp_path):
        """Test that hdiff_sites list is sorted."""
        from iwfm.calib.headdiff_read import headdiff_read

        headdiff_file = self.create_headdiff_file(tmp_path, [
            ('ZEBRA', 'ALPHA', 'HDIFF_01'),
            ('MIKE', 'BETA', 'HDIFF_02'),
        ])

        hdiff_sites, hdiff_pairs, hdiff_link = headdiff_read(headdiff_file)

        assert hdiff_sites == sorted(hdiff_sites)

    def test_single_pair(self, tmp_path):
        """Test with single head difference pair."""
        from iwfm.calib.headdiff_read import headdiff_read

        headdiff_file = self.create_headdiff_file(tmp_path, [
            ('SHALLOW_WELL', 'DEEP_WELL', 'VGRAD_01'),
        ])

        hdiff_sites, hdiff_pairs, hdiff_link = headdiff_read(headdiff_file)

        assert len(hdiff_pairs) == 1
        assert len(hdiff_link) == 1
        assert len(hdiff_sites) == 2

    def test_many_pairs(self, tmp_path):
        """Test with many head difference pairs."""
        from iwfm.calib.headdiff_read import headdiff_read

        pairs = [(f'WELL_A_{i:02d}', f'WELL_B_{i:02d}', f'HDIFF_{i:02d}') 
                 for i in range(50)]
        headdiff_file = self.create_headdiff_file(tmp_path, pairs)

        hdiff_sites, hdiff_pairs, hdiff_link = headdiff_read(headdiff_file)

        assert len(hdiff_pairs) == 50
        assert len(hdiff_link) == 50
        assert len(hdiff_sites) == 100  # 50 pairs * 2 sites

    def test_duplicate_sites_in_pairs(self, tmp_path):
        """Test that duplicate sites appear multiple times in hdiff_sites."""
        from iwfm.calib.headdiff_read import headdiff_read

        # WELL_A appears in two pairs
        headdiff_file = self.create_headdiff_file(tmp_path, [
            ('WELL_A', 'WELL_B', 'HDIFF_01'),
            ('WELL_A', 'WELL_C', 'HDIFF_02'),
        ])

        hdiff_sites, hdiff_pairs, hdiff_link = headdiff_read(headdiff_file)

        # WELL_A should appear twice
        assert hdiff_sites.count('WELL_A') == 2

    def test_whitespace_handling(self, tmp_path):
        """Test that whitespace-separated fields are parsed correctly."""
        from iwfm.calib.headdiff_read import headdiff_read

        headdiff_file = tmp_path / 'headdiff.dat'
        # Various whitespace separations
        content = """WELL_A    WELL_B    HDIFF_01
WELL_C\tWELL_D\tHDIFF_02
"""
        headdiff_file.write_text(content)

        hdiff_sites, hdiff_pairs, hdiff_link = headdiff_read(str(headdiff_file))

        assert len(hdiff_pairs) == 2

    def test_typical_vertical_gradient_use_case(self, tmp_path):
        """Test typical use case: vertical gradient between shallow and deep wells."""
        from iwfm.calib.headdiff_read import headdiff_read

        headdiff_file = self.create_headdiff_file(tmp_path, [
            ('SHALLOW_01', 'DEEP_01', 'VGRAD_01'),
            ('SHALLOW_02', 'DEEP_02', 'VGRAD_02'),
            ('SHALLOW_03', 'DEEP_03', 'VGRAD_03'),
        ])

        hdiff_sites, hdiff_pairs, hdiff_link = headdiff_read(headdiff_file)

        # Verify structure
        assert len(hdiff_pairs) == 3
        
        # Check links point from deep to shallow
        for link in hdiff_link:
            assert 'DEEP' in link[0]
            assert 'SHALLOW' in link[1]

    def test_function_signature(self):
        """Test function has correct parameters."""
        from iwfm.calib.headdiff_read import headdiff_read
        import inspect
        
        sig = inspect.signature(headdiff_read)
        params = list(sig.parameters.keys())
        
        assert 'headdiff_file' in params


class TestHeaddiffReadImports:
    """Tests for function imports."""

    def test_import_from_calib(self):
        """Test import from iwfm.calib."""
        from iwfm.calib import headdiff_read
        assert callable(headdiff_read)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.calib.headdiff_read import headdiff_read
        assert callable(headdiff_read)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.calib.headdiff_read import headdiff_read
        
        assert headdiff_read.__doc__ is not None
        assert 'hdiff_sites' in headdiff_read.__doc__
        assert 'hdiff_pairs' in headdiff_read.__doc__
        assert 'hdiff_link' in headdiff_read.__doc__


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
