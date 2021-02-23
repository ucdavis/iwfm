# qgis_init.py
# Initialize QGIS application
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


def qgis_init(debug=0):
    import qgis.core as qcore
    import init_qgis_paths as init_qgis_paths

    if debug:
        print("  => QGIS initializing")  # debugging
    app_path = init_qgis_paths()
    qcore.QgsApplication.setPrefixPath(app_path, True)  # Path to QGIS binary
    qgs = qcore.QgsApplication(
        [], True
    )  # Create a reference to the QgsApplication, True = enables GUI (for applications)
    qgs.initQgis()  # load providers
    if debug:
        print("  => QGIS initialized")  # debugging
    return
