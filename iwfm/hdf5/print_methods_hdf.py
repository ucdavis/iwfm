# print_methods_hdf.py 
# print dll methods for an hdf file
# Copyright (C) 2018-2024 University of California
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

def print_methods_hdf(filename, spacing=20, verbose=False):
    '''print_methods_hdf() - print dll methods for an hdf file

    Parameters
    ----------
    filename : str
        name of hdf5 file

    spacing : int, default = 20
        print spacing    

    Returns
    -------
    methods : list
        list of methods

    '''
    import h5py
    import iwfm as iwfm

    iwfm.file_test(filename)

    object = h5py.File(filename)

    if verbose:
        print(f'  Opened {filename}')

#    methodList = [method for method in dir(object) if callable(getattr(object, method))]

    methodList = []
    for method_name in dir(object):
        print(f'  ==> {method_name=}')
        try:
            if callable(getattr(object, method_name)):
                methodList.append(str(method_name))
        except Exception:
            methodList.append(str(method_name))
    processFunc = (lambda s: ' '.join(s.split())) or (lambda s: s)
    for method in methodList:
        try:
            print(str(method.ljust(spacing)) + ' ' +
                processFunc(str(getattr(object, method).__doc__)[0:90]))
        except Exception:
            print(method.ljust(spacing) + ' ' + ' getattr() failed')


    return methodList

if __name__ == '__main__':methods_hdf() from command line '
    import sys
    import os
    import iwfm as iwfm
    import iwfm.debug as dbg


    if len(sys.argv) > 1:  # arguments are listed on the command line
        filename = sys.argv[1]
    else:  # ask for file names from terminal
        filename    = input('IWFM HDF file name: ')

    print(f'  ==> {filename=}')

    iwfm.file_test(filename)

    dbg.exe_time()  # initialize timer

    methods = print_methods_hdf(filename, verbose=True)

    print(f'  Read {len(methods):,} methods from {filename}.')

    # write methods to text file 
    outfile = filename.split('.')[0] + '_metnods.txt'
    with open(outfile, 'w') as f:
        for method in methods:
            f.write(f'{method}\n')

    dbg.exe_time()  # print elapsed time
