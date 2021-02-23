# iwfm_read_strat.py
# read IWFM preprocessor stratigraphy file
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


def iwfm_read_strat(strat_file, node_coords):
    """ iwfm_read_strat() reads an IWFM Stratigraphy file and returns a list
        of stratigraphy for each node.
    """
    import iwfm as iwfm
    import re

    strat_lines = open(strat_file).read().splitlines()  # open and read input file
    line_index = 0  # start at the top
    line_index = iwfm.skip_ahead(line_index, strat_lines, 0)  # skip comments
    import re

    layers = int(re.findall('\d+', strat_lines[line_index])[0])  # read no. layers

    line_index = iwfm.skip_ahead(line_index + 1, strat_lines, 0)  # skip comments
    factor = float(re.findall('\d+', strat_lines[line_index])[0])  # read no. layers

    line_index = iwfm.skip_ahead(line_index + 1, strat_lines, 0)  # skip comments

    strat = []
    for i in range(0, len(node_coords)):
        l = strat_lines[line_index + i].split()
        s = []
        s.append(int(l.pop(0)))  # node no
        for j in range(0, len(l)):
            s.append(factor * float(l.pop(0)))  # lse, etc as floats
        strat.append(s)
    nlayers = int((len(strat[0]) - 1) / 2)
    return strat, nlayers
