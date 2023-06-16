# read_settings.py
# Read a PEST-style settings file
# Copyright (C) 2018-2020 Hydrolytics LLC
# Based on a PEST utility written by John Doherty
#-----------------------------------------------------------------------------
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
#-----------------------------------------------------------------------------


def read_settings(in_file='settings.fig'):
    ''' read_settings() - Subroutine read_settings reads the settings.fig file 
        located in the current directory. From John Doherty.

    Parameters
    ----------
    in_file : str
        settings file name

    Returns
    -------
    datespec : int
        1: dd/mm/yyyy, 2: mm/dd/yyyy

    headerspec : int
        1: header present, 0: header not present

    idate : int, default = 0
        zero unless datespec is incorrect in settings file

    iheader : int, default = 0
        zero unless headerspec is incorrect in settings file

    '''
    import os
    import iwfm as iwfm

    idate, iheader, datespec, headerspec = 0, 0, 0, ' '

    if not os.path.isfile(in_file):                         # test for input file
        print(f' Settings file \'{in_file}\' was not found in the current directory.')
        datespec, headerspec, idate, iheader = 2, 'no', 0, 0
        with open(in_file, 'w') as output_file:
            output_file.write("{}\n{}\n".format('colrow=no','date=mm/dd/yyyy'))
        print(f' Created a default \'{in_file}\' file')
        return datespec, headerspec, idate, iheader

    # == read the file into array file_lines
    file_lines = open(in_file).read().splitlines()          # open and read input file

    for cline in file_lines:
        cline = cline.lower().lstrip()  # convert to lower case and remove leading whitespace
        iequals = cline.find('=')
        aline = cline[0:iequals]

        if aline == 'date':
            aline = cline[iequals + 1:].lstrip()
            if aline[0:2] == 'dd' and aline[3:5] == 'mm':
                datespec = 1
            elif aline[0:2] == 'mm' and aline [3:5] == 'dd':
                datespec = 2
            else:
                idate = 1

        elif aline == 'colrow':
            aline = cline[iequals + 1:].lstrip().lower()
            if aline[0:3] == 'yes':
                headerspec='yes'
            elif aline[0:2] == 'no':
                headerspec='no'
            else:
                iheader = 1
        else:
            print(f' Error encountered while reading settings file \'{in_file}\'')
            sys.exit()
            return 0, 0, 0, 0

    return datespec, headerspec, idate, iheader
    

