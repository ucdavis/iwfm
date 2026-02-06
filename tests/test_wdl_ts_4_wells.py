# test_wdl_ts_4_wells.py
# Unit tests for wdl_ts_4_wells.py - Write well data as time series
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


class TestWdlTs4Wells:
    """Tests for wdl_ts_4_wells function"""

    def test_basic_functionality(self, tmp_path):
        """Test basic functionality with matching station and water level data."""
        # Create station file (tab-delimited with header)
        station_file = tmp_path / 'stations.dat'
        station_content = (
            "STN_ID\tSITE_CODE\tSWN\n"
            "WELL001\tSC001\tSWN001\n"
            "WELL002\tSC002\tSWN002\n"
            "WELL003\tSC003\tSWN003\n"
        )
        station_file.write_text(station_content)

        # Create water level file with comma-separated data
        waterlevel_file = tmp_path / 'waterlevels.dat'
        waterlevel_content = (
            "WELL001,SC001,WLM001,01/15/2020,100.5,50.0,10.0,5.0,95.5,50.0,5.0,QA1,DESC1,ACC1,ORG1,ORG_NAME1,CMT1,COOP1,COOP_NAME1\n"
            "WELL002,SC002,WLM002,01/16/2020,101.2,51.0,11.0,6.0,95.2,51.0,6.0,QA2,DESC2,ACC2,ORG2,ORG_NAME2,CMT2,COOP2,COOP_NAME2\n"
            "WELL001,SC001,WLM003,01/17/2020,102.3,52.0,12.0,7.0,95.3,52.0,7.0,QA1,DESC1,ACC1,ORG1,ORG_NAME1,CMT3,COOP1,COOP_NAME1\n"
        )
        waterlevel_file.write_text(waterlevel_content)

        # Run the function
        iwfm.wdl_ts_4_wells(str(station_file), str(waterlevel_file), verbose=False)

        # Check output file exists
        output_file = tmp_path / 'stations_TS.out'
        assert output_file.exists(), "Output file was not created"

        # Read and verify output
        output_lines = output_file.read_text().strip().split('\n')
        
        # Should have header + 3 data lines
        assert len(output_lines) == 4, f"Expected 4 lines (header + 3 data), got {len(output_lines)}"

    def test_output_header_format(self, tmp_path):
        """Test that output file has correct header format."""
        station_file = tmp_path / 'stations.dat'
        station_content = (
            "STN_ID\tSITE_CODE\tSWN\n"
            "WELL001\tSC001\tSWN001\n"
        )
        station_file.write_text(station_content)

        waterlevel_file = tmp_path / 'waterlevels.dat'
        waterlevel_content = (
            "WELL001,SC001,WLM001,01/15/2020,100.5,50.0,10.0,5.0,95.5,50.0,5.0,QA1,DESC1,ACC1,ORG1,ORG_NAME1,CMT1,COOP1,COOP_NAME1\n"
        )
        waterlevel_file.write_text(waterlevel_content)

        iwfm.wdl_ts_4_wells(str(station_file), str(waterlevel_file), verbose=False)

        output_file = tmp_path / 'stations_TS.out'
        header = output_file.read_text().strip().split('\n')[0]

        # Verify header contains expected columns
        expected_columns = [
            'STN_ID', 'SITE_CODE', 'WLM_ID', 'MSMT_DATE', 'WLM_RPE', 'WLM_GSE',
            'RDNG_WS', 'RDNG_RP', 'WSE', 'RPE_GSE', 'GSE_WSE', 'WLM_QA_DESC',
            'WLM_DESC', 'WLM_ACC_DESC', 'WLM_ORG_ID', 'WLM_ORG_NAME', 'MSMT_CMT',
            'COOP_AGENCY_ORG_ID', 'COOP_ORG_NAME'
        ]
        for col in expected_columns:
            assert col in header, f"Header missing column: {col}"

    def test_filters_by_station_id(self, tmp_path):
        """Test that only water levels matching station IDs are written."""
        station_file = tmp_path / 'stations.dat'
        station_content = (
            "STN_ID\tSITE_CODE\tSWN\n"
            "WELL001\tSC001\tSWN001\n"
        )
        station_file.write_text(station_content)

        # Water level file with matching and non-matching station IDs
        waterlevel_file = tmp_path / 'waterlevels.dat'
        waterlevel_content = (
            "WELL001,SC001,WLM001,01/15/2020,100.5,50.0,10.0,5.0,95.5,50.0,5.0,QA1,DESC1,ACC1,ORG1,ORG_NAME1,CMT1,COOP1,COOP_NAME1\n"
            "WELL999,SC999,WLM999,01/16/2020,999.9,99.0,99.0,9.0,99.9,99.0,9.0,QA9,DESC9,ACC9,ORG9,ORG_NAME9,CMT9,COOP9,COOP_NAME9\n"
            "WELL001,SC001,WLM002,01/17/2020,102.3,52.0,12.0,7.0,95.3,52.0,7.0,QA1,DESC1,ACC1,ORG1,ORG_NAME1,CMT3,COOP1,COOP_NAME1\n"
        )
        waterlevel_file.write_text(waterlevel_content)

        iwfm.wdl_ts_4_wells(str(station_file), str(waterlevel_file), verbose=False)

        output_file = tmp_path / 'stations_TS.out'
        output_content = output_file.read_text()
        output_lines = output_content.strip().split('\n')

        # Should have header + 2 matching lines (WELL001 appears twice)
        assert len(output_lines) == 3, f"Expected 3 lines, got {len(output_lines)}"
        
        # WELL999 should NOT be in output
        assert 'WELL999' not in output_content, "Non-matching station WELL999 should not be in output"

    def test_no_matching_stations(self, tmp_path):
        """Test behavior when no water levels match any stations."""
        station_file = tmp_path / 'stations.dat'
        station_content = (
            "STN_ID\tSITE_CODE\tSWN\n"
            "WELL001\tSC001\tSWN001\n"
        )
        station_file.write_text(station_content)

        # Water level file with no matching station IDs
        waterlevel_file = tmp_path / 'waterlevels.dat'
        waterlevel_content = (
            "WELL999,SC999,WLM999,01/16/2020,999.9,99.0,99.0,9.0,99.9,99.0,9.0,QA9,DESC9,ACC9,ORG9,ORG_NAME9,CMT9,COOP9,COOP_NAME9\n"
        )
        waterlevel_file.write_text(waterlevel_content)

        iwfm.wdl_ts_4_wells(str(station_file), str(waterlevel_file), verbose=False)

        output_file = tmp_path / 'stations_TS.out'
        output_lines = output_file.read_text().strip().split('\n')

        # Should have only header (no data lines matched)
        assert len(output_lines) == 1, f"Expected only header, got {len(output_lines)} lines"

    def test_empty_water_level_file(self, tmp_path):
        """Test behavior with empty water level file."""
        station_file = tmp_path / 'stations.dat'
        station_content = (
            "STN_ID\tSITE_CODE\tSWN\n"
            "WELL001\tSC001\tSWN001\n"
        )
        station_file.write_text(station_content)

        # Empty water level file
        waterlevel_file = tmp_path / 'waterlevels.dat'
        waterlevel_file.write_text("")

        iwfm.wdl_ts_4_wells(str(station_file), str(waterlevel_file), verbose=False)

        output_file = tmp_path / 'stations_TS.out'
        assert output_file.exists(), "Output file should still be created"
        
        output_lines = output_file.read_text().strip().split('\n')
        # Should have only header
        assert len(output_lines) == 1

    def test_multiple_stations(self, tmp_path):
        """Test with multiple stations and matching water levels."""
        station_file = tmp_path / 'stations.dat'
        station_content = (
            "STN_ID\tSITE_CODE\tSWN\n"
            "WELL001\tSC001\tSWN001\n"
            "WELL002\tSC002\tSWN002\n"
            "WELL003\tSC003\tSWN003\n"
        )
        station_file.write_text(station_content)

        waterlevel_file = tmp_path / 'waterlevels.dat'
        waterlevel_content = (
            "WELL001,SC001,WLM001,01/15/2020,100.5,50.0,10.0,5.0,95.5,50.0,5.0,QA1,DESC1,ACC1,ORG1,ORG_NAME1,CMT1,COOP1,COOP_NAME1\n"
            "WELL002,SC002,WLM002,01/16/2020,101.2,51.0,11.0,6.0,95.2,51.0,6.0,QA2,DESC2,ACC2,ORG2,ORG_NAME2,CMT2,COOP2,COOP_NAME2\n"
            "WELL003,SC003,WLM003,01/17/2020,102.3,52.0,12.0,7.0,95.3,52.0,7.0,QA3,DESC3,ACC3,ORG3,ORG_NAME3,CMT3,COOP3,COOP_NAME3\n"
        )
        waterlevel_file.write_text(waterlevel_content)

        iwfm.wdl_ts_4_wells(str(station_file), str(waterlevel_file), verbose=False)

        output_file = tmp_path / 'stations_TS.out'
        output_content = output_file.read_text()

        # All three wells should be in output
        assert 'WELL001' in output_content
        assert 'WELL002' in output_content
        assert 'WELL003' in output_content

    def test_verbose_output(self, tmp_path, capsys):
        """Test verbose output displays processing information."""
        station_file = tmp_path / 'stations.dat'
        station_content = (
            "STN_ID\tSITE_CODE\tSWN\n"
            "WELL001\tSC001\tSWN001\n"
            "WELL002\tSC002\tSWN002\n"
        )
        station_file.write_text(station_content)

        waterlevel_file = tmp_path / 'waterlevels.dat'
        waterlevel_content = (
            "WELL001,SC001,WLM001,01/15/2020,100.5,50.0,10.0,5.0,95.5,50.0,5.0,QA1,DESC1,ACC1,ORG1,ORG_NAME1,CMT1,COOP1,COOP_NAME1\n"
            "WELL002,SC002,WLM002,01/16/2020,101.2,51.0,11.0,6.0,95.2,51.0,6.0,QA2,DESC2,ACC2,ORG2,ORG_NAME2,CMT2,COOP2,COOP_NAME2\n"
        )
        waterlevel_file.write_text(waterlevel_content)

        iwfm.wdl_ts_4_wells(str(station_file), str(waterlevel_file), verbose=True)

        captured = capsys.readouterr()
        
        # Verbose output should show station count
        assert 'Read' in captured.out
        assert 'stations' in captured.out
        # Should show lines processed
        assert 'Processed' in captured.out
        assert 'lines' in captured.out
        # Should show lines written
        assert 'Wrote' in captured.out

    def test_output_filename_based_on_station_file(self, tmp_path):
        """Test that output filename is based on station file basename."""
        station_file = tmp_path / 'my_custom_stations.dat'
        station_content = (
            "STN_ID\tSITE_CODE\tSWN\n"
            "WELL001\tSC001\tSWN001\n"
        )
        station_file.write_text(station_content)

        waterlevel_file = tmp_path / 'waterlevels.dat'
        waterlevel_content = (
            "WELL001,SC001,WLM001,01/15/2020,100.5,50.0,10.0,5.0,95.5,50.0,5.0,QA1,DESC1,ACC1,ORG1,ORG_NAME1,CMT1,COOP1,COOP_NAME1\n"
        )
        waterlevel_file.write_text(waterlevel_content)

        iwfm.wdl_ts_4_wells(str(station_file), str(waterlevel_file), verbose=False)

        # Output should be named based on station file
        expected_output = tmp_path / 'my_custom_stations_TS.out'
        assert expected_output.exists(), f"Expected output file: {expected_output}"

    def test_short_lines_ignored(self, tmp_path):
        """Test that short lines (<=10 chars) are ignored."""
        station_file = tmp_path / 'stations.dat'
        station_content = (
            "STN_ID\tSITE_CODE\tSWN\n"
            "WELL001\tSC001\tSWN001\n"
        )
        station_file.write_text(station_content)

        waterlevel_file = tmp_path / 'waterlevels.dat'
        waterlevel_content = (
            "short\n"  # Short line should be ignored
            "WELL001,SC001,WLM001,01/15/2020,100.5,50.0,10.0,5.0,95.5,50.0,5.0,QA1,DESC1,ACC1,ORG1,ORG_NAME1,CMT1,COOP1,COOP_NAME1\n"
            "x\n"  # Another short line
        )
        waterlevel_file.write_text(waterlevel_content)

        iwfm.wdl_ts_4_wells(str(station_file), str(waterlevel_file), verbose=False)

        output_file = tmp_path / 'stations_TS.out'
        output_lines = output_file.read_text().strip().split('\n')

        # Should have header + 1 valid data line
        assert len(output_lines) == 2, f"Expected 2 lines (header + 1 data), got {len(output_lines)}"

    def test_station_dictionary_creation(self, tmp_path):
        """Test that station dictionary is correctly created from tab-delimited file."""
        station_file = tmp_path / 'stations.dat'
        # Tab-delimited station file
        station_content = (
            "STN_ID\tSITE_CODE\tSWN\n"
            "WELL_A\tCODE_A\tSWN_A\n"
            "WELL_B\tCODE_B\tSWN_B\n"
        )
        station_file.write_text(station_content)

        waterlevel_file = tmp_path / 'waterlevels.dat'
        waterlevel_content = (
            "WELL_A,CODE_A,WLM001,01/15/2020,100.5,50.0,10.0,5.0,95.5,50.0,5.0,QA1,DESC1,ACC1,ORG1,ORG_NAME1,CMT1,COOP1,COOP_NAME1\n"
        )
        waterlevel_file.write_text(waterlevel_content)

        iwfm.wdl_ts_4_wells(str(station_file), str(waterlevel_file), verbose=False)

        output_file = tmp_path / 'stations_TS.out'
        output_content = output_file.read_text()

        assert 'WELL_A' in output_content

    def test_return_value(self, tmp_path):
        """Test that function returns None (no return value)."""
        station_file = tmp_path / 'stations.dat'
        station_content = (
            "STN_ID\tSITE_CODE\tSWN\n"
            "WELL001\tSC001\tSWN001\n"
        )
        station_file.write_text(station_content)

        waterlevel_file = tmp_path / 'waterlevels.dat'
        waterlevel_content = (
            "WELL001,SC001,WLM001,01/15/2020,100.5,50.0,10.0,5.0,95.5,50.0,5.0,QA1,DESC1,ACC1,ORG1,ORG_NAME1,CMT1,COOP1,COOP_NAME1\n"
        )
        waterlevel_file.write_text(waterlevel_content)

        result = iwfm.wdl_ts_4_wells(str(station_file), str(waterlevel_file), verbose=False)

        assert result is None


class TestWdlTs4WellsEdgeCases:
    """Edge case tests for wdl_ts_4_wells function"""

    def test_station_id_with_special_characters(self, tmp_path):
        """Test station IDs containing special characters."""
        station_file = tmp_path / 'stations.dat'
        station_content = (
            "STN_ID\tSITE_CODE\tSWN\n"
            "S_380313N1219426W001\tSC001\tSWN001\n"
        )
        station_file.write_text(station_content)

        waterlevel_file = tmp_path / 'waterlevels.dat'
        waterlevel_content = (
            "S_380313N1219426W001,SC001,WLM001,01/15/2020,100.5,50.0,10.0,5.0,95.5,50.0,5.0,QA1,DESC1,ACC1,ORG1,ORG_NAME1,CMT1,COOP1,COOP_NAME1\n"
        )
        waterlevel_file.write_text(waterlevel_content)

        iwfm.wdl_ts_4_wells(str(station_file), str(waterlevel_file), verbose=False)

        output_file = tmp_path / 'stations_TS.out'
        output_content = output_file.read_text()

        assert 'S_380313N1219426W001' in output_content

    def test_many_stations(self, tmp_path):
        """Test with large number of stations."""
        station_file = tmp_path / 'stations.dat'
        
        # Build station content
        station_lines = ["STN_ID\tSITE_CODE\tSWN"]
        for i in range(100):
            station_lines.append(f"WELL{i:03d}\tSC{i:03d}\tSWN{i:03d}")
        station_file.write_text('\n'.join(station_lines) + '\n')

        waterlevel_file = tmp_path / 'waterlevels.dat'
        
        # Build water level content with subset of wells
        wl_lines = []
        for i in range(0, 100, 10):  # Every 10th well
            wl_lines.append(
                f"WELL{i:03d},SC{i:03d},WLM{i:03d},01/15/2020,100.5,50.0,10.0,5.0,95.5,50.0,5.0,QA1,DESC1,ACC1,ORG1,ORG_NAME1,CMT1,COOP1,COOP_NAME1"
            )
        waterlevel_file.write_text('\n'.join(wl_lines) + '\n')

        iwfm.wdl_ts_4_wells(str(station_file), str(waterlevel_file), verbose=False)

        output_file = tmp_path / 'stations_TS.out'
        output_lines = output_file.read_text().strip().split('\n')

        # Should have header + 10 data lines
        assert len(output_lines) == 11

    def test_single_station_single_record(self, tmp_path):
        """Test minimal case with single station and single water level record."""
        station_file = tmp_path / 'stations.dat'
        station_content = (
            "STN_ID\tSITE_CODE\tSWN\n"
            "ONLY_WELL\tONLY_CODE\tONLY_SWN\n"
        )
        station_file.write_text(station_content)

        waterlevel_file = tmp_path / 'waterlevels.dat'
        waterlevel_content = (
            "ONLY_WELL,ONLY_CODE,WLM001,01/15/2020,100.5,50.0,10.0,5.0,95.5,50.0,5.0,QA1,DESC1,ACC1,ORG1,ORG_NAME1,CMT1,COOP1,COOP_NAME1\n"
        )
        waterlevel_file.write_text(waterlevel_content)

        iwfm.wdl_ts_4_wells(str(station_file), str(waterlevel_file), verbose=False)

        output_file = tmp_path / 'stations_TS.out'
        output_lines = output_file.read_text().strip().split('\n')

        assert len(output_lines) == 2  # header + 1 data line
        assert 'ONLY_WELL' in output_lines[1]


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
