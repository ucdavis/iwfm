# test_hdf5_hdf_metadata.py
# Tests for hdf5/hdf_metadata.py - HDF5 metadata reader
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

import pytest

# Check if h5py is available
try:
    import h5py
    HAS_H5PY = True
except ImportError:
    HAS_H5PY = False


class TestHdfReaderImports:
    """Tests for HdfReader imports."""

    def test_import_from_hdf5(self):
        """Test import from iwfm.hdf5."""
        from iwfm.hdf5 import HdfReader
        assert HdfReader is not None

    def test_import_open_hdf(self):
        """Test import of open_hdf factory function."""
        from iwfm.hdf5 import open_hdf
        assert callable(open_hdf)

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.hdf5.hdf_metadata import HdfReader, open_hdf
        assert HdfReader is not None
        assert callable(open_hdf)

    def test_class_has_docstring(self):
        """Test that class has documentation."""
        from iwfm.hdf5.hdf_metadata import HdfReader

        assert HdfReader.__doc__ is not None
        assert 'HDF5' in HdfReader.__doc__

    def test_open_hdf_has_docstring(self):
        """Test that open_hdf has documentation."""
        from iwfm.hdf5.hdf_metadata import open_hdf

        assert open_hdf.__doc__ is not None
        assert 'HDF5' in open_hdf.__doc__


class TestHdfReaderSignature:
    """Tests for HdfReader method signatures."""

    def test_init_signature(self):
        """Test that HdfReader.__init__ has correct signature."""
        from iwfm.hdf5.hdf_metadata import HdfReader
        import inspect

        sig = inspect.signature(HdfReader.__init__)
        params = list(sig.parameters.keys())

        assert 'self' in params
        assert 'hdf5_file' in params
        assert 'verbose' in params

    def test_open_hdf_signature(self):
        """Test that open_hdf has correct signature."""
        from iwfm.hdf5.hdf_metadata import open_hdf
        import inspect

        sig = inspect.signature(open_hdf)
        params = list(sig.parameters.keys())

        assert 'hdf5_file' in params
        assert 'verbose' in params

    def test_default_verbose(self):
        """Test that verbose defaults to False."""
        from iwfm.hdf5.hdf_metadata import open_hdf
        import inspect

        sig = inspect.signature(open_hdf)
        assert sig.parameters['verbose'].default == False


class TestHdfReaderMethods:
    """Tests for HdfReader method existence."""

    def test_has_get_n_nodes(self):
        """Test that HdfReader has get_n_nodes method."""
        from iwfm.hdf5.hdf_metadata import HdfReader
        assert hasattr(HdfReader, 'get_n_nodes')
        assert callable(getattr(HdfReader, 'get_n_nodes'))

    def test_has_get_n_elements(self):
        """Test that HdfReader has get_n_elements method."""
        from iwfm.hdf5.hdf_metadata import HdfReader
        assert hasattr(HdfReader, 'get_n_elements')
        assert callable(getattr(HdfReader, 'get_n_elements'))

    def test_has_get_n_layers(self):
        """Test that HdfReader has get_n_layers method."""
        from iwfm.hdf5.hdf_metadata import HdfReader
        assert hasattr(HdfReader, 'get_n_layers')
        assert callable(getattr(HdfReader, 'get_n_layers'))

    def test_has_get_n_timesteps(self):
        """Test that HdfReader has get_n_timesteps method."""
        from iwfm.hdf5.hdf_metadata import HdfReader
        assert hasattr(HdfReader, 'get_n_timesteps')
        assert callable(getattr(HdfReader, 'get_n_timesteps'))

    def test_has_get_timestep_info(self):
        """Test that HdfReader has get_timestep_info method."""
        from iwfm.hdf5.hdf_metadata import HdfReader
        assert hasattr(HdfReader, 'get_timestep_info')
        assert callable(getattr(HdfReader, 'get_timestep_info'))

    def test_has_get_metadata(self):
        """Test that HdfReader has get_metadata method."""
        from iwfm.hdf5.hdf_metadata import HdfReader
        assert hasattr(HdfReader, 'get_metadata')
        assert callable(getattr(HdfReader, 'get_metadata'))

    def test_has_close(self):
        """Test that HdfReader has close method."""
        from iwfm.hdf5.hdf_metadata import HdfReader
        assert hasattr(HdfReader, 'close')
        assert callable(getattr(HdfReader, 'close'))

    def test_has_context_manager(self):
        """Test that HdfReader supports context manager."""
        from iwfm.hdf5.hdf_metadata import HdfReader
        assert hasattr(HdfReader, '__enter__')
        assert hasattr(HdfReader, '__exit__')


@pytest.fixture
def mock_hdf5_file(tmp_path):
    """Create a mock HDF5 file with IWFM-like metadata."""
    if not HAS_H5PY:
        pytest.skip("h5py not installed")

    test_file = tmp_path / "test_budget.hdf"
    with h5py.File(test_file, 'w') as f:
        # Create Attributes group with IWFM metadata
        attrs_group = f.create_group('Attributes')
        attrs_group.attrs['SystemData%NNodes'] = 1234
        attrs_group.attrs['SystemData%NElements'] = 5678
        attrs_group.attrs['SystemData%NLayers'] = 3
        attrs_group.attrs['NTimeSteps'] = 120
        attrs_group.attrs['TimeStep%BeginDateAndTime'] = b'10/31/1973_24:00'
        attrs_group.attrs['TimeStep%DeltaT'] = 1.0
        attrs_group.attrs['TimeStep%Unit'] = b'1MON'

    return str(test_file)


@pytest.fixture
def mock_hdf5_file_minimal(tmp_path):
    """Create a minimal HDF5 file with only some metadata."""
    if not HAS_H5PY:
        pytest.skip("h5py not installed")

    test_file = tmp_path / "test_minimal.hdf"
    with h5py.File(test_file, 'w') as f:
        attrs_group = f.create_group('Attributes')
        attrs_group.attrs['SystemData%NNodes'] = 100
        attrs_group.attrs['nLocations'] = 200  # Fallback for elements
        attrs_group.attrs['NTimeSteps'] = 12
        attrs_group.attrs['TimeStep%BeginDateAndTime'] = b'01/01/2000_24:00'
        attrs_group.attrs['TimeStep%DeltaT'] = 1.0
        attrs_group.attrs['TimeStep%Unit'] = b'1DAY'

    return str(test_file)


@pytest.mark.skipif(not HAS_H5PY, reason="h5py not installed")
class TestHdfReaderFunctionality:
    """Tests for HdfReader functionality with mock HDF5 files."""

    def test_open_hdf_returns_reader(self, mock_hdf5_file):
        """Test that open_hdf returns HdfReader instance."""
        from iwfm.hdf5.hdf_metadata import HdfReader, open_hdf

        reader = open_hdf(mock_hdf5_file)
        try:
            assert isinstance(reader, HdfReader)
        finally:
            reader.close()

    def test_context_manager(self, mock_hdf5_file):
        """Test context manager usage."""
        from iwfm.hdf5.hdf_metadata import open_hdf

        with open_hdf(mock_hdf5_file) as reader:
            assert reader is not None
            n_nodes = reader.get_n_nodes()
            assert n_nodes == 1234

    def test_get_n_nodes(self, mock_hdf5_file):
        """Test get_n_nodes method."""
        from iwfm.hdf5.hdf_metadata import open_hdf

        with open_hdf(mock_hdf5_file) as reader:
            n_nodes = reader.get_n_nodes()
            assert n_nodes == 1234
            assert isinstance(n_nodes, int)

    def test_get_n_elements(self, mock_hdf5_file):
        """Test get_n_elements method."""
        from iwfm.hdf5.hdf_metadata import open_hdf

        with open_hdf(mock_hdf5_file) as reader:
            n_elements = reader.get_n_elements()
            assert n_elements == 5678
            assert isinstance(n_elements, int)

    def test_get_n_elements_fallback(self, mock_hdf5_file_minimal):
        """Test get_n_elements falls back to nLocations."""
        from iwfm.hdf5.hdf_metadata import open_hdf

        with open_hdf(mock_hdf5_file_minimal) as reader:
            n_elements = reader.get_n_elements()
            assert n_elements == 200

    def test_get_n_layers(self, mock_hdf5_file):
        """Test get_n_layers method."""
        from iwfm.hdf5.hdf_metadata import open_hdf

        with open_hdf(mock_hdf5_file) as reader:
            n_layers = reader.get_n_layers()
            assert n_layers == 3
            assert isinstance(n_layers, int)

    def test_get_n_layers_default(self, mock_hdf5_file_minimal):
        """Test get_n_layers defaults to 1 when not available."""
        from iwfm.hdf5.hdf_metadata import open_hdf

        with open_hdf(mock_hdf5_file_minimal) as reader:
            n_layers = reader.get_n_layers()
            assert n_layers == 1

    def test_get_n_timesteps(self, mock_hdf5_file):
        """Test get_n_timesteps method."""
        from iwfm.hdf5.hdf_metadata import open_hdf

        with open_hdf(mock_hdf5_file) as reader:
            n_timesteps = reader.get_n_timesteps()
            assert n_timesteps == 120
            assert isinstance(n_timesteps, int)

    def test_get_timestep_info(self, mock_hdf5_file):
        """Test get_timestep_info method."""
        from iwfm.hdf5.hdf_metadata import open_hdf

        with open_hdf(mock_hdf5_file) as reader:
            start_date, delta, unit = reader.get_timestep_info()
            assert start_date == '10/31/1973_24:00'
            assert delta == 1.0
            assert unit == '1MON'

    def test_get_metadata(self, mock_hdf5_file):
        """Test get_metadata method."""
        from iwfm.hdf5.hdf_metadata import open_hdf
        from iwfm.hdf5.hdf_metadata_base import HdfMetadata

        with open_hdf(mock_hdf5_file) as reader:
            metadata = reader.get_metadata()
            assert isinstance(metadata, HdfMetadata)
            assert metadata.n_nodes == 1234
            assert metadata.n_elements == 5678
            assert metadata.n_layers == 3
            assert metadata.n_timesteps == 120
            assert metadata.start_date == '10/31/1973_24:00'
            assert metadata.timestep_delta == 1.0
            assert metadata.timestep_unit == '1MON'

    def test_metadata_caching(self, mock_hdf5_file):
        """Test that metadata is cached after first read."""
        from iwfm.hdf5.hdf_metadata import open_hdf

        with open_hdf(mock_hdf5_file) as reader:
            metadata1 = reader.get_metadata()
            metadata2 = reader.get_metadata()
            # Should be the same object (cached)
            assert metadata1 is metadata2

    def test_verbose_output(self, mock_hdf5_file, capsys):
        """Test that verbose mode prints messages."""
        from iwfm.hdf5.hdf_metadata import open_hdf

        with open_hdf(mock_hdf5_file, verbose=True) as reader:
            reader.get_n_nodes(verbose=True)

        captured = capsys.readouterr()
        assert 'nodes' in captured.out.lower() or 'Opening' in captured.out

    def test_optional_methods_return_none(self, mock_hdf5_file):
        """Test that optional methods return None for HDF5 reader."""
        from iwfm.hdf5.hdf_metadata import open_hdf

        with open_hdf(mock_hdf5_file) as reader:
            assert reader.get_node_ids() is None
            assert reader.get_element_ids() is None
            assert reader.get_node_coords() is None
            assert reader.get_element_nodes() is None


@pytest.mark.skipif(not HAS_H5PY, reason="h5py not installed")
class TestHdfReaderErrors:
    """Tests for HdfReader error handling."""

    def test_file_not_found(self):
        """Test error when file doesn't exist."""
        from iwfm.hdf5.hdf_metadata import open_hdf

        with pytest.raises(FileNotFoundError):
            open_hdf('nonexistent_file.hdf')

    def test_missing_attributes_group(self, tmp_path):
        """Test error when Attributes group is missing."""
        from iwfm.hdf5.hdf_metadata import open_hdf
        from iwfm.hdf5.hdf_exceptions import DataSourceError

        # Create HDF5 file without Attributes group
        test_file = tmp_path / "no_attrs.hdf"
        with h5py.File(test_file, 'w') as f:
            f.create_dataset('data', data=[1, 2, 3])

        with pytest.raises(DataSourceError):
            with open_hdf(str(test_file)) as reader:
                reader.get_n_nodes()

    def test_missing_required_attribute(self, tmp_path):
        """Test error when required attribute is missing."""
        from iwfm.hdf5.hdf_metadata import open_hdf
        from iwfm.hdf5.hdf_exceptions import DataSourceError

        # Create HDF5 file with empty Attributes group
        test_file = tmp_path / "empty_attrs.hdf"
        with h5py.File(test_file, 'w') as f:
            f.create_group('Attributes')

        with pytest.raises(DataSourceError):
            with open_hdf(str(test_file)) as reader:
                reader.get_n_nodes()


class TestHdfReaderWithoutH5py:
    """Tests for HdfReader behavior when h5py is not available."""

    def test_backend_not_available_error_exists(self):
        """Test that BackendNotAvailableError is defined."""
        from iwfm.hdf5.hdf_exceptions import BackendNotAvailableError
        assert BackendNotAvailableError is not None

    def test_imports_succeed_without_h5py(self):
        """Test that module imports work even if h5py fails at runtime."""
        # This tests that the module handles ImportError gracefully
        from iwfm.hdf5 import HdfReader, open_hdf
        assert HdfReader is not None
        assert open_hdf is not None


class TestBackwardCompatibility:
    """Tests for backward compatibility with iwfm.model."""

    def test_deprecated_model_aliases(self):
        """Test that iwfm.model aliases point to correct classes."""
        import warnings
        # Suppress warnings since we just want to test the aliases work
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            from iwfm.model import Model, open_model, ModelMetadata

        # Check aliases work
        from iwfm.hdf5 import HdfReader, open_hdf, HdfMetadata
        assert Model is HdfReader
        assert open_model is open_hdf
        assert ModelMetadata is HdfMetadata

    def test_model_module_issues_deprecation_warning(self):
        """Test that importing iwfm.model issues deprecation warning."""
        import sys
        import warnings

        # Remove iwfm.model from cache to force re-import
        modules_to_remove = [k for k in sys.modules if k.startswith('iwfm.model')]
        for mod in modules_to_remove:
            del sys.modules[mod]

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            # Force fresh import
            import importlib
            import iwfm.model
            importlib.reload(iwfm.model)

            # Check deprecation warning was raised
            deprecation_warnings = [
                warning for warning in w
                if issubclass(warning.category, DeprecationWarning)
                and 'iwfm.model' in str(warning.message)
            ]
            assert len(deprecation_warnings) >= 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
