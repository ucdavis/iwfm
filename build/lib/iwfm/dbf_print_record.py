# dbf_print_record.py
# Print a DBF record to command line
# Copyright (C) 2020-2021 University of California
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


def dbf_print_record(db, rec):
    ''' dbf_print_record() - Print a DBF record to command line

    Parameters
    ----------
    db : dbf
        database object
    
    rec : int
        record number

    Returns
    -------
    nothing
    
    '''
    records = list(db)
    print(f'   Record {rec}: \n{records[rec]}')
    return
