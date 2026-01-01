# iwfm_exe_time.py
# Extract the simulation time from SimulationMessages.out and write to
# a file as the number of seconds to execute the model
# Copyright (C) 2018-2026 University of California
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


def iwfm_exe_time(infile='SimulationMessages.out',outfile='exe_time.smp'):
    ''' iwfm_exe_time() - Extract the simulation time from SimulationMessages.out 
              and write to a file as the number of seconds to execute the model

    Parameters
    ----------
    infile : str
        SimulationMessages.out file name

    outfile : str
        output file name
    
    Returns:
    ----------
    time : float
        number of seconds to execute the model

    '''
    import iwfm 
    iwfm.file_test(infile)

    # read infile
    with open(infile, 'r') as f:
        lines = f.readlines()

    # find the line containing 'TOTAL RUN TIME'
    for line in lines:
        if 'TOTAL RUN TIME' in line:
            break

    # parse the line
    line = line.split()[3:]

    # convert the time to seconds
    time = 0
    if line[1] == 'HOURS':
        time += float(line[0]) * 3600
        line = line[2:]
    if line[1] == 'MINUTES':
        time += float(line[0]) * 60
        line = line[2:]
    if line[1] == 'SECONDS':
        time += float(line[0])

    # write the time to the output smp-format file
    with open(outfile, 'w') as f:
        f.write(f' EXETIME          10/31/1985   00:00:00            {time}           \n')
    return time

if __name__ == "__main__":
    ''' Run iwfm_exe_time() from command line '''

    infile='SimulationMessages.out'
    outfile='exe_time.smp'
    time = iwfm_exe_time(infile,outfile)
    print(f'  Model ran in {time:,} seconds')
    print(f'  Wrote result to {outfile}\n')

