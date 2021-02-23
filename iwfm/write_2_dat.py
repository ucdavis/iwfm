# write_2_dat.py
# Write a 3D array of crop areas to a series of 2D files for each crop
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


def write_2_dat(file_base_name, data, crops, elements, time_steps, dates):
    """ write_2_dat() - Write a 3D array as 2D tables (row=elements
        x col=time_steps) to crops # of text files with filename 
        extension 'dat'

    Parameters:
      file_base_name (str):   Base name of output file
      data           (list):  Data to be written
      crops          (list):  List of crop codes or names
      elements       (list):  Model element numbers
      time_steps     (int):   Number of time steps
      dates          (list):  Dates corresponding to time steps

    Returns:
      nothing

    """
    # Create the output file names
    files = ["" for x in range(crops)]  # empty list
    for i in range(0, crops):
        files[i] = "".join([file_base_name, "_", str(i + 1), ".dat"])
    # write the arrays to the output files
    for i in range(crops):
        fp = open(files[i], "w")
        fp.write("   WYr  ")
        for j in range(time_steps):
            fp.write("               {}  ".format(dates[j].year))
        fp.write("\n")
        for j in range(elements):
            fp.write("{:6d} ".format(j + 1))
            for k in range(time_steps):
                fp.write("{:20.4f} ".format(float(data[i][j][k])))
            fp.write("\n")
        fp.close
    return
