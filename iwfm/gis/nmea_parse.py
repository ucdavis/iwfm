# nmea_parse.py
# Reads a GIS waypoint file and writes lat-lon values
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


def nmea_parse(infile):
    ''' nmea_parse() - Read a GIS waypoint file and write lat-lon values

    Parameters
    ----------
    infile : str
        waypoint file name

    Returns
    -------
    nothing

    '''
    from pynmea.streamer import NMEAStream

    nmea_file = open(infile)
    nmea_stream = NMEAStream(stream_obj=nmea_file)
    next_data = nmea_stream.get_objects()
    nmea_objects = []
    while next_data:
        nmea_objects += next_data
        next_data = nmea_stream.get_objects()
    for nmea_obj in nmea_objects:
        if hasattr(nmea_obj, 'lat'):
            print(f'    Lat/Lon: ({nmea_obj.lat}, {nmea_obj.lon})')
    return
    