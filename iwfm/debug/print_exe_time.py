# print_exe_time.py
# Print difference between two datetime values
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


def print_exe_time(start, end):
    """Function print_exe_time(start, end) prints the time between two datetime values

    Parameters:
      start    (datetime):  Starting time
      end      (datetime):  Ending time
    
    Return:
      nothing
"""
    import iwfm as iwfm

    diff = str(end - start).split(":")
    secs = str(round(float(diff[2]), 1))
    if int(diff[0]) > 0:
        hours = iwfm.pad_front(str(int(diff[0])), 2, "0") + ":"
        mins = iwfm.pad_front(str(int(diff[1])), 2, "0") + ":"
    elif int(diff[1]) > 0:
        hours = ""
        mins = str(int(diff[1])) + " min "
        secs += " sec"
    else:
        hours, mins = "", ""
        secs += " seconds"
    print("  Execution time: {}{}{}\n".format(hours, mins, secs))
