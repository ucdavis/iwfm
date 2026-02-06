# test_Unbuffered.py
# unit tests for Unbuffered class
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
import io


import iwfm


class MockStream:
    """Mock stream class to track write and flush calls."""

    def __init__(self):
        self.data = []
        self.flush_count = 0
        self.write_count = 0

    def write(self, data):
        self.data.append(data)
        self.write_count += 1

    def writelines(self, datas):
        self.data.extend(datas)

    def flush(self):
        self.flush_count += 1

    def getvalue(self):
        return ''.join(self.data)


class TestUnbufferedInit:
    """Tests for Unbuffered class initialization."""

    def test_init_with_stringio(self):
        """Test initialization with StringIO stream."""
        stream = io.StringIO()

        unbuffered = iwfm.Unbuffered(stream)

        assert unbuffered.stream is stream

    def test_init_stores_stream(self):
        """Test that stream is stored as attribute."""
        stream = MockStream()

        unbuffered = iwfm.Unbuffered(stream)

        assert unbuffered.stream is stream

    def test_init_with_mock_stream(self):
        """Test initialization with mock stream."""
        stream = MockStream()

        unbuffered = iwfm.Unbuffered(stream)

        assert unbuffered is not None


class TestUnbufferedWrite:
    """Tests for Unbuffered.write method."""

    def test_write_simple_string(self):
        """Test writing a simple string."""
        stream = io.StringIO()
        unbuffered = iwfm.Unbuffered(stream)

        unbuffered.write("hello")

        assert stream.getvalue() == "hello"

    def test_write_flushes_after_write(self):
        """Test that flush is called after write."""
        stream = MockStream()
        unbuffered = iwfm.Unbuffered(stream)

        unbuffered.write("test")

        assert stream.flush_count == 1

    def test_write_multiple_times(self):
        """Test multiple writes accumulate correctly."""
        stream = io.StringIO()
        unbuffered = iwfm.Unbuffered(stream)

        unbuffered.write("hello")
        unbuffered.write(" ")
        unbuffered.write("world")

        assert stream.getvalue() == "hello world"

    def test_write_flushes_each_time(self):
        """Test that flush is called after each write."""
        stream = MockStream()
        unbuffered = iwfm.Unbuffered(stream)

        unbuffered.write("one")
        unbuffered.write("two")
        unbuffered.write("three")

        assert stream.flush_count == 3

    def test_write_empty_string(self):
        """Test writing an empty string."""
        stream = io.StringIO()
        unbuffered = iwfm.Unbuffered(stream)

        unbuffered.write("")

        assert stream.getvalue() == ""

    def test_write_with_newline(self):
        """Test writing string with newline."""
        stream = io.StringIO()
        unbuffered = iwfm.Unbuffered(stream)

        unbuffered.write("line1\nline2")

        assert stream.getvalue() == "line1\nline2"

    def test_write_special_characters(self):
        """Test writing special characters."""
        stream = io.StringIO()
        unbuffered = iwfm.Unbuffered(stream)

        unbuffered.write("tab\there\nand\rcarriage")

        assert stream.getvalue() == "tab\there\nand\rcarriage"

    def test_write_unicode(self):
        """Test writing unicode characters."""
        stream = io.StringIO()
        unbuffered = iwfm.Unbuffered(stream)

        unbuffered.write("héllo wörld")

        assert stream.getvalue() == "héllo wörld"


class TestUnbufferedWritelines:
    """Tests for Unbuffered.writelines method."""

    def test_writelines_list(self):
        """Test writelines with a list of strings."""
        stream = io.StringIO()
        unbuffered = iwfm.Unbuffered(stream)

        unbuffered.writelines(["line1", "line2", "line3"])

        assert stream.getvalue() == "line1line2line3"

    def test_writelines_flushes_after(self):
        """Test that flush is called after writelines."""
        stream = MockStream()
        unbuffered = iwfm.Unbuffered(stream)

        unbuffered.writelines(["a", "b", "c"])

        assert stream.flush_count == 1

    def test_writelines_empty_list(self):
        """Test writelines with empty list."""
        stream = io.StringIO()
        unbuffered = iwfm.Unbuffered(stream)

        unbuffered.writelines([])

        assert stream.getvalue() == ""

    def test_writelines_single_item(self):
        """Test writelines with single item list."""
        stream = io.StringIO()
        unbuffered = iwfm.Unbuffered(stream)

        unbuffered.writelines(["only one"])

        assert stream.getvalue() == "only one"

    def test_writelines_with_newlines(self):
        """Test writelines preserves newlines."""
        stream = io.StringIO()
        unbuffered = iwfm.Unbuffered(stream)

        unbuffered.writelines(["line1\n", "line2\n", "line3\n"])

        assert stream.getvalue() == "line1\nline2\nline3\n"

    def test_writelines_tuple(self):
        """Test writelines with a tuple."""
        stream = io.StringIO()
        unbuffered = iwfm.Unbuffered(stream)

        unbuffered.writelines(("a", "b", "c"))

        assert stream.getvalue() == "abc"


class TestUnbufferedGetattr:
    """Tests for Unbuffered.__getattr__ method."""

    def test_getattr_delegates_to_stream(self):
        """Test that unknown attributes are delegated to stream."""
        stream = io.StringIO()
        unbuffered = iwfm.Unbuffered(stream)

        # StringIO has getvalue method
        result = unbuffered.getvalue()

        assert result == ""

    def test_getattr_after_write(self):
        """Test getattr after writing to stream."""
        stream = io.StringIO()
        unbuffered = iwfm.Unbuffered(stream)

        unbuffered.write("test data")
        result = unbuffered.getvalue()

        assert result == "test data"

    def test_getattr_seek(self):
        """Test accessing seek method through getattr."""
        stream = io.StringIO()
        unbuffered = iwfm.Unbuffered(stream)

        unbuffered.write("hello world")
        unbuffered.seek(0)  # Delegated to stream
        result = stream.read()

        assert result == "hello world"

    def test_getattr_tell(self):
        """Test accessing tell method through getattr."""
        stream = io.StringIO()
        unbuffered = iwfm.Unbuffered(stream)

        unbuffered.write("12345")
        position = unbuffered.tell()  # Delegated to stream

        assert position == 5


class TestUnbufferedIntegration:
    """Integration tests for Unbuffered class."""

    def test_use_as_stdout_replacement(self, capsys):
        """Test using Unbuffered as stdout replacement."""
        # Create unbuffered wrapper around StringIO
        stream = io.StringIO()
        unbuffered = iwfm.Unbuffered(stream)

        # Write progress-style output
        unbuffered.write("Processing: ")
        unbuffered.write("25%")
        unbuffered.write(" 50%")
        unbuffered.write(" 75%")
        unbuffered.write(" 100%")

        assert stream.getvalue() == "Processing: 25% 50% 75% 100%"

    def test_progress_simulation(self):
        """Test simulating progress output."""
        stream = MockStream()
        unbuffered = iwfm.Unbuffered(stream)

        # Simulate progress updates
        for i in range(0, 101, 10):
            unbuffered.write(f"\rProgress: {i}%")

        # Should have flushed 11 times (0, 10, 20, ..., 100)
        assert stream.flush_count == 11

    def test_date_output_example(self):
        """Test the example from docstring: writing dates."""
        stream = io.StringIO()
        unbuffered = iwfm.Unbuffered(stream)

        dates = ["01/01/2000", "02/01/2000", "03/01/2000"]
        for date in dates:
            unbuffered.write(" " + date)

        assert stream.getvalue() == " 01/01/2000 02/01/2000 03/01/2000"

    def test_mixed_write_and_writelines(self):
        """Test mixing write and writelines calls."""
        stream = io.StringIO()
        unbuffered = iwfm.Unbuffered(stream)

        unbuffered.write("Header: ")
        unbuffered.writelines(["item1", ", ", "item2", ", ", "item3"])
        unbuffered.write("\nEnd")

        assert stream.getvalue() == "Header: item1, item2, item3\nEnd"


class TestUnbufferedEdgeCases:
    """Edge case tests for Unbuffered class."""

    def test_write_numbers_as_string(self):
        """Test writing numbers converted to strings."""
        stream = io.StringIO()
        unbuffered = iwfm.Unbuffered(stream)

        unbuffered.write(str(123))
        unbuffered.write(str(456.789))

        assert stream.getvalue() == "123456.789"

    def test_large_write(self):
        """Test writing large amount of data."""
        stream = io.StringIO()
        unbuffered = iwfm.Unbuffered(stream)

        large_string = "x" * 10000
        unbuffered.write(large_string)

        assert len(stream.getvalue()) == 10000

    def test_many_small_writes(self):
        """Test many small writes."""
        stream = MockStream()
        unbuffered = iwfm.Unbuffered(stream)

        for i in range(100):
            unbuffered.write(".")

        assert stream.write_count == 100
        assert stream.flush_count == 100
        assert stream.getvalue() == "." * 100

    def test_carriage_return_for_progress(self):
        """Test using carriage return for overwriting progress."""
        stream = io.StringIO()
        unbuffered = iwfm.Unbuffered(stream)

        unbuffered.write("\rProgress: 0%")
        unbuffered.write("\rProgress: 50%")
        unbuffered.write("\rProgress: 100%")

        # All writes are accumulated (stream doesn't interpret \r)
        assert "\rProgress: 100%" in stream.getvalue()
