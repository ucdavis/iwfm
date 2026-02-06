# test_pdf2csv.py
# unit tests for pdf2csv function
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
import subprocess

import pytest


def tabula_py_available():
    """Check if tabula-py is installed with convert_into available."""
    try:
        from tabula.io import convert_into  # noqa: F401
        del convert_into
        return True
    except ImportError:
        return False


def java_available():
    """Check if Java is available (required for tabula-py)."""
    try:
        result = subprocess.run(
            ['java', '-version'],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0
    except (subprocess.SubprocessError, FileNotFoundError, OSError):
        return False


# Mark for skipping tests that require real tabula-py and Java
requires_tabula = pytest.mark.skipif(
    not tabula_py_available() or not java_available(),
    reason="tabula-py library not available or Java not installed"
)

import iwfm


def create_pdf_with_table(filepath):
    """Helper to create a PDF with a simple table using fpdf."""
    try:
        import fpdf
    except ImportError:
        pytest.skip("fpdf library not installed")

    pdf = fpdf.FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)

    # Create a simple table
    col_width = 40
    row_height = 10

    # Header row
    headers = ['Name', 'Value', 'Unit']
    for header in headers:
        pdf.cell(col_width, row_height, header, border=1, align='C')
    pdf.ln()

    # Data rows
    pdf.set_font('Arial', '', 12)
    data = [
        ['Flow', '100.5', 'cfs'],
        ['Head', '250.3', 'ft'],
        ['Storage', '5000', 'af'],
    ]
    for row in data:
        for item in row:
            pdf.cell(col_width, row_height, item, border=1, align='C')
        pdf.ln()

    pdf.output(str(filepath))


@requires_tabula
class TestPdf2csv:
    """Tests for the pdf2csv function (requires tabula-py and Java)."""

    def test_basic_conversion(self, tmp_path):
        """Test basic PDF to CSV conversion."""
        # Create PDF with table
        input_file = tmp_path / "test_table.pdf"
        create_pdf_with_table(input_file)

        output_file = tmp_path / "output.csv"
        log_file = tmp_path / "test.log"

        # Run conversion
        iwfm.pdf2csv(str(input_file), str(output_file), log_file=str(log_file))

        # Check output file was created
        assert output_file.exists()

    def test_output_file_created(self, tmp_path):
        """Test that output CSV file is created."""
        input_file = tmp_path / "test.pdf"
        create_pdf_with_table(input_file)

        output_file = tmp_path / "result.csv"
        log_file = tmp_path / "test.log"

        iwfm.pdf2csv(str(input_file), str(output_file), log_file=str(log_file))

        assert output_file.exists()
        assert output_file.stat().st_size > 0

    def test_verbose_output(self, tmp_path, capsys):
        """Test verbose output shows conversion message."""
        input_file = tmp_path / "test.pdf"
        create_pdf_with_table(input_file)

        output_file = tmp_path / "output.csv"
        log_file = tmp_path / "test.log"

        iwfm.pdf2csv(
            str(input_file),
            str(output_file),
            verbose=True,
            log_file=str(log_file)
        )

        captured = capsys.readouterr()
        assert 'test.pdf' in captured.out
        assert 'output.csv' in captured.out

    def test_no_verbose_output(self, tmp_path, capsys):
        """Test that verbose=False produces no output."""
        input_file = tmp_path / "test.pdf"
        create_pdf_with_table(input_file)

        output_file = tmp_path / "output.csv"
        log_file = tmp_path / "test.log"

        iwfm.pdf2csv(
            str(input_file),
            str(output_file),
            verbose=False,
            log_file=str(log_file)
        )

        captured = capsys.readouterr()
        assert captured.out == ''

    def test_returns_none(self, tmp_path):
        """Test that function returns None."""
        input_file = tmp_path / "test.pdf"
        create_pdf_with_table(input_file)

        output_file = tmp_path / "output.csv"
        log_file = tmp_path / "test.log"

        result = iwfm.pdf2csv(
            str(input_file),
            str(output_file),
            log_file=str(log_file)
        )

        assert result is None

    def test_custom_log_file(self, tmp_path):
        """Test that custom log file is used."""
        input_file = tmp_path / "test.pdf"
        create_pdf_with_table(input_file)

        output_file = tmp_path / "output.csv"
        log_file = tmp_path / "custom_log.log"

        iwfm.pdf2csv(
            str(input_file),
            str(output_file),
            log_file=str(log_file)
        )

        # Log file may or may not be created depending on whether warnings occurred
        # Just verify no exception was raised
        assert output_file.exists()

    def test_nonexistent_input_file_raises_error(self, tmp_path):
        """Test that nonexistent input file raises an error."""
        input_file = tmp_path / "nonexistent.pdf"
        output_file = tmp_path / "output.csv"
        log_file = tmp_path / "test.log"

        with pytest.raises(Exception):
            iwfm.pdf2csv(
                str(input_file),
                str(output_file),
                log_file=str(log_file)
            )

    def test_output_to_subdirectory(self, tmp_path):
        """Test writing output to subdirectory."""
        input_file = tmp_path / "test.pdf"
        create_pdf_with_table(input_file)

        subdir = tmp_path / "output_dir"
        subdir.mkdir()
        output_file = subdir / "output.csv"
        log_file = tmp_path / "test.log"

        iwfm.pdf2csv(
            str(input_file),
            str(output_file),
            log_file=str(log_file)
        )

        assert output_file.exists()

    def test_csv_extension(self, tmp_path):
        """Test output file with .csv extension."""
        input_file = tmp_path / "test.pdf"
        create_pdf_with_table(input_file)

        output_file = tmp_path / "data.csv"
        log_file = tmp_path / "test.log"

        iwfm.pdf2csv(
            str(input_file),
            str(output_file),
            log_file=str(log_file)
        )

        assert output_file.exists()
        assert output_file.suffix == '.csv'

    def test_overwrites_existing_output(self, tmp_path):
        """Test that existing output file is overwritten."""
        input_file = tmp_path / "test.pdf"
        create_pdf_with_table(input_file)

        output_file = tmp_path / "output.csv"
        log_file = tmp_path / "test.log"

        # Create existing file
        output_file.write_text("old content")
        old_size = output_file.stat().st_size

        iwfm.pdf2csv(
            str(input_file),
            str(output_file),
            log_file=str(log_file)
        )

        # File should exist and content should have changed
        assert output_file.exists()
        new_content = output_file.read_text()
        assert new_content != "old content"


@requires_tabula
class TestPdf2csvEdgeCases:
    """Edge case tests for pdf2csv function (requires tabula-py and Java)."""

    def test_pdf_without_tables(self, tmp_path):
        """Test PDF without any tables."""
        try:
            import fpdf
        except ImportError:
            pytest.skip("fpdf library not installed")

        # Create PDF without tables
        input_file = tmp_path / "no_table.pdf"
        pdf = fpdf.FPDF()
        pdf.add_page()
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, 'This PDF has no tables, just text.')
        pdf.output(str(input_file))

        output_file = tmp_path / "output.csv"
        log_file = tmp_path / "test.log"

        # Should not raise an error, but output may be empty
        iwfm.pdf2csv(
            str(input_file),
            str(output_file),
            log_file=str(log_file)
        )

        # Output file should still be created (may be empty)
        assert output_file.exists()

    def test_multipage_pdf(self, tmp_path):
        """Test PDF with multiple pages containing tables."""
        try:
            import fpdf
        except ImportError:
            pytest.skip("fpdf library not installed")

        input_file = tmp_path / "multipage.pdf"
        pdf = fpdf.FPDF()

        # Create multiple pages with tables
        for page_num in range(3):
            pdf.add_page()
            pdf.set_font('Arial', 'B', 12)

            # Simple table on each page
            pdf.cell(40, 10, 'Col1', border=1)
            pdf.cell(40, 10, 'Col2', border=1)
            pdf.ln()
            pdf.set_font('Arial', '', 12)
            pdf.cell(40, 10, f'Page{page_num}', border=1)
            pdf.cell(40, 10, f'Data{page_num}', border=1)

        pdf.output(str(input_file))

        output_file = tmp_path / "output.csv"
        log_file = tmp_path / "test.log"

        iwfm.pdf2csv(
            str(input_file),
            str(output_file),
            log_file=str(log_file)
        )

        assert output_file.exists()

    def test_special_characters_in_path(self, tmp_path):
        """Test with special characters in file path."""
        # Create subdirectory with spaces
        subdir = tmp_path / "test dir"
        subdir.mkdir()

        input_file = subdir / "test file.pdf"
        create_pdf_with_table(input_file)

        output_file = subdir / "output file.csv"
        log_file = subdir / "test.log"

        iwfm.pdf2csv(
            str(input_file),
            str(output_file),
            log_file=str(log_file)
        )

        assert output_file.exists()
