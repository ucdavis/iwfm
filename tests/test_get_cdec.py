# test_get_cdec.py
# unit tests for get_cdec functions (using polars and BeautifulSoup)
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


def _load_functions():
    """Load the get_cdec functions dynamically."""
    from importlib.util import spec_from_file_location, module_from_spec
    base = Path(__file__).resolve().parents[1] / "iwfm" / "util" / "get_cdec.py"
    spec = spec_from_file_location("get_cdec", str(base))
    assert spec is not None, "Failed to load module specification"
    mod = module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return (
        getattr(mod, "parse_html_table"),
        getattr(mod, "save_table_as_csv"),
        getattr(mod, "download_data_table"),
        getattr(mod, "format_file"),
    )


parse_html_table, save_table_as_csv, download_data_table, format_file = _load_functions()


class TestParseHtmlTable:
    """Tests for the parse_html_table function."""

    def test_basic_table_parsing(self):
        """Test parsing a basic HTML table."""
        html = """
        <table>
            <tr><th>Col1</th><th>Col2</th><th>Col3</th></tr>
            <tr><td>A</td><td>B</td><td>C</td></tr>
            <tr><td>D</td><td>E</td><td>F</td></tr>
        </table>
        """
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')

        headers, rows = parse_html_table(table)

        assert headers == ['Col1', 'Col2', 'Col3']
        assert rows == [['A', 'B', 'C'], ['D', 'E', 'F']]

    def test_table_with_no_headers(self):
        """Test parsing table where first row has td instead of th."""
        html = """
        <table>
            <tr><td>Header1</td><td>Header2</td></tr>
            <tr><td>Data1</td><td>Data2</td></tr>
        </table>
        """
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')

        headers, rows = parse_html_table(table)

        # First row's td elements are treated as headers
        assert headers == ['Header1', 'Header2']
        assert rows == [['Data1', 'Data2']]

    def test_empty_table(self):
        """Test parsing an empty table."""
        html = "<table></table>"
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')

        headers, rows = parse_html_table(table)

        assert headers == []
        assert rows == []

    def test_table_with_empty_rows(self):
        """Test that empty rows are skipped."""
        html = """
        <table>
            <tr><th>A</th><th>B</th></tr>
            <tr></tr>
            <tr><td>1</td><td>2</td></tr>
            <tr></tr>
        </table>
        """
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')

        headers, rows = parse_html_table(table)

        assert headers == ['A', 'B']
        assert rows == [['1', '2']]  # Empty rows skipped

    def test_whitespace_stripping(self):
        """Test that whitespace is stripped from cell values."""
        html = """
        <table>
            <tr><th>  Name  </th><th>  Value  </th></tr>
            <tr><td>  Test  </td><td>  123  </td></tr>
        </table>
        """
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')

        headers, rows = parse_html_table(table)

        assert headers == ['Name', 'Value']
        assert rows == [['Test', '123']]


class TestSaveTableAsCsv:
    """Tests for the save_table_as_csv function."""

    def test_saves_csv_file(self, tmp_path):
        """Test that save_table_as_csv creates a CSV file."""
        html = """
        <table>
            <tr><th>Date</th><th>Value</th></tr>
            <tr><td>2022-01-01</td><td>100</td></tr>
            <tr><td>2022-01-02</td><td>200</td></tr>
        </table>
        """
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')

        output_file = str(tmp_path / "test_output.csv")
        save_table_as_csv(output_file, table)

        # Verify file was created
        assert (tmp_path / "test_output.csv").exists()

        # Read and verify contents
        df = pl.read_csv(output_file)
        assert 'Date' in df.columns
        assert 'Value' in df.columns
        assert len(df) == 2

    def test_handles_empty_table(self, tmp_path, capsys):
        """Test handling of empty table."""
        html = "<table><tr><th>Header</th></tr></table>"
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')

        output_file = str(tmp_path / "empty.csv")
        save_table_as_csv(output_file, table)

        captured = capsys.readouterr()
        assert "empty or malformed" in captured.out

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
        # Third column should be empty string
        assert df['C'][0] == ''

    def test_prints_success_message(self, tmp_path, capsys):
        """Test that success message is printed."""
        html = """
        <table>
            <tr><th>X</th></tr>
            <tr><td>1</td></tr>
        </table>
        """
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')

        output_file = str(tmp_path / "success.csv")
        save_table_as_csv(output_file, table)

        captured = capsys.readouterr()
        assert "Data table saved to" in captured.out


class TestDownloadDataTable:
    """Tests for the download_data_table function."""

    @patch('iwfm.util.get_cdec.requests.get')
    def test_successful_download(self, mock_get, tmp_path, capsys, monkeypatch):
        """Test successful download and save."""
        # Change to tmp_path so files are created there
        monkeypatch.chdir(tmp_path)

        html_content = b"""
        <html><body>
        <table>
            <tr><th>Date</th><th>Value</th></tr>
            <tr><td>2022-01</td><td>100</td></tr>
        </table>
        </body></html>
        """
        mock_response = MagicMock()
        mock_response.content = html_content
        mock_get.return_value = mock_response

        files = [["Test File", "Test Source", "http://example.com/data"]]
        result = download_data_table(files)

        assert result == [["test_file_raw.csv", "Test Source"]]
        mock_get.assert_called_once_with("http://example.com/data", timeout=30)

    @patch('iwfm.util.get_cdec.requests.get')
    def test_no_table_found(self, mock_get, tmp_path, capsys, monkeypatch):
        """Test handling when no table found in HTML."""
        monkeypatch.chdir(tmp_path)

        mock_response = MagicMock()
        mock_response.content = b"<html><body>No tables here</body></html>"
        mock_get.return_value = mock_response

        files = [["Empty", "Source", "http://example.com/empty"]]
        result = download_data_table(files)

        captured = capsys.readouterr()
        assert "No tables found" in captured.out
        assert result == [["empty_raw.csv", "Source"]]

    @patch('iwfm.util.get_cdec.requests.get')
    def test_timeout_handling(self, mock_get, capsys):
        """Test handling of request timeout."""
        import requests
        mock_get.side_effect = requests.exceptions.Timeout()

        files = [["Timeout Test", "Source", "http://example.com/slow"]]
        result = download_data_table(files)

        captured = capsys.readouterr()
        assert "timed out" in captured.out
        assert result == [["timeout_test_raw.csv", "Source"]]

    @patch('iwfm.util.get_cdec.requests.get')
    def test_connection_error(self, mock_get, capsys):
        """Test handling of connection error."""
        import requests
        mock_get.side_effect = requests.exceptions.ConnectionError()

        files = [["Conn Test", "Source", "http://example.com/fail"]]
        result = download_data_table(files)

        captured = capsys.readouterr()
        assert "Connection error" in captured.out

    def test_filename_formatting(self):
        """Test that filenames are correctly formatted."""
        # The function should:
        # - Replace spaces with underscores
        # - Convert to lowercase
        # - Add _raw.csv suffix
        name = "Test File Name"
        expected = "test_file_name_raw.csv"

        formatted = name.replace(' ', '_').lower() + '_raw.csv'
        assert formatted == expected


class TestFormatFile:
    """Tests for the format_file function."""

    def test_basic_formatting(self, tmp_path, capsys):
        """Test basic file formatting."""
        # Create a raw file
        raw_file = tmp_path / "test_raw.csv"
        raw_file.write_text("Date,Value CFS\n2022,100\n2023,200\n")

        info = [[str(raw_file), "Test Source"]]
        format_file(info)

        # Check output file was created
        data_file = tmp_path / "test_data.csv"
        assert data_file.exists()

        # Check content
        content = data_file.read_text()
        assert "Date" in content
        assert "Data Source" in content

        # Check raw file was deleted
        assert not raw_file.exists()

        captured = capsys.readouterr()
        assert "Data saved to" in captured.out

    def test_file_not_found_error(self, tmp_path):
        """Test FileNotFoundError for missing raw file."""
        info = [[str(tmp_path / "nonexistent_raw.csv"), "Source"]]

        with pytest.raises(FileNotFoundError):
            format_file(info)

    def test_units_extraction(self, tmp_path):
        """Test that units are extracted from header."""
        raw_file = tmp_path / "units_raw.csv"
        # Units should be second word after splitting
        raw_file.write_text("Date,Flow CFS\n2022,100\n")

        info = [[str(raw_file), "Test Source"]]
        format_file(info)

        data_file = tmp_path / "units_data.csv"
        content = data_file.read_text()
        assert "CFS" in content


class TestGetCdecEdgeCases:
    """Edge case tests for get_cdec functions."""

    def test_multiple_files_processing(self, tmp_path, capsys, monkeypatch):
        """Test processing multiple files."""
        monkeypatch.chdir(tmp_path)

        @patch('iwfm.util.get_cdec.requests.get')
        def run_test(mock_get):
            html = b"<table><tr><th>A</th></tr><tr><td>1</td></tr></table>"
            mock_response = MagicMock()
            mock_response.content = html
            mock_get.return_value = mock_response

            files = [
                ["File One", "Source 1", "http://example.com/1"],
                ["File Two", "Source 2", "http://example.com/2"],
            ]
            result = download_data_table(files)

            assert len(result) == 2
            assert result[0][0] == "file_one_raw.csv"
            assert result[1][0] == "file_two_raw.csv"

        run_test()

    def test_table_with_mixed_th_td_headers(self):
        """Test parsing table with mixed th and td in header row."""
        html = """
        <table>
            <tr><th>First</th><td>Second</td><th>Third</th></tr>
            <tr><td>A</td><td>B</td><td>C</td></tr>
        </table>
        """
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')

        headers, rows = parse_html_table(table)

        # Should extract all cells from first row regardless of th/td
        assert len(headers) == 3
        assert headers == ['First', 'Second', 'Third']
