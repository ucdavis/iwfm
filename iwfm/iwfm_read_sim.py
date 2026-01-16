# iwfm_read_sim.py
# Read IWFM Simulation main file
# Copyright (C) 2020-2026 University of California
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


def _safe_get_value(line, line_num, field_name='value'):
    """Safely extract first value from line with validation.

    Parameters
    ----------
    line : str
        The line to parse
    line_num : int
        Line number for error reporting
    field_name : str
        Description of expected field for error messages

    Returns
    -------
    str
        The first whitespace-separated value from the line

    Raises
    ------
    ValueError
        If the line is empty or contains only whitespace
    """
    parts = line.split()
    if not parts:
        raise ValueError(
            f"Line {line_num}: Expected {field_name}, got empty line or whitespace"
        )
    return parts[0]


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
    with open(sim_file) as f:
        sim_lines = f.read().splitlines()

    line_index = iwfm.skip_ahead(0, sim_lines, 3)  # skip comments
    sim_dict['preout'] = _safe_get_value(sim_lines[line_index], line_index, 'preout filename')

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)
    sim_dict['gw'] = _safe_get_value(sim_lines[line_index], line_index, 'groundwater filename')

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)
    sim_dict['stream'] = _safe_get_value(sim_lines[line_index], line_index, 'stream filename')

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)
    temp = _safe_get_value(sim_lines[line_index], line_index, 'lake filename')
    if temp[0] == '/':   # check for presence of lake file
        lake_file = ''
    else:
        lake_file = temp
    sim_dict['lake'] = lake_file

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)
    sim_dict['rootzone'] = _safe_get_value(sim_lines[line_index], line_index, 'rootzone filename')

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)
    sim_dict['smallwatershed'] = _safe_get_value(sim_lines[line_index], line_index, 'smallwatershed filename')

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)
    sim_dict['unsat'] = _safe_get_value(sim_lines[line_index], line_index, 'unsaturated zone filename')

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)
    sim_dict['irrfrac'] = _safe_get_value(sim_lines[line_index], line_index, 'irrigation fraction filename')

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)
    sim_dict['supplyadj'] = _safe_get_value(sim_lines[line_index], line_index, 'supply adjustment filename')

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)
    sim_dict['precip'] = _safe_get_value(sim_lines[line_index], line_index, 'precipitation filename')

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)
    sim_dict['et'] = _safe_get_value(sim_lines[line_index], line_index, 'ET filename')

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)
    sim_dict['start'] = _safe_get_value(sim_lines[line_index], line_index, 'start date')

    line_index = iwfm.skip_ahead(line_index + 2, sim_lines, 0)
    sim_dict['step'] = _safe_get_value(sim_lines[line_index], line_index, 'time step')

    line_index = iwfm.skip_ahead(line_index + 1, sim_lines, 0)
    sim_dict['end'] = _safe_get_value(sim_lines[line_index], line_index, 'end date')  

    return sim_dict
