# test_gis_xml_fix.py
# Tests for gis/xml_fix.py - Fix a broken XML file
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

# Check if lxml is available for BeautifulSoup XML parsing
try:
    import lxml  # noqa: F401
    del lxml
    HAS_LXML = True
except ImportError:
    HAS_LXML = False


@pytest.mark.skipif(not HAS_LXML, reason="lxml not installed (required for BeautifulSoup XML parsing)")
class TestXmlFix:
    """Tests for xml_fix function."""

    def test_creates_output_file(self, tmp_path):
        """Test that function creates an output file."""
        from iwfm.gis.xml_fix import xml_fix

        infile = tmp_path / "input.xml"
        outfile = tmp_path / "output.xml"

        # Create a simple XML file
        infile.write_text('<?xml version="1.0"?><root><item>test</item></root>')

        xml_fix(str(infile), str(outfile))

        assert outfile.exists()

    def test_fixes_malformed_xml(self, tmp_path):
        """Test that function can handle malformed XML."""
        from iwfm.gis.xml_fix import xml_fix

        infile = tmp_path / "broken.xml"
        outfile = tmp_path / "fixed.xml"

        # Create XML with unclosed tags (BeautifulSoup should fix this)
        broken_content = '<root><item>test<nested>content</root>'
        infile.write_text(broken_content)

        xml_fix(str(infile), str(outfile))

        # Output file should exist
        assert outfile.exists()

        # Output should be valid XML (prettified)
        content = outfile.read_text()
        assert '<root>' in content or '<root' in content

    def test_preserves_valid_xml(self, tmp_path):
        """Test that valid XML is preserved."""
        from iwfm.gis.xml_fix import xml_fix

        infile = tmp_path / "valid.xml"
        outfile = tmp_path / "output.xml"

        valid_content = '<?xml version="1.0"?><root><item>value</item></root>'
        infile.write_text(valid_content)

        xml_fix(str(infile), str(outfile))

        content = outfile.read_text()
        assert 'item' in content
        assert 'value' in content

    def test_verbose_output(self, tmp_path, capsys):
        """Test verbose output."""
        from iwfm.gis.xml_fix import xml_fix

        infile = tmp_path / "input.xml"
        outfile = tmp_path / "output.xml"
        infile.write_text('<root><item>test</item></root>')

        xml_fix(str(infile), str(outfile), verbose=True)

        captured = capsys.readouterr()
        assert 'fixed' in captured.out.lower() or len(captured.out) > 0

    def test_returns_none(self, tmp_path):
        """Test that function returns None."""
        from iwfm.gis.xml_fix import xml_fix

        infile = tmp_path / "input.xml"
        outfile = tmp_path / "output.xml"
        infile.write_text('<root>test</root>')

        result = xml_fix(str(infile), str(outfile))

        assert result is None


class TestXmlFixImports:
    """Tests for xml_fix imports."""

    def test_import_from_gis(self):
        """Test import from iwfm.gis."""
        from iwfm.gis import xml_fix
        assert callable(xml_fix)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.gis.xml_fix import xml_fix
        assert callable(xml_fix)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.gis.xml_fix import xml_fix

        assert xml_fix.__doc__ is not None
        assert 'xml' in xml_fix.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
