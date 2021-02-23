# igsm2shp.py
# Create shapefiles for an IGSM model
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


def igsm2shp(main_file, shape_name, verbose=0, debug=0):
    """igsm2shp() takes the IGSM model main preprocessor file name
    and a base name for output files, reads the names of the
    component input files, reads the contents of these files, and
    creates node, element, stream node and stream reach shapefiles"""
    import sys
    import iwfm as iwfm
    import iwfm.gis as gis

    # get the path to the main_file
    path = main_file.split("/")
    main_path = "/".join(path[:-1])

    # == read main input file for other file names
    main_lines = open(main_file).read().splitlines()  # open and read input file
    line_index = iwfm.skip_ahead(0, main_lines, 6)  # skip comments
    elem_file = main_lines[line_index].split()[0]
    line_index += 1
    node_file = main_lines[line_index].split()[0]
    line_index += 1
    strat_file = main_lines[line_index].split()[0]
    line_index += 1
    stream_file = main_lines[line_index].split()[0]
    line_index += 1
    lake_file = main_lines[line_index].split()[0]
    line_index += 2
    char_file = main_lines[line_index].split()[0]

    # == test that each of the input files exist
    iwfm.file_test(elem_file)
    iwfm.file_test(node_file)
    iwfm.file_test(strat_file)
    iwfm.file_test(stream_file)
    if len(lake_file) > 1:
        iwfm.file_test(lake_file)
    iwfm.file_test(char_file)

    # read element file
    elem_nodes, elem_list = iwfm.igsm_read_elements(
        elem_file, debug=debug
    )  # read element info
    if verbose:
        print(
            "  Read nodes of {:,} elements from {}".format(len(elem_nodes), elem_file)
        )

    # read node file
    node_coords, node_list = iwfm.igsm_read_nodes(
        node_file, debug=debug
    )  # read node info
    if verbose:
        print(
            "  Read coordinates of {:,} nodes from {}".format(
                len(node_coords), node_file
            )
        )

    # read element characteristics file
    elem_char = iwfm.igsm_read_chars(
        char_file, elem_nodes, debug=debug
    )  # read element characteristics
    if verbose:
        print(
            "  Read characteristics for {:,} elements from {}".format(
                len(elem_char), char_file
            )
        )

    # read stratigraphy file
    node_strat, nlayers = iwfm.igsm_read_strat(
        strat_file, node_coords, debug=debug
    )  # read nodal stratigraphy
    if verbose:
        print(
            "  Read stratigraphy for {:,} nodes from {}".format(
                len(node_strat), strat_file
            )
        )

    # ** add code for case of no lakes file **
    lake_elems, lakes = iwfm.igsm_read_lake(
        lake_file, debug=debug
    )  # read lake elements
    if verbose:
        if len(lakes) > 1:
            print("  Read info for {:,} lakes from {}".format(len(lakes), lake_file))
        elif len(lakes) == 1:
            print("  Read info for {:,} lake from {}".format(len(lakes), lake_file))

    # read stream file
    reach_list, stnodes_dict, nsnodes = iwfm.igsm_read_streams(
        stream_file, debug=debug
    )  # read streams
    if verbose:
        print(
            "  Read info for {:,} stream reaches and {:,} stream nodes from {}\n".format(
                len(reach_list), nsnodes, stream_file
            )
        )

    # == Create node shapefile in UTM 10N (EPSG 26910)  ====================================
    gis.nodes2shp(
        node_coords, node_strat, nlayers, shape_name, verbose=verbose, debug=debug
    )

    # == Create element shapefile in UTM 10N (EPSG 26910)  =================================
    gis.igsm_elem2shp(
        elem_nodes,
        node_coords,
        elem_char,
        lake_elems,
        shape_name,
        verbose=verbose,
        debug=debug,
    )

    # == Create stream node shapefile in UTM 10N (EPSG 26910)  =============================
    gis.snodes2shp(
        nsnodes, stnodes_dict, node_coords, shape_name, verbose=verbose, debug=debug
    )

    # == Create stream reach shapefile in UTM 10N (EPSG 26910) =============================
    gis.reach2shp(
        reach_list, stnodes_dict, node_coords, shape_name, verbose=verbose, debug=debug
    )

    return


if __name__ == "__main__":
    " Run igsm2shp() from command line "
    import sys
    import iwfm.debug as idb
    import iwfm as iwfm

    if len(sys.argv) > 1:  # arguments are listed on the command line
        input_file = sys.argv[1]
        output_basename = sys.argv[2]
    else:  # ask for file names from terminal
        input_file = input("IGSM Preprocessor main file name: ")
        output_basename = input("Output shapefile basename: ")

    iwfm.file_test(input_file)

    idb.exe_time()  # initialize timer
    igsm2shp(input_file, output_basename, verbose=1)  # set verbose=1 for progress

    idb.exe_time()  # print elapsed time
