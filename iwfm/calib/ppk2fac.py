# ppk2fac.py
# Use kriging to translate parameter values from pilot points to model nodes.
# From ppk2faci.F90 by Matt Tonkin
# Program PPK2FACI performs the first step in kriging from a set of
# pilot points to an IWFM finite element mesh; it calculates the
# factors by which the value assigned to each pilot point contributes to
# the value at each mesh node.
# Copyright (C) 2020-2023 University of California
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

def read_pp_file(pp_file, verbose=False):
    """ read_pp_file() - Read pilot points file and return list of tuples.
        
    Parameters
    ----------
    pp_file : str
        Name of pilot points file
            
    verbose : bool, default=False
        Turn command-line output on or off
            
    Returns
    -------
    pp_list : list
        List of tuples representing pilot points. Each tuple contains (id, x, y, zone, value).
    """

    with open(pp_file, 'r') as f:
        pp_list = []
        for line in f:
            if line.startswith('#'):
                continue
            else:
                line = line.strip()
                line = line.split()
                pp_list.append(tuple(line))
    if verbose:
        print(f'  Read {len(pp_list):,} pilot points from {pp_file}')

    return pp_list

def read_struct_file(struct_file, verbose=False):
    """ read_struct_file() - Read IWFM structure file and return list of tuples.
        
    Parameters
    ----------
    struct_file : str
        Name of IWFM structure file
            
    verbose : bool, default=False
        Turn command-line output on or off
                
    Returns
    -------
    struct_list : list
        List of tuples representing structures. Each tuple contains (id, x, y, zone).
    """
    with open(struct_file, 'r') as f:
        struct_line = []
        for line in f:
            if line.startswith('#'):
                continue
            else:
                line = line.strip()
                line = line.split()
                #print(f'  {line} ')
                struct_line.append(line)
    if verbose:
        print(f'  Read {len(struct_line):,} lines from {struct_file}')

    structure_d, variogram_d, i = {}, {}, 0
    while i < len(struct_line):
        if len(struct_line[i])>0 and struct_line[i][0].lower() == 'structure':
            name = struct_line[i][1]
            nugget, transform, num_variograms, variogram_names, maxpowervar = 0.0, 'none', 0, [], 1.0    # defaults
            while struct_line[i][0].lower() != 'end':
                if struct_line[i][0].lower() == 'nugget':
                    nugget = float(struct_line[i][1])
                elif struct_line[i][0].lower() == 'transform':
                    transform = struct_line[i][1].lower()
                elif struct_line[i][0].lower() == 'maxpowervar':
                    maxpowervar = float(struct_line[i][1])
                elif struct_line[i][0].lower() == 'numvariogram':
                    num_variograms = int(struct_line[i][1])
                    variogram_names = []
                elif struct_line[i][0].lower() == 'variogram':
                    variogram_names.append([struct_line[i][1],struct_line[i][2]])
                i += 1
            structure_d[name]=[nugget, transform, maxpowervar, num_variograms, variogram_names]

        elif len(struct_line[i])>0 and struct_line[i][0].lower() == 'variogram':
            name = struct_line[i][1]
            vartype, bearing, a, anisotropy = 0, 0, 0.0, 0.0    # defaults
            while struct_line[i][0].lower() != 'end':
                if struct_line[i][0].lower() == 'vartype':
                    vartype = int(struct_line[i][1])
                elif struct_line[i][0].lower() == 'bearing':
                    bearing = int(struct_line[i][1])
                elif len(struct_line[i][0]) == 1 and struct_line[i][0].lower() == 'a':
                    a = float(struct_line[i][1])
                elif struct_line[i][0].lower() == 'anisotropy':
                    anisotropy = float(struct_line[i][1])
                i += 1
            variogram_d[name]=[vartype, bearing, a, anisotropy]
        else:
            i += 1

    return structure_d, variogram_d

def read_zone_file(zone_file, verbose=False):
    """ read_zone_file() - Read IWFM zone file and return list of tuples.
    
    Parameters
    ----------
    
    zone_file : str
        Name of IWFM zone file
        
    verbose : bool, default=False
        Turn command-line output on or off
        
    Returns
    -------
    zone_list : list
        List of tuples representing zones. Each tuple contains (id, x, y, zone).
    """
    with open(zone_file, 'r') as f:
        zone_lines = []
        for line in f:
            if line.startswith('C'):
                continue
            else:
                line = line.strip()
                line = line.split()
                zone_lines.append(line)
    if verbose:
        print(f'  Read {len(zone_lines):,} lines from {zone_file}')

    # convert list to dictionary
    zone_dict, zones = {}, []
    for line in zone_lines[1:]:
        zone_dict[int(line[0])] = int(line[1])
        if int(line[1]) not in zones:
            zones.append(int(line[1]))

    return zone_dict, zones

def getXY(pp_list):
    ''' getXY() - Extract x and y coordinates from pilot points list.
    
    Parameters
    ----------
    pp_list : list
        List of tuples representing pilot points. Each tuple contains (id, x, y, zone, value).
        
    Returns
    -------
    x : list
        List of x coordinates.
        
    y : list
        List of y coordinates.
    '''
    import numpy as np

    x = [float(i[1]) for i in pp_list]
    y = [float(i[2]) for i in pp_list]

    # zip x and y to one list and convert to numpy array for computation
    return np.array(list(zip(x, y)))

def min_dist(XY):
    '''  min_dist() - Calculate minimum distance between two points.
    
    Parameters
    ----------
    XY : numpy array of [x,y] coordinates
        List of pilot point coordinates.
        
    Returns
    -------
    min_dist : float
        Minimum distance between two points.
    '''
    import numpy as np

    #  calculate minimum distance between two points
    min_dist = 9999999999999

    for i in range(len(XY)-1):
        for j in range(i + 1, len(XY)):
            dist = np.sqrt((XY[i][0] - XY[j][0]) ** 2 + (XY[i][1] - XY[j][1]) ** 2)
            if dist < min_dist:
                min_dist = dist
                if min_dist == 0.0:
                    print(f'  Error: Two (or more) pilot points coincide.')
                    print(f'  Pilot points {i} at {XY[i]}, and {j} at {XY[j]}')
                    printf('  Exiting...\n')
                    exit()
    return min_dist

def read_zone_struct(zone_struct_file, verbose=False):
    """ read_zone_struct() - Read zone-structure file and return dictionary.
    
    Parameters
    ----------
    zone_struct_file : str
        Name of zone-structure file.
        
    verbose : bool, default=False
        Turn command-line output on or off
        
    Returns
    -------
    zone_struct_dict : dict
        Dictionary of zone-structure relationships.
    """
    with open(zone_struct_file, 'r') as f:
        zone_struct_lines = []
        for line in f:
            if line.startswith('C') or line.startswith('#'):
                continue
            elif len(line) > 0:
                line = line.strip()
                line = line.split()
                zone_struct_lines.append(line)
    if verbose:
        print(f'  Read {len(zone_struct_lines):,} lines from {zone_struct_file}')

    # convert list to dictionary
    zone_struct_dict = {}
    for line in zone_struct_lines:
        zone_struct_dict[int(line[0])] = line[1]

    return zone_struct_dict
 
def get_krige_weights(zone_struct_d, structure_d, variogram_d, krige_type, verbose=False):
    """ get_krige_weights() - Calculate kriging weights for each zone.
    
    Parameters
    ----------
    zone_struct_d : dict
        Dictionary of zone-structure relationships.
    
    structure_d : dict
        Dictionary of structures.

    variogram_d : dict
        Dictionary of variograms.

    krige_type : str
        Type of kriging to use. 'o' for ordinary or 's' for simple.

    verbose : bool, default=False
        Turn command-line output on or off

    Returns
    -------
    krig_wts : dict
        Dictionary of kriging weights for each zone.
    """
    import numpy as np
    import iwfm as iwfm

    print(f'  {zone_struct_d}')

    #  evaluate kriging weights for each zone
    krig_wts_d = {}
    for zone in zone_struct_d:
        if verbose: print(f'  Calculating kriging weights for zone {zone}')
        struct = zone_struct_d[zone]
        print(f'  {struct=}')
        nugget, transform, maxpowervar, num_variograms, variogram_names = structure_d[struct]
        print(f'  {nugget=}, {transform=}, {maxpowervar=}, {num_variograms=}, {variogram_names=}')
        if krige_type == 'o':   # ordinary kriging
            k_ktype, s_skmean = 1, 0.0
        else:                   # simple kriging
            k_ktype, s_skmean = 0, 1.0
        print(f'  {k_ktype=}, {s_skmean=}')

        krig_wts_d[zone] = iwfm.krige_weights(nugget, transform, maxpowervar, num_variograms, variogram_names,
                                            k_ktype, s_skmean, variogram_d, verbose=verbose)
    return krig_wts_d

def gslib2df(filename, xcol, ycol, vcol, tmin, tmax, verbose=False):
    """ gslib2df() - Read a GSLIB Geo-EAS file and return a pandas dataframe.
    
    Parameters
    ----------
    filename : str
        Name of GSLIB Geo-EAS-formatted file.
        
    xcol : numpy array
        Column containing x coordinates.
        
    ycol : numpy array
        Column containing y coordinates.
        
    vcol : numpy array
        Column containing values.
        
    tmin : float
        Minimum data value to be kriged, smaller ignored.
        
    tmax : float
        Maximum data value to be kriged, greater ignored.
        
    verbose : bool, default=False
        Turn command-line output on or off
        
    Returns
    -------
    df : pandas dataframe
        input data from a simplified Geo-EAS formatted file in a pandas dataframe formatted
        for geostatspy.geostats.kb2d().
    """
    import pandas as pd
    import geostatspy.geostats as geostats

    df = geostats.GSLIB2Dataframe(filename, xcol, ycol, vcol, tmin, tmax, verbose=verbose)

    #  read GSLIB file
    #df = pd.read_csv(filename, sep='\s+', header=None, names=['x', 'y', 'v'])
    #
    #  remove data outside of tmin and tmax
    #df = df[(df['v'] >= tmin) & (df['v'] <= tmax)]

    return df

def call_kb2d(df,xcol,ycol,vcol,tmin,tmax,nx,xmn,xsiz,ny,ymn,ysiz,nxdis,nydis,ndmin,ndmax,radius,ktype,skmean,vario):
    """ call_kb2d() - Call kb2d() from geostatspy.geostats.
    
    Parameters
    ----------
    df : pandas dataframe
        input data from a simplified Geo-EAS formatted file in a pandas dataframe
        
    xcol : numpy arrray
        Column containing x coordinates.
        
    ycol : numpy array
        Column containing y coordinates.
        
    vcol : numpy array
        Column containing values.
        
    tmin : float
        Minimum data value to be kriged, smaller ignored.
        
    tmax : float
        Maximum data value to be kriged, greater ignored.
        
    nx : int
        Number of kriging grid nodes in x direction.
        
    xmn : float
        Minimum x coordinate of kriging grid.
        
    xsiz : float
        Size of kriging grid cells in x direction.
        
    ny : int
        Number of kriging grid nodes in y direction.
        
    ymn : float
        Minimum y coordinate of kriging grid.
        
    ysiz : float
        Size of kriging grid cells in y direction.
        
    nxdis : int
        Number of discretization points in x direction.
        
    nydis : int
        Number of discretization points in y direction.
        
    ndmin : int
        Minimum number of data points to use for kriging.
        
    ndmax : int
        Maximum number of data points to use for kriging.
        
    radius : float
        Maximum search radius.
            
    ktype : int
        Kriging type, 0=SK, 1=OK, 2=non-stationary SK, 3=non-stationary OK.
        
    skmean : float
        Mean of the variable for simple kriging.
        
    vario : list
        List of variogram parameters.
        
    Returns
    -------
    kmap : numpy array
        Kriging map.
            
    vmap : numpy array
        Variance map.   
            
    """
    import geostatspy.geostats as geostats

    kmap, vmap = geostats.kb2d(df,xcol,ycol,vcol,tmin,tmax,nx,xmn,xsiz,ny,ymn,ysiz,nxdis,nydis,
        ndmin,ndmax,radius,ktype,skmean,vario)

    return kmap, vmap


def par2fac(pp_list, node_file, struct_file, zone_file, factors_outfile, regul_outfile,
            zone_struct_file, krige_type='o', krige_radius=1000, min_ppoints=3, max_ppoints=10, verbose=False):
    ''' par2fac() - Calculate kriging factors and write to output file.
    
    Parameters
    ----------
    pp_list : list
        List of tuples representing pilot points. Each tuple contains (id, x, y, zone, value).
        
    node_file : str
        Name of IWFM node file.
        
    struct_file : str
        Name of IWFM structure file.
        
    zone_file : str
        Name of IWFM zone file. 
        
    factors_outfile : str
        Name of output file for kriging factors.
        
    regul_outfile : str
        Name of output file for regularization factors.
    
    zone_struct_file : str
        Name of zone-structure file.

    krige_type : str; default = 'o'
        Type of kriging to use. 'o' for ordinary or 's' for simple.

    krige_radius : float; default = 1000
        Search radius for kriging.

    min_ppoints : int; default = 3
        Minimum number of pilot points for interpolation.

    max_ppoints : int; default = 10
        Maximum number of pilot points for interpolation.

    verbose : bool, default=False
        Turn command-line output on or off
        
    Returns
    -------
    None
    '''
    import iwfm as iwfm
    import numpy as np
    import pandas as pd

    #  check for errors
    if max_ppoints < min_ppoints:
        print(f'\n  Error: max_ppoints ({max_ppoints}) must be greater than or equal to min_ppoints ({min_ppoints}).')
        print('  Exiting...\n')
        exit()

    # pilot points and (x,y) locations
    pp_list = read_pp_file(pp_file, verbose=verbose)
    pp_coord = getXY(pp_list)     # get (x,y) coordinats from pp_list
    md = min_dist(pp_coord)       # calculate minimum distance between two points
    if verbose: print(f'  Minimum distance between two pilot points is {md.round(2):,}')

    # model nodes and (x,y) coordinates
    node_coord, node_list, factor = iwfm.iwfm_read_nodes(node_file)
    if verbose: print(f'  Read {len(node_list):,} nodes from {node_file}')

    # kriging structures and variograms
    structure_d, variogram_d = read_struct_file(struct_file, verbose=verbose)
    if verbose: print(f'  Read {len(structure_d):,} structure(s) from {struct_file}')

    # zone for each model node
    zone_dict, zones = read_zone_file(zone_file, verbose=verbose)
    if verbose: print(f'  Read {len(zones):,} zone(s) from {zone_file}')

    #  make sure  number of model nodes == number of nodes with a zone
    if len(node_list) != len(zone_dict):
        print(f'\n  Error: Number of nodes in {node_file} and {zone_file} must match.')
        print(f'  {len(node_list):,} nodes in {node_file} and {len(zone_dict):,} zones in {zone_file}')
        print('  Exiting...\n')
        exit()
        
    # get the structure for each zone
    zone_struct_d = read_zone_struct(zone_struct_file, verbose=verbose)
    if verbose: print(f'  Read {len(zone_struct_d):,} zone(s) from {zone_struct_file}')

    # evaluate kriging weights for each zone
    krig_wts = get_krige_weights(zone_struct_d, structure_d, variogram_d, krige_type, verbose=verbose)

    if krige_type == 'o':   # ordinary kriging
        k_ktype, s_skmean = 1, 0.0
    else:                   # simple kriging
        k_ktype, s_skmean = 0, 1.0




    #  get krige factors and base set values
    #krige_factors = calib.krige(A, B)
    #values = [val for _, _, _, val in B]

    count = 0
    return count

def par2iwfm(A, B):
    """ par2iwfm() - Implement krige function to create new parameter values.

    Parameters
    ----------
    A : list
        List of tuples representing grid A points. Each tuple contains (id, x, y) coordinates.
    
    B : list
        List of tuples representing grid B points. Each tuple contains (id, x, y, value) coordinates.
    
    Returns
    -------
    a_values : list
        List of calculated floats representing values for A in B's grid
    """
    import iwfm.calib as calib
    import numpy as np

    #  get krige factors and base set values
    krige_factors = calib.krige(A, B)
    values = [val for _, _, _, val in B]
  
    #  convert to numpy arrays for computation
    first_array = np.array(values)
    second_array = np.array(krige_factors)
    
    #  Element-wise matrix multiplication
    a_value_array = first_array * second_array
    a_values = [np.sum(array) for array in a_value_array]

    return a_values

# Sample data for grid A
new_set = [
    (1, 1.0, 2.0),
    (2, 2.0, 3.0),
    (3, 5.0, 4.0),
    (4, 6.0, 7.0),
    (5, 10.0, 4.0),
    (6, 6.0, 3.0),
    (7, 8.0, 1.0),
    (8, 12.0, 12.0),
]

# Sample data for grid B
base_set = [
    (1, 2.0, 1.0, 80.0),
    (2, 3.0, 3.0, 120.0),
    (3, 4.0, 6.0, 85.0),
    (4, 5.0, 10.0, 40.0),
    (5, 7.0, 8.0, 50.0),
    (6, 8.0, 6.0, 55.0),
    (7, 10.0, 6.0, 80.0),
    (8, 7.0, 3.0, 50.0),
    (9, 5.0, 1.0, 120.0),
    (10, 9.0, 1.0, 55.0),
]

# Sample larger data for grid B
base_set_big = [
    (1, 2.0, 1.0, 80.0),
    (2, 3.0, 3.0, 120.0),
    (3, 4.0, 6.0, 85.0),
    (4, 5.0, 10.0, 40.0),
    (5, 7.0, 8.0, 50.0),
    (6, 8.0, 6.0, 55.0),
    (7, 10.0, 6.0, 80.0),
    (8, 7.0, 3.0, 50.0),
    (9, 5.0, 1.0, 120.0),
    (10, 9.0, 1.0, 55.0),
    (11, 1.0, 14.0, 70.0),
    (12, 4.0, 14.5, 70.0),
    (13, 8.0, 12.0, 75.0),
    (14, 10.0, 15.0, 65.0),
    (15, 14.0, 13.0, 63.0),
    (16, 16.0, 11.0, 57.0),
    (17, 14.0, 2.0, 75.0),
    (18, 16.0, 6.0, 62.0),
]


if __name__ == '__main__':
    ''' Run ppk2fac() from command line '''

    #    a_values = par2iwfm(new_set, base_set)
    #    print(a_values)

    import sys
    import iwfm.debug as idb
    import iwfm as iwfm

    if len(sys.argv) > 1:  # arguments are listed on the command line
        pp_file          = sys.argv[1]
        node_file        = sys.argv[2]
        struct_file      = sys.argv[3]
        zone_file        = sys.argv[4]
        zone_struct_file = sys.argv[5]
        factors_outfile  = sys.argv[6]
        regul_outfile    = sys.argv[7]
        krige_type       = sys.argv[8].lower()
        krige_radius     = float(sys.argv[9])
        min_ppoints      = int(sys.argv[10])
        max_ppoints      = int(sys.argv[11])

        # IWFMnodes.dat structure.dat IWFMzones.dat factors.dat regul.dat
    else:  # ask for file names from terminal
        pp_file          = input('Pilot points file name: ')
        node_file        = input('IWFM Node.dat file name: ')
        struct_file      = input('Structure file name: ')
        zone_file        = input('Zone file name: ')
        zone_struct_file = input('Zone-structure file name: ')
        factors_outfile  = input('Factors output file name: ')
        regul_outfile    = input('Regularization output file name: ')
        krige_type       = input('[O]rdinary or [S]imple kriging: ').lower()
        krige_radius     = float(input('Search radius: '))
        min_ppoints      = int(input('Minimum number of pilot points for interpolation: '))
        max_ppoints      = int(input('Maximum number of pilot points for interpolation: '))

    print(f'  => {pp_file=}')
    print(f'  => {node_file=}')
    print(f'  => {struct_file=}')
    print(f'  => {zone_file=}')
    print(f'  => {zone_struct_file=}')
    print(f'  => {factors_outfile=}')
    print(f'  => {regul_outfile=}')
    print(f'  => {krige_type=}')
    print(f'  => {krige_radius=}')
    print(f'  => {min_ppoints=}')
    print(f'  => {max_ppoints=}\n')

    iwfm.file_test(pp_file)
    iwfm.file_test(node_file)
    iwfm.file_test(struct_file)
    iwfm.file_test(zone_file)

    idb.exe_time()  # initialize timer
    count = par2fac(pp_file, node_file, struct_file, zone_file, factors_outfile, regul_outfile,
                    zone_struct_file, krige_type, krige_radius, min_ppoints, max_ppoints, verbose=True)

    print(f'  Wrote {count} factors to {factors_outfile} and {regul_outfile}')  # update cli
    idb.exe_time()  # print elapsed time

        
