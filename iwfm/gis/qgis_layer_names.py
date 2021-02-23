# qgis_layer_names.py
# QGIS project layer names
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


def qgis_layer_names(project, debug=0):
    """ project is a qcore.QgsProject.instance() """
    root = project.layerTreeRoot()
    layers = project.mapLayers()
    if debug:
        print("=> Getting layer names")  # debugging
        print("  => project: {}".format(project))
        print("  => title: '{}'".format(project.title()))
        print("  => root:  '{}'".format(project.layerTreeRoot()))
        print("  => layers: {}".format(project.count()))
        print("  => mapLayers: {}".format(project.mapLayers()))
        print("  => values: {}".format(project.mapLayers().values()))

    # layer_names = [layer.name() for layer in project.mapLayers().values()]
    # layer_names = [layer.name() for layer in project.layerTreeRoot()]
    # layer_names = project.layerTreeRoot().children()
    layer_names = [layer.name() for layer in project.layerTreeRoot().children()]
    layer_paths = [layer.source() for layer in project.mapLayers().values()]
    if debug:
        print("  => Layer names:")
        print("      {}".format(layer_names))
        print("  => Layer paths:")
        print("      {}".format(layer_paths))
    return layer_names
