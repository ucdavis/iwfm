# exe_time.py
# Print difference between two datetime values
# First call stores start time, subsequent calls print elapsed time
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


def exe_time():
    """ print_exe_time() - Tracks the time since the first call, and prints
        the elapsed time on subsequent calls 

    Parameters:
      nothing
    
    Return:
      nothing
    """
    import datetime
    import iwfm as iwfm

    if not hasattr(exe_time, "start"):
        exe_time.start = datetime.datetime.now()
        # access exe_time.start in the body however you want
        return
    else:
        end = datetime.datetime.now()

        diff = str(end - exe_time.start).split(":")
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
        print("  Elapsed time: {}{}{}\n".format(hours, mins, secs))
    return
