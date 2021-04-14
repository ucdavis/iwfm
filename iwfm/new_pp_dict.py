# new_pp_dict.py
# Creates and returns a dictionary of preprocessor file names from a basename
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


def new_pp_dict(out_base_name):
    ''' new_pp_dict() - Create and return a dictionary of preprocessor file
        names from a basename

    Parameters
    ----------
    out_base_name : str
        root of submodel output file names

    Returns
    -------
    pre_dict_new : dict
        dictionary of submodel preprocessor file names

    '''
    pre_dict_new = {}
    pre_dict_new['prename'] = out_base_name + '_Preprocessor.in'
    pre_dict_new['preout'] = out_base_name + '_Preprocessor.bin'
    pre_dict_new['elem_file'] = out_base_name + '_Elements.dat'
    pre_dict_new['node_file'] = out_base_name + '_Nodes.dat'
    pre_dict_new['strat_file'] = out_base_name + '_Stratigraphy.dat'
    pre_dict_new['stream_file'] = out_base_name + '_StreamSpec.dat'
    pre_dict_new['lake_file'] = out_base_name + '_Lakes.dat'
    return pre_dict_new
