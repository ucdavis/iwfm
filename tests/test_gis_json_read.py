# test_gis_json_read.py
# Tests for gis/json_read.py - Read JSON data
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
import json


class TestJsonRead:
    """Tests for json_read function."""

    def test_parses_simple_object(self):
        """Test parsing simple JSON object."""
        from iwfm.gis.json_read import json_read
        
        jdata = '{"name": "test", "value": 123}'
        
        result = json_read(jdata)
        
        assert result['name'] == 'test'
        assert result['value'] == 123

    def test_parses_array(self):
        """Test parsing JSON array."""
        from iwfm.gis.json_read import json_read
        
        jdata = '[1, 2, 3, 4, 5]'
        
        result = json_read(jdata)
        
        assert result == [1, 2, 3, 4, 5]

    def test_parses_nested_object(self):
        """Test parsing nested JSON object."""
        from iwfm.gis.json_read import json_read
        
        jdata = '{"outer": {"inner": "value"}}'
        
        result = json_read(jdata)
        
        assert result['outer']['inner'] == 'value'

    def test_parses_boolean(self):
        """Test parsing JSON with boolean values."""
        from iwfm.gis.json_read import json_read
        
        jdata = '{"active": true, "disabled": false}'
        
        result = json_read(jdata)
        
        assert result['active'] is True
        assert result['disabled'] is False

    def test_parses_null(self):
        """Test parsing JSON with null value."""
        from iwfm.gis.json_read import json_read
        
        jdata = '{"value": null}'
        
        result = json_read(jdata)
        
        assert result['value'] is None

    def test_parses_geojson_point(self):
        """Test parsing GeoJSON point."""
        from iwfm.gis.json_read import json_read
        
        jdata = '''
        {
            "type": "Point",
            "coordinates": [-118.2437, 34.0522]
        }
        '''
        
        result = json_read(jdata)
        
        assert result['type'] == 'Point'
        assert result['coordinates'] == [-118.2437, 34.0522]

    def test_parses_geojson_polygon(self):
        """Test parsing GeoJSON polygon."""
        from iwfm.gis.json_read import json_read
        
        jdata = '''
        {
            "type": "Polygon",
            "coordinates": [[[0, 0], [10, 0], [10, 10], [0, 10], [0, 0]]]
        }
        '''
        
        result = json_read(jdata)
        
        assert result['type'] == 'Polygon'
        assert len(result['coordinates'][0]) == 5

    def test_verbose_mode(self, capsys):
        """Test verbose mode prints output."""
        from iwfm.gis.json_read import json_read
        
        jdata = '{"test": "value"}'
        
        json_read(jdata, verbose=True)
        
        captured = capsys.readouterr()
        assert 'JSON Data' in captured.out

    def test_invalid_json_raises_error(self):
        """Test that invalid JSON raises error."""
        from iwfm.gis.json_read import json_read
        
        jdata = 'not valid json'
        
        with pytest.raises(json.JSONDecodeError):
            json_read(jdata)

    def test_empty_object(self):
        """Test parsing empty JSON object."""
        from iwfm.gis.json_read import json_read
        
        jdata = '{}'
        
        result = json_read(jdata)
        
        assert result == {}

    def test_empty_array(self):
        """Test parsing empty JSON array."""
        from iwfm.gis.json_read import json_read
        
        jdata = '[]'
        
        result = json_read(jdata)
        
        assert result == []


class TestJsonReadImports:
    """Tests for json_read imports."""

    def test_import_from_gis(self):
        """Test import from iwfm.gis."""
        from iwfm.gis import json_read
        assert callable(json_read)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.gis.json_read import json_read
        assert callable(json_read)

    def test_function_has_docstring(self):
        """Test that function has documentation."""
        from iwfm.gis.json_read import json_read
        
        assert json_read.__doc__ is not None
        assert 'json' in json_read.__doc__.lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
