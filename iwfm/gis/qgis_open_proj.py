# qgis_open_proj.py
# Open QGIS project
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


def qgis_open_proj(project_filename, debug=0):  # Open a project
    import os
    import qgis.core as qcore

    if debug:
        print("=> Opening QGIS project {}".format(project_filename))  # debugging

    # check for the project file
    if not os.path.isfile(
        os.path.join(os.getcwd(), project_filename)
    ):  # test for input file
        print(
            "=> Could not find {}".format(os.path.join(os.getcwd(), project_filename))
        )

    #  # for QGIS standalone app, bridge to sync loaded project with canvas
    #  bridge = QgsLayerTreeMapCanvasBridge(project.layerTreeRoot(), canvas)
    #  # NameError: name 'QgsLayerTreeMapCanvasBridge' is not defined

    #  apparently python 2 / QGIS2 way:
    #  project = qutil.QFile(project_filename)

    project = qcore.QgsProject.instance()  # instantiate

    project.read(
        project_filename
    )  # fill instantiated project (file name, not full path)
    if debug:
        print("=> Opened QGIS project {}".format(project_filename))  # debugging
        print("  => project: {}".format(project))
        print("  => project.filename(): '{}'".format(project.fileName()))
        print("  => title: '{}'".format(project.title()))
        print("  => layers: {}".format(project.count()))
        print("  ----------------------------")
    return project
