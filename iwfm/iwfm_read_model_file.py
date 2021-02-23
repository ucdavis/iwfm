# iwfm_read_model_file.py
# read IWFM model file and return ordered list of file names
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


def iwfm_read_model_file(iwfm_file):
    """ iwfm_read_model() - Read an IWFM model file (*.iwfm) containing file
        names for an IWFM model components (Preprocessor,Simulation, Budget, 
        ZBudget) and return a list of the file names

    Parameters:
      iwfm_file       (str):  Name of IWFM model file

    Returns:
      files_list      (list):  List of file names

    To do:
      - change the list to a dictionary

    """
    # -- read the file contents into array file_lines
    lines = open(iwfm_file).read().splitlines()  # open and read input file
    files_list = []
    for i, line in enumerate(lines):
        if line[0] != "#":  # skip comment lines
            items = line.split()
            if len(files_list) == 0:
                files_list.append([items[0], [items[1]]])
            else:
                j, skip = 0, 0
                while skip == 0 and j < len(files_list):
                    if items[0] == files_list[j][0]:
                        files_list[j][1].append(items[1])
                        skip = 1
                    j += 1
                if skip == 0:
                    files_list.append([items[0], [items[1]]])
    return files_list
