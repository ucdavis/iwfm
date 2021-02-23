# gw_well_lay_elev.py
# Find layer elevation for each observation well
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


def gw_well_lay_elev(self, d_wellinfo, debug=0):
    """ gw_well_lay_elev() - Find layer elevations at each well using node 
        elevation data. Inverse Distance Weighting is used to determine the 
        elevations.

    Parameters:
      d_wellinfo     (dict): Dictionary with info for each well
      debug          (int):  Turn debugging to CLI on if >0 

    Returns:
      new_d_wellinfo (dict): Dictionary with layer info for each well


    To do:
        Find layer elevations at each well using node elevation data.


    """

    if debug:
        print('      => gw_well_lay_elev()')

    new_d_wellinfo = {}
    for key in d_wellinfo:  # cycle through wells
        if debug:
            print('      =>  {}: \t{}'.format('key', key))
        well_elevs = []

        old_value = d_wellinfo[key]  # save dictionary contents for this well
        x = d_wellinfo[key][0]  # well x coordinate
        y = d_wellinfo[key][1]  # well y coordinate
        elem = d_wellinfo[key][4]  # element containing well
        if debug:
            print('      =>  {}: \t{}'.format('old_value', old_value))

        e_nodes = self.e_nodes[
            self.e_nos.index(elem)
        ]  # nodes of element containing well
        old_value.append(e_nodes)

        nodexy = []
        for i in range(0, len(e_nodes)):
            nodexy.append(self.d_nodes[e_nodes[i]])  # x,y coordinates of element nodes

        if debug:
            print('      =>  {}: \t{}'.format('elem', elem))
            print('      =>  {}: \t{}'.format('e_nodes', e_nodes))
            print('      =>  {}: \t{}'.format('nodexy', nodexy))
            print('\n      => right here\n')

        elevs = []
        for i in range(0, len(self.nnodes)):
            index = self.nodeno[self.nnodes[i]]
            elevs.append(self.aquifer_top[index])  # aquifer top for these nodes
        if debug:
            print('      =>  {}: \t{}'.format('aquifer_top elevs', elevs))
        result_aqtop = IDW(
            x, y, elem, self.nnodes, self.nlayers, nodexy, elevs, debug
        )  # Top of each aquifer layer at well
        well_elevs.append(result_aqtop)
        if debug:
            print('      =>  {}: \t{}'.format('well_elevs', well_elevs))

        elevs = []
        for i in range(0, len(self.nnodes)):
            index = self.nodeno[self.nnodes[i]]
            elevs.append(self.aquifer_bottom[index])  # aquifer bottom for these nodes
        if debug:
            print('      =>  {}: \t{}'.format('aquifer_bottom elevs', elevs))
        result_aqbot = IDW(
            x, y, elem, self.nnodes, self.nlayers, nodexy, elevs, debug
        )  # Bottom of each aquifer layer at well
        well_elevs.append(result_aqbot)
        if debug:
            print('      =>  {}: \t{}'.format('well_elevs', well_elevs))

        elevs = []
        for i in range(0, len(self.nnodes)):
            index = self.nodeno[self.nnodes[i]]
            elevs.append(self.aquitard_top[index])  # aquitard top for these nodes
        if debug:
            print('      =>  {}: \t{}'.format('aquitard_top elevs', elevs))
        result_attop = IDW(
            x, y, elem, self.nnodes, self.nlayers, nodexy, elevs, debug
        )  # Top of each aquitard layer at well
        well_elevs.append(result_attop)
        if debug:
            print('      =>  {}: \t{}'.format('well_elevs', well_elevs))

        elevs = []
        for i in range(0, len(self.nnodes)):
            index = self.nodeno[self.nnodes[i]]
            elevs.append(self.aquitard_bottom[index])  # aquitard bottom for these nodes
        if debug:
            print('      =>  {}: \t{}'.format('aquitard_bottom elevs', elevs))
        result_atbot = IDW(
            x, y, elem, self.nnodes, self.nlayers, nodexy, elevs, debug
        )  # Bottom of each aquitard layer at well
        well_elevs.append(result_atbot)
        if debug:
            print('      =>  {}: \t{}'.format('well_elevs', well_elevs))

        old_value.append(well_elevs)
        if debug:
            print('      =>  {}: \t{}'.format('key', key))
        if debug:
            print('      =>  {}: \t{}'.format('old_value', old_value))
        new_d_wellinfo[key] = old_value
        if debug:
            print('      =>  new_d_wellinfo[{}]: \t{}'.format(key, new_d_wellinfo[key]))
        # result_top = IDW(nwell, xwell, ywell, wellelem, result_top, nnodes, nlayers, nodex, nodey, top_elev, nelements, elements)
        # result_bot = IDW(nwell, xwell, ywell, wellelem, result_bot, nnodes, nlayers, nodex, nodey, bot_elev, nelements, elements)
        # return result_top,result_botom

        #!-----------------------------------------------------------------------------!
        # SUBROUTINE layerelevation(top_elev, bot_elev, result_top, result_bot)
        #    implicit none
        #!-----------------------------------------------------------------------------!
        #! Find layer elevations at each well using node elevation data.
        #! Inverse Distance Weighting is used to determine the elevations.
        #!
        #! Arguments:
        #!    - topelev    - Top elevation at nodes
        #!    - botelev    - Bottom elevation at nodes
        #!    - result_top - Layer top elevations at each well
        #!    - result_bot - Layer bottom elevations at each well
        #!-----------------------------------------------------------------------------!
        #    real,intent(in)          :: top_elev(nnodes, nlayers), &
        #                                bot_elev(nnodes, nlayers)
        #    real,intent(inout)       :: result_top(nwell, nlayers), &
        #                                result_bot(nwell, nlayers)
        #
        #    result_top = 0.0
        #    result_bot = 0.0
        #
        #    call IDW(nwell, xwell, ywell, wellelem, result_top, nnodes, nlayers, &
        #             nodex, nodey, top_elev, nelements, elements)
        #    call IDW(nwell, xwell, ywell, wellelem, result_bot, nnodes, nlayers, &
        #             nodex, nodey, bot_elev, nelements, elements)
        #
        # end subroutine layerelevation
        #!-----------------------------------------------------------------------------!
    if debug:
        print('\n  ** incomplete: gw_well_lay_elev.py  **\n')
    return new_d_wellinfo
