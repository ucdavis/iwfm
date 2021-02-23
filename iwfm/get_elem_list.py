# get_elem_list.py
# Reads the submodel elements and returns a dictionary of old to new elements
# and a dictionary of new to old elements
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


def get_elem_list(elem_pairs_file):
    """get_elem_list() reads the submodel elements and returns a dictionary
        of old to new elements and a dictionary of new to old elements

    Parameters:
      elem_pairs_file (str):  Name of file listing elements of existing nmodel
                                and submodel

    Returns:
      elem_list      (ints):  List of existing model elements in submodel
      new_srs        (ints):  List of existing model subregions in submodel
      elem_dict      (dict):  Dictionary existing model element to submodel
                                element
      rev_elem_dict  (dict):  Dictionary submodel element to existing model
                                element

    """
    import iwfm as iwfm

    # == read in the element pairs and create a dictionary
    elem_list = []
    elem_pairs = open(elem_pairs_file).read().splitlines()  # open and read input file
    for i in range(0, len(elem_pairs)):  # cycle through the lines
        line = elem_pairs[i].split()
        for j in range(0, len(line)):  # convert to integers
            line[j] = int(line[j])
        elem_list.append(line)
    elem_dict = iwfm.list2dict(elem_list)  # dictionary old elem -> new elem
    # also create a reverse dictionary new elem -> old elem
    for i in range(0, len(elem_list)):  # switch the new and old elem nos
        temp = elem_list[i][0]
        elem_list[i][0] = elem_list[i][1]
        elem_list[i][1] = temp
    rev_elem_dict = iwfm.list2dict(elem_list)  # dictionary new elem -> old elem

    # make a list of the subregions in the submodel
    new_srs = []
    for i in range(0, len(elem_list)):
        if int(elem_list[i][2]) not in new_srs:
            new_srs.append(int(elem_list[i][2]))
    new_srs.sort()
    if new_srs[0] == 0:
        new_srs.pop(0)

    return elem_list, new_srs, elem_dict, rev_elem_dict
