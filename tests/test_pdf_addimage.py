# test_pdf_addimage.py
# unit tests for pdf_addimage function
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

# Check if fpdf is available
fpdf = pytest.importorskip("fpdf", reason="fpdf library not installed")

import iwfm


def create_test_image(filepath, width=100, height=100, color=(255, 0, 0)):
    """Helper to create a simple test PNG image."""
    try:
        from PIL import Image
        img = Image.new('RGB', (width, height), color=color)
        img.save(filepath)
        return True
    except ImportError:
        # Fall back to creating a minimal valid PNG without PIL
        # Minimal 1x1 red PNG
        import struct
        import zlib

        def png_chunk(chunk_type, data):
            chunk_len = len(data)
            chunk = chunk_type + data
            crc = zlib.crc32(chunk) & 0xffffffff
            return struct.pack('>I', chunk_len) + chunk + struct.pack('>I', crc)

        # PNG signature
        signature = b'\x89PNG\r\n\x1a\n'

        # IHDR chunk (image header)
        ihdr_data = struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0)
        ihdr = png_chunk(b'IHDR', ihdr_data)

        # IDAT chunk (image data) - simple uncompressed red pixels
        raw_data = b''
        for _ in range(height):
            raw_data += b'\x00'  # filter byte
            for _ in range(width):
                raw_data += bytes(color)
        compressed = zlib.compress(raw_data)
        idat = png_chunk(b'IDAT', compressed)

        # IEND chunk
        iend = png_chunk(b'IEND', b'')

        with open(filepath, 'wb') as f:
            f.write(signature + ihdr + idat + iend)
        return True


class TestPdfAddimage:
    """Tests for the pdf_addimage function."""

    def test_basic_add_image(self, tmp_path):
        """Test basic image addition to PDF."""
        # Create a test image
        image_path = tmp_path / "test_image.png"
        create_test_image(str(image_path))

        # Create PDF and add page
        pdf = iwfm.pdf_create()
        pdf.add_page()

        # Add image
        result = iwfm.pdf_addimage(pdf, str(image_path))

        # Verify PDF object is returned
        assert result is not None
        assert result is pdf

        # Save and verify file can be created
        output_path = tmp_path / "output.pdf"
        pdf.output(str(output_path))
        assert output_path.exists()
        assert output_path.stat().st_size > 0

    def test_default_parameters(self, tmp_path):
        """Test that default parameters work correctly."""
        image_path = tmp_path / "test_image.png"
        create_test_image(str(image_path))

        pdf = iwfm.pdf_create()
        pdf.add_page()

        # Use all defaults
        result = iwfm.pdf_addimage(pdf, str(image_path))

        assert result is not None

        # Save to verify it worked
        output_path = tmp_path / "output.pdf"
        pdf.output(str(output_path))
        assert output_path.exists()

    def test_custom_position(self, tmp_path):
        """Test image placement at custom position."""
        image_path = tmp_path / "test_image.png"
        create_test_image(str(image_path))

        pdf = iwfm.pdf_create()
        pdf.add_page()

        # Custom position
        result = iwfm.pdf_addimage(pdf, str(image_path), ux=2, uy=3)

        assert result is not None

        output_path = tmp_path / "output.pdf"
        pdf.output(str(output_path))
        assert output_path.exists()

    def test_custom_dimensions(self, tmp_path):
        """Test image with custom width and height."""
        image_path = tmp_path / "test_image.png"
        create_test_image(str(image_path))

        pdf = iwfm.pdf_create()
        pdf.add_page()

        # Custom dimensions
        result = iwfm.pdf_addimage(pdf, str(image_path), width=4.0, height=3.0)

        assert result is not None

        output_path = tmp_path / "output.pdf"
        pdf.output(str(output_path))
        assert output_path.exists()

    def test_custom_position_and_dimensions(self, tmp_path):
        """Test image with all custom parameters."""
        image_path = tmp_path / "test_image.png"
        create_test_image(str(image_path))

        pdf = iwfm.pdf_create()
        pdf.add_page()

        # All custom parameters
        result = iwfm.pdf_addimage(
            pdf, str(image_path),
            ux=0.5, uy=0.5,
            width=7.5, height=10.0
        )

        assert result is not None

        output_path = tmp_path / "output.pdf"
        pdf.output(str(output_path))
        assert output_path.exists()

    def test_multiple_images(self, tmp_path):
        """Test adding multiple images to same PDF."""
        image1_path = tmp_path / "image1.png"
        image2_path = tmp_path / "image2.png"
        create_test_image(str(image1_path), color=(255, 0, 0))
        create_test_image(str(image2_path), color=(0, 255, 0))

        pdf = iwfm.pdf_create()
        pdf.add_page()

        # Add first image
        pdf = iwfm.pdf_addimage(pdf, str(image1_path), ux=1, uy=1, width=3, height=3)

        # Add second image
        pdf = iwfm.pdf_addimage(pdf, str(image2_path), ux=4, uy=1, width=3, height=3)

        output_path = tmp_path / "output.pdf"
        pdf.output(str(output_path))
        assert output_path.exists()
        # File should be larger with two images
        assert output_path.stat().st_size > 100

    def test_image_on_multiple_pages(self, tmp_path):
        """Test adding images to multiple pages."""
        image_path = tmp_path / "test_image.png"
        create_test_image(str(image_path))

        pdf = iwfm.pdf_create()

        # Page 1
        pdf.add_page()
        pdf = iwfm.pdf_addimage(pdf, str(image_path), ux=1, uy=1)

        # Page 2
        pdf.add_page()
        pdf = iwfm.pdf_addimage(pdf, str(image_path), ux=2, uy=2)

        output_path = tmp_path / "output.pdf"
        pdf.output(str(output_path))
        assert output_path.exists()

    def test_returns_same_pdf_object(self, tmp_path):
        """Test that function returns the same PDF object (modified in place)."""
        image_path = tmp_path / "test_image.png"
        create_test_image(str(image_path))

        pdf = iwfm.pdf_create()
        pdf.add_page()

        original_id = id(pdf)
        result = iwfm.pdf_addimage(pdf, str(image_path))

        assert id(result) == original_id

    def test_small_image_dimensions(self, tmp_path):
        """Test image with very small dimensions."""
        image_path = tmp_path / "test_image.png"
        create_test_image(str(image_path))

        pdf = iwfm.pdf_create()
        pdf.add_page()

        result = iwfm.pdf_addimage(pdf, str(image_path), width=0.5, height=0.5)

        assert result is not None

        output_path = tmp_path / "output.pdf"
        pdf.output(str(output_path))
        assert output_path.exists()

    def test_large_image_dimensions(self, tmp_path):
        """Test image with large dimensions."""
        image_path = tmp_path / "test_image.png"
        create_test_image(str(image_path))

        pdf = iwfm.pdf_create()
        pdf.add_page()

        # Full page size
        result = iwfm.pdf_addimage(pdf, str(image_path), ux=0, uy=0, width=8.5, height=11)

        assert result is not None

        output_path = tmp_path / "output.pdf"
        pdf.output(str(output_path))
        assert output_path.exists()

    def test_zero_position(self, tmp_path):
        """Test image at origin position (0, 0)."""
        image_path = tmp_path / "test_image.png"
        create_test_image(str(image_path))

        pdf = iwfm.pdf_create()
        pdf.add_page()

        result = iwfm.pdf_addimage(pdf, str(image_path), ux=0, uy=0)

        assert result is not None

        output_path = tmp_path / "output.pdf"
        pdf.output(str(output_path))
        assert output_path.exists()

    def test_nonexistent_image_raises_error(self, tmp_path):
        """Test that nonexistent image file raises an error."""
        pdf = iwfm.pdf_create()
        pdf.add_page()

        nonexistent_path = tmp_path / "nonexistent.png"

        with pytest.raises(Exception):  # fpdf raises various exceptions for missing files
            iwfm.pdf_addimage(pdf, str(nonexistent_path))

    def test_with_landscape_pdf(self, tmp_path):
        """Test adding image to landscape-oriented PDF."""
        image_path = tmp_path / "test_image.png"
        create_test_image(str(image_path))

        # Create landscape PDF
        pdf = iwfm.pdf_create(layout='L')
        pdf.add_page()

        result = iwfm.pdf_addimage(pdf, str(image_path), width=9, height=6.5)

        assert result is not None

        output_path = tmp_path / "output.pdf"
        pdf.output(str(output_path))
        assert output_path.exists()

    def test_float_positions(self, tmp_path):
        """Test image with float position values."""
        image_path = tmp_path / "test_image.png"
        create_test_image(str(image_path))

        pdf = iwfm.pdf_create()
        pdf.add_page()

        result = iwfm.pdf_addimage(
            pdf, str(image_path),
            ux=1.5, uy=2.75,
            width=3.25, height=4.125
        )

        assert result is not None

        output_path = tmp_path / "output.pdf"
        pdf.output(str(output_path))
        assert output_path.exists()

    def test_jpeg_image(self, tmp_path):
        """Test adding JPEG image to PDF."""
        image_path = tmp_path / "test_image.jpg"

        try:
            from PIL import Image
            img = Image.new('RGB', (100, 100), color=(0, 0, 255))
            img.save(str(image_path), 'JPEG')
        except ImportError:
            pytest.skip("PIL not available for JPEG creation")

        pdf = iwfm.pdf_create()
        pdf.add_page()

        result = iwfm.pdf_addimage(pdf, str(image_path))

        assert result is not None

        output_path = tmp_path / "output.pdf"
        pdf.output(str(output_path))
        assert output_path.exists()
