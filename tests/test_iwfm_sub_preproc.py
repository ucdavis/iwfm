# test_iwfm_sub_preproc.py
# unit tests for iwfm_sub_preproc function
# Copyright (C) 2026 University of California
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

import polars as pl
from pathlib import Path
from unittest.mock import patch
from iwfm.dataclasses import PreprocessorFiles


def _load_iwfm_sub_preproc():
    """Load the iwfm_sub_preproc function dynamically."""
    from importlib.util import spec_from_file_location, module_from_spec
    base = Path(__file__).resolve().parents[1] / "iwfm" / "iwfm_sub_preproc.py"
    spec = spec_from_file_location("iwfm_sub_preproc", str(base))
    assert spec is not None, "Failed to load module specification"
    mod = module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return getattr(mod, "iwfm_sub_preproc")


iwfm_sub_preproc = _load_iwfm_sub_preproc()


class TestIwfmSubPreproc:
    """Tests for the iwfm_sub_preproc function."""

    @patch('iwfm.iwfm_read_preproc')
    @patch('iwfm.new_pp_files')
    @patch('iwfm.get_elem_list')
    @patch('iwfm.sub_pp_node_list')
    @patch('iwfm.iwfm_read_nodes')
    @patch('iwfm.sub_pp_streams')
    @patch('iwfm.sub_pp_node_file')
    @patch('iwfm.sub_pp_elem_file')
    @patch('iwfm.sub_pp_strat_file')
    @patch('iwfm.sub_pp_stream_file')
    @patch('iwfm.sub_pp_file')
    def test_basic_execution(self, mock_sub_pp_file, mock_stream_file,
                              mock_strat_file, mock_elem_file, mock_node_file,
                              mock_sub_streams, mock_read_nodes, mock_node_list,
                              mock_elem_list, mock_new_dict, mock_read_preproc,
                              tmp_path):
        """Test basic execution of iwfm_sub_preproc."""
        # Setup mocks
        mock_read_preproc.return_value = (PreprocessorFiles(
            node_file='nodes.dat',
            elem_file='elems.dat',
            strat_file='strat.dat',
            stream_file='streams.dat',
            lake_file='none',
        ), False)

        mock_new_dict.return_value = PreprocessorFiles(
            prename='sub_pre.dat',
            node_file='sub_nodes.dat',
            elem_file='sub_elems.dat',
            strat_file='sub_strat.dat',
            stream_file='sub_streams.dat',
            lake_file='none',
        )

        mock_elem_list.return_value = ([1, 2, 3], [1], {1: 1, 2: 2, 3: 3}, {1: 1, 2: 2, 3: 3})
        mock_node_list.return_value = [1, 2, 3, 4]
        mock_read_nodes.return_value = ([[1, 100.0, 200.0], [2, 110.0, 210.0]], [1, 2], 1.0)
        mock_sub_streams.return_value = ([], {}, {}, '', [], [])
        mock_elem_file.return_value = [[1, 1, 2, 3, 4]]

        # Create temp files
        pp_file = tmp_path / "preproc.dat"
        pp_file.write_text("C preprocessor file")
        elem_pairs = tmp_path / "elem_pairs.dat"
        elem_pairs.write_text("1,1\n2,2\n3,3")
        out_base = str(tmp_path / "submodel")

        result = iwfm_sub_preproc(str(pp_file), str(elem_pairs), out_base, verbose=False)

        # Verify return values
        assert result is not None
        assert len(result) == 7  # pre_files_new, sub_elem_list, new_srs, elem_dict, sub_node_list, snode_dict, lake_info

    @patch('iwfm.iwfm_read_preproc')
    @patch('iwfm.new_pp_files')
    @patch('iwfm.get_elem_list')
    @patch('iwfm.sub_pp_node_list')
    @patch('iwfm.iwfm_read_nodes')
    @patch('iwfm.sub_pp_streams')
    @patch('iwfm.sub_pp_node_file')
    @patch('iwfm.sub_pp_elem_file')
    @patch('iwfm.sub_pp_strat_file')
    @patch('iwfm.sub_pp_stream_file')
    @patch('iwfm.sub_pp_file')
    def test_creates_parquet_file(self, mock_sub_pp_file, mock_stream_file,
                                   mock_strat_file, mock_elem_file, mock_node_file,
                                   mock_sub_streams, mock_read_nodes, mock_node_list,
                                   mock_elem_list, mock_new_dict, mock_read_preproc,
                                   tmp_path):
        """Test that parquet file is created with node coordinates."""
        mock_read_preproc.return_value = (PreprocessorFiles(
            node_file='nodes.dat',
            elem_file='elems.dat',
            strat_file='strat.dat',
            stream_file='streams.dat',
            lake_file='none',
        ), False)

        mock_new_dict.return_value = PreprocessorFiles(
            prename='sub_pre.dat',
            node_file='sub_nodes.dat',
            elem_file='sub_elems.dat',
            strat_file='sub_strat.dat',
            stream_file='sub_streams.dat',
            lake_file='none',
        )

        mock_elem_list.return_value = ([1], [1], {1: 1}, {1: 1})
        mock_node_list.return_value = [1, 2]
        mock_read_nodes.return_value = (
            [[1, 100.0, 200.0], [2, 150.0, 250.0]],
            [1, 2],
            1.0
        )
        mock_sub_streams.return_value = ([], {}, {}, '', [], [])
        mock_elem_file.return_value = [[1, 1, 2, 3, 4]]

        pp_file = tmp_path / "preproc.dat"
        pp_file.write_text("C preprocessor")
        elem_pairs = tmp_path / "elem_pairs.dat"
        elem_pairs.write_text("1,1")
        out_base = str(tmp_path / "submodel")

        iwfm_sub_preproc(str(pp_file), str(elem_pairs), out_base, verbose=False)

        # Check parquet file was created
        parquet_file = tmp_path / "submodel_df.parquet"
        assert parquet_file.exists()

        # Read and verify parquet contents
        df = pl.read_parquet(str(parquet_file))
        assert 'node_id' in df.columns
        assert 'easting' in df.columns
        assert 'northing' in df.columns

    @patch('iwfm.iwfm_read_preproc')
    @patch('iwfm.new_pp_files')
    @patch('iwfm.get_elem_list')
    @patch('iwfm.sub_pp_node_list')
    @patch('iwfm.iwfm_read_nodes')
    @patch('iwfm.sub_pp_streams')
    @patch('iwfm.sub_pp_node_file')
    @patch('iwfm.sub_pp_elem_file')
    @patch('iwfm.sub_pp_strat_file')
    @patch('iwfm.sub_pp_stream_file')
    @patch('iwfm.sub_pp_file')
    def test_creates_pickle_files(self, mock_sub_pp_file, mock_stream_file,
                                   mock_strat_file, mock_elem_file, mock_node_file,
                                   mock_sub_streams, mock_read_nodes, mock_node_list,
                                   mock_elem_list, mock_new_dict, mock_read_preproc,
                                   tmp_path):
        """Test that pickle files are created."""
        mock_read_preproc.return_value = (PreprocessorFiles(
            node_file='nodes.dat',
            elem_file='elems.dat',
            strat_file='strat.dat',
            stream_file='streams.dat',
            lake_file='none',
        ), False)

        mock_new_dict.return_value = PreprocessorFiles(
            prename='sub_pre.dat',
            node_file='sub_nodes.dat',
            elem_file='sub_elems.dat',
            strat_file='sub_strat.dat',
            stream_file='sub_streams.dat',
            lake_file='none',
        )

        mock_elem_list.return_value = ([1, 2], [1], {1: 1, 2: 2}, {1: 1, 2: 2})
        mock_node_list.return_value = [1, 2, 3]
        mock_read_nodes.return_value = ([[1, 100.0, 200.0]], [1], 1.0)
        mock_sub_streams.return_value = ([], {1: 1}, {}, '', [], [1])
        mock_elem_file.return_value = [[1, 1, 2, 3, 4]]

        pp_file = tmp_path / "preproc.dat"
        pp_file.write_text("C preprocessor")
        elem_pairs = tmp_path / "elem_pairs.dat"
        elem_pairs.write_text("1,1\n2,2")
        out_base = str(tmp_path / "submodel")

        iwfm_sub_preproc(str(pp_file), str(elem_pairs), out_base, verbose=False)

        # Check pickle files were created
        assert (tmp_path / "submodel_elems.bin").exists()
        assert (tmp_path / "submodel_nodes.bin").exists()
        assert (tmp_path / "submodel_snodes.bin").exists()
        assert (tmp_path / "submodel_sub_snodes.bin").exists()
        assert (tmp_path / "submodel_node_coords.bin").exists()
        assert (tmp_path / "submodel_elemnodes.bin").exists()

    @patch('iwfm.iwfm_read_preproc')
    @patch('iwfm.new_pp_files')
    @patch('iwfm.get_elem_list')
    @patch('iwfm.sub_pp_node_list')
    @patch('iwfm.iwfm_read_nodes')
    @patch('iwfm.sub_pp_streams')
    @patch('iwfm.sub_pp_lakes')
    @patch('iwfm.sub_pp_node_file')
    @patch('iwfm.sub_pp_elem_file')
    @patch('iwfm.sub_pp_strat_file')
    @patch('iwfm.sub_pp_stream_file')
    @patch('iwfm.sub_pp_lake_file')
    @patch('iwfm.sub_pp_file')
    def test_with_lakes(self, mock_sub_pp_file, mock_lake_file, mock_stream_file,
                        mock_strat_file, mock_elem_file, mock_node_file,
                        mock_sub_lakes, mock_sub_streams, mock_read_nodes,
                        mock_node_list, mock_elem_list, mock_new_dict,
                        mock_read_preproc, tmp_path):
        """Test execution with lake support."""
        mock_read_preproc.return_value = (PreprocessorFiles(
            node_file='nodes.dat',
            elem_file='elems.dat',
            strat_file='strat.dat',
            stream_file='streams.dat',
            lake_file='lakes.dat',
        ), True)

        mock_new_dict.return_value = PreprocessorFiles(
            prename='sub_pre.dat',
            node_file='sub_nodes.dat',
            elem_file='sub_elems.dat',
            strat_file='sub_strat.dat',
            stream_file='sub_streams.dat',
            lake_file='sub_lakes.dat',
        )

        mock_elem_list.return_value = ([1], [1], {1: 1}, {1: 1})
        mock_node_list.return_value = [1]
        mock_read_nodes.return_value = ([[1, 100.0, 200.0]], [1], 1.0)
        mock_sub_streams.return_value = ([], {}, {}, '', [], [])
        mock_sub_lakes.return_value = ([[1, 'Lake1', 100.0]], True)
        mock_elem_file.return_value = [[1, 1, 2, 3, 4]]

        pp_file = tmp_path / "preproc.dat"
        pp_file.write_text("C preprocessor")
        elem_pairs = tmp_path / "elem_pairs.dat"
        elem_pairs.write_text("1,1")
        out_base = str(tmp_path / "submodel")

        result = iwfm_sub_preproc(str(pp_file), str(elem_pairs), out_base, verbose=False)

        # Verify lake info is returned
        assert result[-1] == [[1, 'Lake1', 100.0]]
        # Verify lake pickle file created
        assert (tmp_path / "submodel_lakes.bin").exists()

    @patch('iwfm.iwfm_read_preproc')
    @patch('iwfm.new_pp_files')
    @patch('iwfm.get_elem_list')
    @patch('iwfm.sub_pp_node_list')
    @patch('iwfm.iwfm_read_nodes')
    @patch('iwfm.sub_pp_streams')
    @patch('iwfm.sub_pp_node_file')
    @patch('iwfm.sub_pp_elem_file')
    @patch('iwfm.sub_pp_strat_file')
    @patch('iwfm.sub_pp_stream_file')
    @patch('iwfm.sub_pp_file')
    def test_verbose_output(self, mock_sub_pp_file, mock_stream_file,
                            mock_strat_file, mock_elem_file, mock_node_file,
                            mock_sub_streams, mock_read_nodes, mock_node_list,
                            mock_elem_list, mock_new_dict, mock_read_preproc,
                            tmp_path, capsys):
        """Test verbose mode produces output."""
        mock_read_preproc.return_value = (PreprocessorFiles(
            node_file='nodes.dat',
            elem_file='elems.dat',
            strat_file='strat.dat',
            stream_file='streams.dat',
            lake_file='none',
        ), False)

        mock_new_dict.return_value = PreprocessorFiles(
            prename='sub_pre.dat',
            node_file='sub_nodes.dat',
            elem_file='sub_elems.dat',
            strat_file='sub_strat.dat',
            stream_file='sub_streams.dat',
            lake_file='none',
        )

        mock_elem_list.return_value = ([1], [1], {1: 1}, {1: 1})
        mock_node_list.return_value = [1]
        mock_read_nodes.return_value = ([[1, 100.0, 200.0]], [1], 1.0)
        mock_sub_streams.return_value = ([], {}, {}, '', [], [])
        mock_elem_file.return_value = [[1, 1, 2, 3, 4]]

        pp_file = tmp_path / "preproc.dat"
        pp_file.write_text("C preprocessor")
        elem_pairs = tmp_path / "elem_pairs.dat"
        elem_pairs.write_text("1,1")
        out_base = str(tmp_path / "submodel")

        iwfm_sub_preproc(str(pp_file), str(elem_pairs), out_base, verbose=True)

        captured = capsys.readouterr()
        assert "Read preprocessor file" in captured.out
        assert "Read submodel element pairs file" in captured.out
