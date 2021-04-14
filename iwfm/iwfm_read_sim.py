# iwfm_read_sim.py
# Read IWFM Simulation main file
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

def iwfm_read_sim(sim_file):
    ''' iwfm_read_sim() - Read an IWFM Simulation main input file, and 
        return a dictionary with the files called and some settings

    Parameters
    ----------
    sim_file : str
        Name of IWFM Simulation file

    Returns
    -------
    sim_dict : dictionary
        Dictionary with fixed keys, file names for corresponding values
          Keys            Refers to
          ----            ----------
          preout          Preprocessor output file name
          gw              Groundwater main file name
          stream          Stream main file name
          lake            Lake main file name
          rootzone        Rootzone main file name
          smallwatershed  Small Watershed file name
          unsat           Unsaturated Zone file name
          irrfrac         Irrigation Fractions file name
          supplyadj       Supply Adjustment file name
          precip          Precipitaiton file name
          et              Evapotranspiration file name
          start           Starting data (DSS format)
          step            Time step (IWFM fixed set)
          end             Ending date (DSS format)

    '''
    import iwfm as iwfm

    sim_dict = {}
    sim_lines = open(sim_file).read().splitlines()

    line_index = iwfm.skip_ahead(0, sim_lines, 3)  # skip comments
    sim_dict['preout'] = iwfm.file_get_path(sim_lines[line_index].split()[0])  
    
    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)  
    sim_dict['gw'] = iwfm.file_file_get_path(sim_lines[line_index].split()[0])
    
    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)  
    sim_dict['stream'] = iwfm.file_get_path(sim_lines[line_index].split()[0])
    
    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)  
    temp = sim_lines[line_index].split()[0]
    if temp[0] == '/':   # check for presence of lake file
        lake_file = ''
    else:
        lake_file = iwfm.file_get_path(temp)  
    sim_dict['lake'] = lake_file

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)  
    sim_dict['rootzone'] = iwfm.file_get_path(sim_lines[line_index].split()[0])
    
    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)  
    sim_dict['smallwatershed'] = iwfm.file_get_path(sim_lines[line_index].split()[0])
    
    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)  
    sim_dict['unsat'] = iwfm.file_get_path(sim_lines[line_index].split()[0])
    
    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)  
    sim_dict['irrfrac'] = iwfm.file_get_path(sim_lines[line_index].split()[0])

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)  
    sim_dict['supplyadj'] = iwfm.file_get_path(sim_lines[line_index].split()[0])

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)  
    sim_dict['precip'] = sim_lines[line_index].split()[0]

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)  
    sim_dict['et'] = iwfm.file_get_path(sim_lines[line_index].split()[0])
    
    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)  
    sim_dict['start'] = sim_lines[line_index].split()[0] 
    
    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)  
    sim_dict['step'] = sim_lines[line_index].split()[0]  

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)  
    sim_dict['end'] = sim_lines[line_index].split()[0]  

    return sim_dict
