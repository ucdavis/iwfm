# test_filename.py
# unit test for filename() in the iwfm package
# Copyright (C) 2025 University of California
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

import iwfm


def test_filename_base_removes_extension():
    assert iwfm.filename_base("/tmp/data/file.txt") == "/tmp/data/file"
    assert iwfm.filename_base("file.tar.gz") == "file.tar"


def test_filename_base_no_extension():
    assert iwfm.filename_base("/path/to/file") == "/path/to/file"


def test_filename_ext_appends_when_missing():
    assert iwfm.filename_ext("file", "txt") == "file.txt"


def test_filename_ext_does_not_duplicate_when_present():
    assert iwfm.filename_ext("file.txt", "txt") == "file.txt"


def test_filename_ext_strips_trailing_dot():
    assert iwfm.filename_ext("file.", "csv") == "file.csv"


def test_filename_ext_with_different_existing_ext_behaves_as_implemented():
    # Current implementation appends the new extension rather than replacing
    assert iwfm.filename_ext("file.txt", "csv") == "file.txt.csv"


