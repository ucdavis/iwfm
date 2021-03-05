# ftp_fetch.py
# download a file using FTP
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


def ftp_fetch(server, dir, filename='download.txt', verbose=False):
    """ ftp_fetch() - Downloads a file from a server and saves to
        the specified directory and file name

    Parameters:
      server          (str):   URL ir INET address of FTP server
      dir             (str):   Download directory name
      filename        (str):   Download file name
    
    Return:
      nothing
        
    """
    import ftp

    ftp = ftplib.FTP(server)
    ftp.login()  # anonymous login
    ftp.cwd(dir)
    with open(filename, 'wb') as out:
        ftp.retrbinary('RETR ' + filename, out.write)
    if verbose:
        print(f'  Downloaded \'{filename}\' ')
    return 
