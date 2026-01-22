# get_zbudget_elemids.py 
# open an IWFM ZBudget HDF file and retreive all of the data
# using DWR's PyWFM package to interface wth the IWFM DLL
# Copyright (C) 2018-2026 University of California
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

def get_zbudget_elemids(zbud, zones_file, area_conversion_factor=0.0000229568411, area_units='ACRES', 
                        volume_conversion_factor=0.0000229568411, volume_units='ACRE-FEET', verbose=False):
    ''' get_zbudget_elemids() - open an IWFM Budget HDF file and retreive element ids

    Parameters
    ----------
    zbud : object
        IWFM ZBudget object (opened from HDF file)

    zones_file : str
        Name of IWFM Z-Budget Zones file

    area_conversion_factor : float, default = =0.0000229568411
        Area conversion factor

    area_units : str, default = 'ACRES'
        Area units

    volume_conversion_factor : float, default = =0.0000229568411
        Volume conversion factor

    volume_units : str, default = 'ACRE-FEET'
        Volume units

    verbose : bool, default=False
        Turn command-line output on or off

    Returns
    -------
    elemids : list
        List of element IDs
    '''
    
    from pywfm import IWFMZBudget
    import iwfm

    zbud.generate_zone_list_from_file(zone_definition_file=zones_file)

    n_zones = zbud.get_n_zones()
    if verbose: print(f'  ==>{n_zones=:,}\n')

    zone_list = zbud.get_zone_list()
    if verbose: print(f'  ==>{zone_list=}\n')
    if verbose: print(f'  ==>{zone_list[0]=}\n')

    zone_id = int(zone_list[0])
    column_ids = [15]     # 15 = 'Pumping by Element_Outflow (-)'

    zone_names = zbud.get_zone_names()
    if verbose: print(f'  ==>{zone_names=}\n')

    n_title_lines = zbud.get_n_title_lines()
    if verbose: print(f'  ==>{n_title_lines=}\n')

    for zn in range(0,3):
        if verbose: print(f'  ==============================\n')
        zone_id = int(zone_list[zn])
        zone_name = zone_names[zn]
        if verbose: print(f'  ==>{zone_id=}\t{zone_name=}\n')

        title_lines = zbud.get_title_lines(zone_id)
        if verbose: print(f'  ==>{title_lines=}\n')

        column_names, column_ids = zbud.get_column_headers_for_a_zone(zone_id)
        if verbose: print(f'  ==>{column_names=}\n  ==>{column_ids=}\n')

        zone_vals = zbud.get_values_for_a_zone(zone_id=zone_id, column_ids=15, 
                        begin_date=None, end_date=None, output_interval=None, 
                        area_conversion_factor=area_conversion_factor, area_units=area_units, 
                        volume_conversion_factor=volume_conversion_factor, volume_units=volume_units)
        if verbose: print(f'  ==>{zone_vals.size=:,}\n')
        if verbose: print(f'  ==>{zone_vals.shape=}\n')
        if verbose: print(f'  ==>{zone_vals=}\n')

        # column 1 = dates
        # write to excel file, column = dates, row = element
        # one tab for each of the following columns: 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 15, 17, 18, 20:n-2 (to/from adjacent elements)



#    if verbose: print(f'  ==>{n_title_lines=}')


#    if verbose: print(f'  ==>{n_title_lines=}')


#    elemids = zbud.get_elemids()           # get list of element IDs

    #elemids = zbud.iw_model_getelementids       # get elemet ids from zbudget file

    # get the file contents
    #zone_names      = zbud.get_zone_names()            # get list of zone names
    #zone_list       = zbud.get_zone_list()             # get list of zone IDs
    #zone_extent_ids = zbud.get_zone_extent_ids()       # get zone extent IDs

    # TODO: This function is incomplete - elemids is not properly extracted from zbud
    # Temporary fix to avoid undefined variable error
    elemids = []  # placeholder - needs proper implementation
    return elemids

if __name__ == '__main__':
    ''' Run get_zbudget_elemids() from command line '''
    import sys
    from pathlib import Path
    import iwfm
    from pywfm import IWFMZBudget
    import iwfm.debug as idb

    verbose=True

    if len(sys.argv) > 1:  # arguments are listed on the command line
        hdf_file   = sys.argv[1]
        zones_file = sys.argv[2]
    else:  # ask for file names from terminal
        hdf_file       = input('IWFM Z-Budget file name: ')
        zones_file     = input('IWFM Z-Budget Zones file name: ')

    iwfm.file_test(hdf_file)
    iwfm.file_test(zones_file)

    # if outfile_name extension != '.txt' add '.txt'
    hdf_path = Path(hdf_file)
    if hdf_path.suffix != '.txt':
        outfile_name = hdf_path.with_suffix('.txt')
        if verbose: print(f'  ==> {outfile_name=}')

    idb.exe_time()  # initialize timer
    
    # open hdf file
    zbud = IWFMZBudget(hdf_file)

    elemids = get_zbudget_elemids(zbud, zones_file, verbose=verbose)

    print(f'  {elemids=}')



#    print(f'  Created {outfile_name} with {count} worksheets.')

    idb.exe_time()  # print elapsed time
