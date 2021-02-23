# skip_ahead.py
# Skip a specified number of list elements plus all that begin with a comment character
# Copyright (C) 2020-2021 Hydrolytics LLC
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


def skip_ahead(line_index, all_lines, skip=0):
    """ skip_ahead() - Increment line_index by skipping (a) every line that 
        begins with 'C', 'c' '*' or '#' and (b) 'skip' additional lines.
        Stop if last line (all_lines) is reached.

    Parameters:
      line_index      (int):  Current line number
      all_lines       (list): Each item is one line from a file
      skip            (int):  Number of non-comment lines to skip

    Returns:
      line_index      (int):  New current line or -1 if end reached
    """
    skip_lines = skip
    comments = 'Cc*#'
    while skip_lines > 0:
        if line_index >= len(all_lines):
            return -1
        if all_lines[line_index][0] not in comments:  # skip 
            skip_lines -= 1
        line_index += 1
    while all_lines[line_index][0] in comments:  # skip
        line_index += 1
        if line_index > len(all_lines):
            return -1
    return line_index
