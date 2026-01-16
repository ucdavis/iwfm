# test_debug_utils.py
# unit test for iwfm.debug methods in the iwfm package
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
import iwfm.debug as debug


def test_check_key_present_and_absent():
    d = {"a": 1, 2: "b"}
    assert debug.check_key(d, "a") is True
    assert debug.check_key(d, 2) is True
    assert debug.check_key(d, "missing") is False


def test_print_dict_outputs_pairs(capsys):
    d = {"k1": "v1", "k2": 2}
    debug.print_dict(d)
    out = capsys.readouterr().out
    assert "key" in out and "value" in out
    assert "k1" in out and "v1" in out
    assert "k2" in out and "2" in out


def test_print_env_outputs_lines(capsys):
    debug.print_env()
    out = capsys.readouterr().out
    assert "Environment:" in out
    assert "System:" in out
    assert "PATH:" in out


def test_system_info_helpers():
    v = debug.this_python()
    assert isinstance(v, str) and "." in v
    sysname = debug.this_sys()
    assert sysname in ("Linux", "Darwin", "Windows")
    rel = debug.this_sys_version()
    assert isinstance(rel, str) and len(rel) >= 1


