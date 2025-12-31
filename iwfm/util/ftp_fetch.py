# ftp_fetch.py
# download a file using FTP
# Copyright (C) 2020-2025 University of California
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
    ''' ftp_fetch() - Download a file from a server and save to
        the specified directory and file name

    Parameters
    ----------
    server : str
        URL or INET address of FTP server

    dir : str
        Download directory name

    filename : str, default='download.txt'
        Download file name
      
    verbose : bool, default=False
        True = command-line output on
    
    Return
    ------
    nothing
        
    '''
    import ftplib
    import socket

    try:
        ftp = ftplib.FTP(server)
    except socket.gaierror as e:
        raise ConnectionError(f'Failed to resolve FTP server address: {server}') from e
    except socket.timeout as e:
        raise ConnectionError(f'Connection to FTP server {server} timed out') from e
    except OSError as e:
        raise ConnectionError(f'Failed to connect to FTP server {server}: {e}') from e

    try:
        ftp.login()  # anonymous login
    except ftplib.error_perm as e:
        ftp.quit()
        raise PermissionError(f'FTP login failed for {server}: {e}') from e

    try:
        ftp.cwd(dir)
    except ftplib.error_perm as e:
        ftp.quit()
        raise FileNotFoundError(f'FTP directory not found: {dir} on {server}') from e

    try:
        with open(filename, 'wb') as out:
            ftp.retrbinary('RETR ' + filename, out.write)
    except ftplib.error_perm as e:
        ftp.quit()
        raise FileNotFoundError(f'FTP file not found: {filename} in {dir} on {server}') from e
    except OSError as e:
        ftp.quit()
        raise IOError(f'Failed to write file {filename}: {e}') from e
    finally:
        try:
            ftp.quit()
        except:
            pass

    if verbose:
        print(f'  Downloaded \'{filename}\' ')

