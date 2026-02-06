# test_hdf5_utils.py
# Tests for hdf5/hdf5_utils.py - Shared HDF5 utility functions
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
import numpy as np
from datetime import datetime


class TestApplyUnitConversion:
    """Tests for apply_unit_conversion function."""

    def test_import(self):
        """Test that function can be imported."""
        from iwfm.hdf5.hdf5_utils import apply_unit_conversion
        assert callable(apply_unit_conversion)

    def test_volume_conversion(self):
        """Test volume conversion (type 1)."""
        from iwfm.hdf5.hdf5_utils import apply_unit_conversion

        data = np.array([[100.0, 200.0]])
        col_types = [0, 1, 1]  # First is time, rest are volume
        result = apply_unit_conversion(data, col_types, area_fact=0.01, vol_fact=0.5)

        np.testing.assert_array_almost_equal(result, [[50.0, 100.0]])

    def test_area_conversion(self):
        """Test area conversion (type 2)."""
        from iwfm.hdf5.hdf5_utils import apply_unit_conversion

        data = np.array([[100.0]])
        col_types = [0, 2]  # First is time, second is area
        result = apply_unit_conversion(data, col_types, area_fact=0.25, vol_fact=0.5)

        np.testing.assert_array_almost_equal(result, [[25.0]])

    def test_storage_conversion(self):
        """Test storage conversion (type 3) uses volume factor."""
        from iwfm.hdf5.hdf5_utils import apply_unit_conversion

        data = np.array([[100.0]])
        col_types = [0, 3]  # Storage type
        result = apply_unit_conversion(data, col_types, area_fact=0.1, vol_fact=0.5)

        np.testing.assert_array_almost_equal(result, [[50.0]])

    def test_length_conversion(self):
        """Test length conversion (type 4)."""
        from iwfm.hdf5.hdf5_utils import apply_unit_conversion

        data = np.array([[100.0]])
        col_types = [0, 4]  # Length type
        result = apply_unit_conversion(data, col_types, area_fact=0.1, vol_fact=0.5, len_fact=2.0)

        np.testing.assert_array_almost_equal(result, [[200.0]])


class TestDecodeHdf5String:
    """Tests for decode_hdf5_string function."""

    def test_import(self):
        """Test that function can be imported."""
        from iwfm.hdf5.hdf5_utils import decode_hdf5_string
        assert callable(decode_hdf5_string)

    def test_decode_bytes(self):
        """Test decoding bytes."""
        from iwfm.hdf5.hdf5_utils import decode_hdf5_string

        result = decode_hdf5_string(b'  test string  ')
        assert result == 'test string'

    def test_decode_string(self):
        """Test handling regular string."""
        from iwfm.hdf5.hdf5_utils import decode_hdf5_string

        result = decode_hdf5_string('  test string  ')
        assert result == 'test string'


class TestDecodeHdf5Strings:
    """Tests for decode_hdf5_strings function."""

    def test_import(self):
        """Test that function can be imported."""
        from iwfm.hdf5.hdf5_utils import decode_hdf5_strings
        assert callable(decode_hdf5_strings)

    def test_decode_list(self):
        """Test decoding list of bytes."""
        from iwfm.hdf5.hdf5_utils import decode_hdf5_strings

        result = decode_hdf5_strings([b'  one  ', b'two', b'  three'])
        assert result == ['one', 'two', 'three']


class TestParseIwfmDate:
    """Tests for parse_iwfm_date function."""

    def test_import(self):
        """Test that function can be imported."""
        from iwfm.hdf5.hdf5_utils import parse_iwfm_date
        assert callable(parse_iwfm_date)

    def test_parse_with_24_00(self):
        """Test parsing date with _24:00 (end of day)."""
        from iwfm.hdf5.hdf5_utils import parse_iwfm_date

        result = parse_iwfm_date('10/31/1973_24:00')
        assert result == datetime(1973, 11, 1)

    def test_parse_with_time(self):
        """Test parsing date with regular time."""
        from iwfm.hdf5.hdf5_utils import parse_iwfm_date

        result = parse_iwfm_date('10/31/1973_12:00')
        assert result == datetime(1973, 10, 31, 12, 0)

    def test_parse_date_only(self):
        """Test parsing date without time."""
        from iwfm.hdf5.hdf5_utils import parse_iwfm_date

        result = parse_iwfm_date('10/31/1973')
        assert result == datetime(1973, 10, 31)


class TestFormatIwfmDate:
    """Tests for format_iwfm_date function."""

    def test_import(self):
        """Test that function can be imported."""
        from iwfm.hdf5.hdf5_utils import format_iwfm_date
        assert callable(format_iwfm_date)

    def test_format(self):
        """Test formatting datetime."""
        from iwfm.hdf5.hdf5_utils import format_iwfm_date

        result = format_iwfm_date(datetime(1973, 10, 31))
        assert result == '10/31/1973_24:00'


class TestGenerateTimestepsFromHdf5:
    """Tests for generate_timesteps_from_hdf5 function."""

    def test_import(self):
        """Test that function can be imported."""
        from iwfm.hdf5.hdf5_utils import generate_timesteps_from_hdf5
        assert callable(generate_timesteps_from_hdf5)

    def test_monthly_timesteps(self):
        """Test generating monthly timesteps."""
        from iwfm.hdf5.hdf5_utils import generate_timesteps_from_hdf5

        result = generate_timesteps_from_hdf5('10/31/1973_24:00', 3, 1.0, '1MON')

        assert len(result) == 3
        assert result[0] == '11/01/1973_24:00'

    def test_daily_timesteps(self):
        """Test generating daily timesteps."""
        from iwfm.hdf5.hdf5_utils import generate_timesteps_from_hdf5

        result = generate_timesteps_from_hdf5('10/31/1973_24:00', 3, 1.0, 'DAY')

        assert len(result) == 3


class TestReadZoneDefinition:
    """Tests for read_zone_definition function."""

    def test_import(self):
        """Test that function can be imported."""
        from iwfm.hdf5.hdf5_utils import read_zone_definition
        assert callable(read_zone_definition)

    def test_read_zone_file(self, tmp_path):
        """Test reading zone definition file."""
        from iwfm.hdf5.hdf5_utils import read_zone_definition

        zone_file = tmp_path / "zones.dat"
        zone_file.write_text("""C Comment line
        1                       / ZEXTENT
C-------------------------------------------------------------------------------
C       ZID     ZNAME
C-------------------------------------------------------------------------------
	1	Zone One
	2	Zone Two
C-------------------------------------------------------------------------------
C       IE      ZONE
C-------------------------------------------------------------------------------
	1	1
	2	1
	3	2
""")

        zextent, zone_info, element_zones = read_zone_definition(str(zone_file))

        assert zextent == 1
        assert zone_info[1] == 'Zone One'
        assert zone_info[2] == 'Zone Two'
        assert element_zones[1] == 1
        assert element_zones[2] == 1
        assert element_zones[3] == 2


class TestGetUnitLabels:
    """Tests for get_unit_labels function."""

    def test_import(self):
        """Test that function can be imported."""
        from iwfm.hdf5.hdf5_utils import get_unit_labels
        assert callable(get_unit_labels)

    def test_acre_feet(self):
        """Test acre-feet volume label."""
        from iwfm.hdf5.hdf5_utils import get_unit_labels

        area_label, vol_label = get_unit_labels('ACRES', 'ACRE-FEET')

        assert area_label == 'AC'
        assert vol_label == 'AC.FT.'

    def test_custom_units(self):
        """Test custom unit labels."""
        from iwfm.hdf5.hdf5_utils import get_unit_labels

        area_label, vol_label = get_unit_labels('hectares', 'cubic meters')

        assert area_label == 'HECTARES'
        assert vol_label == 'CUBIC METERS'


class TestSubstituteTitlePlaceholders:
    """Tests for substitute_title_placeholders function."""

    def test_import(self):
        """Test that function can be imported."""
        from iwfm.hdf5.hdf5_utils import substitute_title_placeholders
        assert callable(substitute_title_placeholders)

    def test_substitution(self):
        """Test placeholder substitution."""
        from iwfm.hdf5.hdf5_utils import substitute_title_placeholders

        result = substitute_title_placeholders(
            'Budget for @LOCNAME@ Area: @AREA@ @UNITAR@ Volume: @UNITVL@',
            'Test Region',
            1234.56,
            'AC',
            'AF'
        )

        assert 'Test Region' in result
        assert '1,234.56' in result
        assert 'AC' in result
        assert 'AF' in result


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
