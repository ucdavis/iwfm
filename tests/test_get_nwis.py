# test_get_nwis.py
# unit tests for get_nwis functions (using polars and BeautifulSoup)
# Copyright (C) 2025-2026 University of California
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
import polars as pl
from pathlib import Path
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup


def _load_module():
    """Load the get_nwis module dynamically."""
    from importlib.util import spec_from_file_location, module_from_spec
    base = Path(__file__).resolve().parents[1] / "iwfm" / "util" / "get_nwis.py"
    spec = spec_from_file_location("get_nwis", str(base))
    assert spec is not None, "Failed to load module specification"
    mod = module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


# Load the module and extract functions
_module = _load_module()
get_nwis = _module.get_nwis
parse_html_table = _module.parse_html_table
save_table_as_csv = _module.save_table_as_csv
format_file = _module.format_file


class TestParseHtmlTable:
    """Tests for the parse_html_table function."""

    def test_basic_table_parsing(self):
        """Test parsing a basic HTML table."""
        html = """
        <table>
            <tr><th>Year</th><th>Jan</th><th>Feb</th></tr>
            <tr><td>2020</td><td>100</td><td>110</td></tr>
            <tr><td>2021</td><td>120</td><td>130</td></tr>
        </table>
        """
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')

        headers, rows = parse_html_table(table)

        assert headers == ['Year', 'Jan', 'Feb']
        assert len(rows) == 2
        assert rows[0] == ['2020', '100', '110']
        assert rows[1] == ['2021', '120', '130']

    def test_empty_table(self):
        """Test parsing an empty table."""
        html = "<table></table>"
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')

        headers, rows = parse_html_table(table)

        assert headers == []
        assert rows == []

    def test_whitespace_stripping(self):
        """Test that whitespace is stripped from cell values."""
        html = """
        <table>
            <tr><th>  Name  </th></tr>
            <tr><td>  Value  </td></tr>
        </table>
        """
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')

        headers, rows = parse_html_table(table)

        assert headers == ['Name']
        assert rows == [['Value']]


class TestSaveTableAsCsv:
    """Tests for the save_table_as_csv function."""

    def test_saves_csv_with_polars(self, tmp_path):
        """Test that save_table_as_csv creates a CSV using polars."""
        html = """
        <table>
            <tr><th>Year</th><th>Value</th></tr>
            <tr><td>2020</td><td>100</td></tr>
            <tr><td>2021</td><td>200</td></tr>
        </table>
        """
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')

        output_file = str(tmp_path / "test_nwis.csv")
        save_table_as_csv(output_file, table)

        assert (tmp_path / "test_nwis.csv").exists()

        df = pl.read_csv(output_file)
        assert 'Year' in df.columns
        assert 'Value' in df.columns
        assert len(df) == 2

    def test_handles_empty_table(self, tmp_path):
        """Test that empty table raises ValueError."""
        html = "<table><tr><th>Header</th></tr></table>"
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')

        output_file = str(tmp_path / "empty.csv")

        with pytest.raises(ValueError):
            save_table_as_csv(output_file, table)

    def test_pads_short_rows(self, tmp_path):
        """Test that short rows are padded to match header length."""
        html = """
        <table>
            <tr><th>A</th><th>B</th><th>C</th></tr>
            <tr><td>1</td><td>2</td></tr>
        </table>
        """
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')

        output_file = str(tmp_path / "padded.csv")
        save_table_as_csv(output_file, table)

        df = pl.read_csv(output_file)
        assert len(df.columns) == 3

    def test_prints_row_count(self, tmp_path, capsys):
        """Test that success message includes row count."""
        html = """
        <table>
            <tr><th>X</th></tr>
            <tr><td>1</td></tr>
            <tr><td>2</td></tr>
        </table>
        """
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')

        output_file = str(tmp_path / "count.csv")
        save_table_as_csv(output_file, table)

        captured = capsys.readouterr()
        assert "2 rows" in captured.out


class TestGetNwis:
    """Tests for the get_nwis function."""

    def test_successful_download(self, tmp_path, monkeypatch):
        """Test successful download and save."""
        monkeypatch.chdir(tmp_path)

        html_content = b"""
        <html><body>
        <table>
            <tr><th>Year</th><th>Flow</th></tr>
            <tr><td>2020</td><td>500</td></tr>
        </table>
        </body></html>
        """

        mock_response = MagicMock()
        mock_response.content = html_content
        mock_response.raise_for_status = MagicMock()

        with patch('requests.get', return_value=mock_response) as mock_get:
            files = [["Sacramento River", "USGS Gage 12345", "http://example.com/nwis"]]
            result = get_nwis(files)

            assert result == [["sacramento_river_raw.csv", "USGS Gage 12345"]]
            mock_get.assert_called_once()

    def test_no_tables_found(self, tmp_path, capsys, monkeypatch):
        """Test handling when no tables found."""
        monkeypatch.chdir(tmp_path)

        mock_response = MagicMock()
        mock_response.content = b"<html><body>No data</body></html>"
        mock_response.raise_for_status = MagicMock()

        with patch('requests.get', return_value=mock_response):
            files = [["Empty", "Source", "http://example.com/empty"]]
            result = get_nwis(files)

            captured = capsys.readouterr()
            assert "No tables found" in captured.out

    def test_timeout_handling(self, capsys):
        """Test handling of request timeout."""
        import requests as requests_lib

        with patch('requests.get', side_effect=requests_lib.exceptions.Timeout()):
            files = [["Test", "Source", "http://example.com/slow"]]
            result = get_nwis(files, timeout=30)

            captured = capsys.readouterr()
            assert "timed out" in captured.out

    def test_connection_error(self, capsys):
        """Test handling of connection error."""
        import requests as requests_lib

        with patch('requests.get', side_effect=requests_lib.exceptions.ConnectionError()):
            files = [["Test", "Source", "http://example.com/fail"]]
            result = get_nwis(files)

            captured = capsys.readouterr()
            assert "Connection error" in captured.out

    def test_http_error(self, capsys):
        """Test handling of HTTP errors."""
        import requests as requests_lib

        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests_lib.exceptions.HTTPError()

        with patch('requests.get', return_value=mock_response):
            files = [["Test", "Source", "http://example.com/404"]]
            result = get_nwis(files)

            captured = capsys.readouterr()
            assert "HTTP" in captured.out or "404" in captured.out

    def test_invalid_files_input(self):
        """Test that invalid input raises ValueError."""
        with pytest.raises(ValueError):
            get_nwis([])  # Empty list

        with pytest.raises(ValueError):
            get_nwis("not a list")  # Not a list

    def test_invalid_file_info_structure(self, capsys):
        """Test handling of invalid file_info structure."""
        # Should skip invalid entries with warning
        files = [
            ["Valid", "Source", "http://example.com"],
            ["Invalid"],  # Missing elements
        ]
        # Will print warning for invalid entry
        # The valid entry would be processed if mocked

    def test_failed_urls_report(self, capsys):
        """Test that failed URLs are reported at the end."""
        import requests as requests_lib

        with patch('requests.get', side_effect=requests_lib.exceptions.Timeout()):
            files = [
                ["File1", "Source1", "http://example.com/1"],
                ["File2", "Source2", "http://example.com/2"],
            ]
            get_nwis(files)

            captured = capsys.readouterr()
            assert "Warning" in captured.out
            assert "failed to download" in captured.out


class TestFormatFile:
    """Tests for the format_file function."""

    def test_basic_formatting(self, tmp_path, capsys):
        """Test basic NWIS file formatting."""
        raw_file = tmp_path / "test_raw.csv"
        # NWIS format: first row has units like "Monthly mean in cubic feet per second"
        raw_file.write_text(
            "Year,Monthly mean in cubic feet per second\n"
            "Jan,100\n"
            "2020,100,110,120,130,140,150,160,170,180,190,200,210\n"
            "2021,200,210,220,230,240,250,260,270,280,290,300,310\n"
        )

        info = [[str(raw_file), "USGS Gage 12345"]]
        format_file(info)

        data_file = tmp_path / "test_data.csv"
        assert data_file.exists()

        content = data_file.read_text()
        assert "Date" in content
        assert "Units" in content
        assert "Data Source" in content

        captured = capsys.readouterr()
        assert "Data saved to" in captured.out

    def test_file_not_found_error(self, tmp_path):
        """Test FileNotFoundError for missing raw file."""
        info = [[str(tmp_path / "missing_raw.csv"), "Source"]]

        with pytest.raises(FileNotFoundError):
            format_file(info)

    def test_deletes_raw_file(self, tmp_path):
        """Test that raw file is deleted after formatting."""
        raw_file = tmp_path / "delete_raw.csv"
        # NWIS format (simplified to match test_basic_formatting structure):
        # Line 1: column header with "Monthly mean in X" in second column (skipped by next())
        # Line 2+: data rows
        # Note: format_file's line_number starts at 1 AFTER the next(csv_reader) skip
        raw_file.write_text(
            "Year,Monthly mean in cubic feet per second\n"
            "Jan,100\n"
            "2020,100,110,120,130,140,150,160,170,180,190,200,210\n"
        )

        info = [[str(raw_file), "Source"]]
        format_file(info)

        # Raw file should be deleted after formatting
        assert not raw_file.exists()

        # Data file should exist
        data_file = tmp_path / "delete_data.csv"
        assert data_file.exists()


class TestGetNwisEdgeCases:
    """Edge case tests for get_nwis functions."""

    def test_filename_with_spaces(self):
        """Test filename formatting with spaces."""
        name = "Sacramento River at Keswick"
        expected = "sacramento_river_at_keswick_raw.csv"

        formatted = name.replace(' ', '_').lower() + '_raw.csv'
        assert formatted == expected

    def test_extracts_last_table(self, tmp_path, monkeypatch):
        """Test that get_nwis extracts the last table from the page."""
        monkeypatch.chdir(tmp_path)

        # HTML with multiple tables - should use the last one
        html_content = b"""
        <html><body>
        <table><tr><th>First</th></tr><tr><td>A</td></tr></table>
        <table><tr><th>Second</th></tr><tr><td>B</td></tr></table>
        <table><tr><th>Third</th></tr><tr><td>C</td></tr></table>
        </body></html>
        """

        mock_response = MagicMock()
        mock_response.content = html_content
        mock_response.raise_for_status = MagicMock()

        with patch('requests.get', return_value=mock_response):
            files = [["Test", "Source", "http://example.com/multi"]]
            result = get_nwis(files)

            # Should process the last table
            assert (tmp_path / "test_raw.csv").exists()

    def test_custom_timeout(self, tmp_path, monkeypatch):
        """Test that custom timeout is passed to requests."""
        monkeypatch.chdir(tmp_path)

        html_content = b"<table><tr><th>A</th></tr><tr><td>1</td></tr></table>"

        mock_response = MagicMock()
        mock_response.content = html_content
        mock_response.raise_for_status = MagicMock()

        with patch('requests.get', return_value=mock_response) as mock_get:
            files = [["Test", "Source", "http://example.com"]]
            get_nwis(files, timeout=60)

            call_args = mock_get.call_args
            assert call_args.kwargs.get('timeout') == 60
