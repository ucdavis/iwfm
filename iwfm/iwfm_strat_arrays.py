# iwfm_strat_arrays.py
# parse IWFM stratigraphy information into arrays
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


def iwfm_strat_arrays(strat):
    """ iwfm_strat_arrays() - Read IWFM nodal stratigraphy information 
        into individual arrays

    Parameters:
      strat           (list):  Stratigraphy information

    Returns:
      aquitard_thick  (list):  Aquitard thickness by model layer and node
      aquifer_thick   (list):  Aquifer thickness by model layer and node
      aquitard_top    (list):  Aquitard top altitude by model layer and node
      aquitard_bot    (list):  Aquitard bottom altitude by model layer and node
      aquifer_top     (list):  Aquifer top altitude by model layer and node
      aquifer_bot     (list):  Aquifer bottom altitude by model layer and node
    """
    nlayers = int((len(strat[0]) - 1) / 2)
    elevation = [i[0] for i in strat]

    aquitard_thick = []  # initialize arrays
    aquifer_thick = []
    aquitard_top = []
    aquitard_bot = []
    aquifer_top = []
    aquifer_bot = []

    for i in range(0, len(strat)):  # cycle through stratigraphy of each node
        l = strat[i]
        depth = 0
        this_node = l.pop(0)
        lse = float(l.pop(0))
        # initialize accumulators
        Tthick = []  # thickness of aquitard(s)
        Athick = []  # thickness of aquifer(s)
        AttElev = []  # top of aquitard(s)
        AtbElev = []  # bottom of aquitard(s)
        AqtElev = []  # top of aquifer(s)
        AqbElev = []  # bottom of aquifer(s)

        for j in range(0, nlayers):  # cycle through layers for each node
            AttElev.append(lse - depth)  # top of aquitard

            t = strat[i][2 * j]  # thickness of aquitard
            Tthick.append(t)
            depth += t  # add to total depth
            AtbElev.append(lse - depth)  # bottom of aquitard
            AqtElev.append(lse - depth)  # top of aquifer

            a = strat[i][2 * j + 1]  # thickness of aquifer
            Athick.append(a)
            depth += a  # add to total depth
            AqbElev.append(lse - depth)  # bottom of aquifer

        aquitard_thick.append(Tthick)  # aqTardThick[node][layer]
        aquifer_thick.append(Athick)  # thick[node][layer]
        aquitard_top.append(AttElev)  # aqTardTopElev[node][layer]
        aquitard_bot.append(AtbElev)  # aqTardBotElev[node][layer]
        aquifer_top.append(AqtElev)  # topElev[node][layer]
        aquifer_bot.append(AqbElev)  # botElev[node][layer]

    return (
        aquitard_thick,
        aquifer_thick,
        aquitard_top,
        aquitard_bot,
        aquifer_top,
        aquifer_bot,
    )
