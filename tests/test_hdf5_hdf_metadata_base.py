# test_hdf5_hdf_metadata_base.py
# Tests for hdf5/hdf_metadata_base.py - Base classes and data structures
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
from abc import ABC


class TestHdfMetadataImports:
    """Tests for HdfMetadata imports."""

    def test_import_from_hdf5(self):
        """Test import from iwfm.hdf5."""
        from iwfm.hdf5 import HdfMetadata
        assert HdfMetadata is not None

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.hdf5.hdf_metadata_base import HdfMetadata
        assert HdfMetadata is not None

    def test_class_has_docstring(self):
        """Test that class has documentation."""
        from iwfm.hdf5.hdf_metadata_base import HdfMetadata

        assert HdfMetadata.__doc__ is not None
        assert 'metadata' in HdfMetadata.__doc__.lower()


class TestHdfMetadataDataclass:
    """Tests for HdfMetadata dataclass."""

    def test_is_dataclass(self):
        """Test that HdfMetadata is a dataclass."""
        from iwfm.hdf5.hdf_metadata_base import HdfMetadata
        from dataclasses import is_dataclass

        assert is_dataclass(HdfMetadata)

    def test_required_fields(self):
        """Test that HdfMetadata has required fields."""
        from iwfm.hdf5.hdf_metadata_base import HdfMetadata
        import dataclasses

        fields = {f.name for f in dataclasses.fields(HdfMetadata)}

        assert 'n_nodes' in fields
        assert 'n_elements' in fields
        assert 'n_layers' in fields
        assert 'n_timesteps' in fields
        assert 'start_date' in fields
        assert 'timestep_unit' in fields
        assert 'timestep_delta' in fields

    def test_optional_fields(self):
        """Test that HdfMetadata has optional fields."""
        from iwfm.hdf5.hdf_metadata_base import HdfMetadata
        import dataclasses

        fields = {f.name for f in dataclasses.fields(HdfMetadata)}

        assert 'node_ids' in fields
        assert 'element_ids' in fields
        assert 'node_coords' in fields

    def test_create_instance_required_only(self):
        """Test creating HdfMetadata with only required fields."""
        from iwfm.hdf5.hdf_metadata_base import HdfMetadata

        metadata = HdfMetadata(
            n_nodes=100,
            n_elements=200,
            n_layers=3,
            n_timesteps=120,
            start_date='10/31/1973_24:00',
            timestep_unit='1MON',
            timestep_delta=1.0
        )

        assert metadata.n_nodes == 100
        assert metadata.n_elements == 200
        assert metadata.n_layers == 3
        assert metadata.n_timesteps == 120
        assert metadata.start_date == '10/31/1973_24:00'
        assert metadata.timestep_unit == '1MON'
        assert metadata.timestep_delta == 1.0

    def test_optional_fields_default_none(self):
        """Test that optional fields default to None."""
        from iwfm.hdf5.hdf_metadata_base import HdfMetadata

        metadata = HdfMetadata(
            n_nodes=100,
            n_elements=200,
            n_layers=3,
            n_timesteps=120,
            start_date='10/31/1973_24:00',
            timestep_unit='1MON',
            timestep_delta=1.0
        )

        assert metadata.node_ids is None
        assert metadata.element_ids is None
        assert metadata.node_coords is None

    def test_create_instance_all_fields(self):
        """Test creating HdfMetadata with all fields."""
        from iwfm.hdf5.hdf_metadata_base import HdfMetadata

        metadata = HdfMetadata(
            n_nodes=100,
            n_elements=200,
            n_layers=3,
            n_timesteps=120,
            start_date='10/31/1973_24:00',
            timestep_unit='1MON',
            timestep_delta=1.0,
            node_ids=[1, 2, 3],
            element_ids=[1, 2],
            node_coords=[(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)]
        )

        assert metadata.node_ids == [1, 2, 3]
        assert metadata.element_ids == [1, 2]
        assert metadata.node_coords == [(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)]

    def test_field_types(self):
        """Test that fields have correct type annotations."""
        from iwfm.hdf5.hdf_metadata_base import HdfMetadata
        import dataclasses

        fields = {f.name: f.type for f in dataclasses.fields(HdfMetadata)}

        assert fields['n_nodes'] == int
        assert fields['n_elements'] == int
        assert fields['n_layers'] == int
        assert fields['n_timesteps'] == int
        assert fields['start_date'] == str
        assert fields['timestep_unit'] == str
        assert fields['timestep_delta'] == float


class TestHdfBackendImports:
    """Tests for HdfBackend imports."""

    def test_import_from_hdf5(self):
        """Test import from iwfm.hdf5."""
        from iwfm.hdf5 import HdfBackend
        assert HdfBackend is not None

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.hdf5.hdf_metadata_base import HdfBackend
        assert HdfBackend is not None

    def test_class_has_docstring(self):
        """Test that class has documentation."""
        from iwfm.hdf5.hdf_metadata_base import HdfBackend

        assert HdfBackend.__doc__ is not None


class TestHdfBackendAbstract:
    """Tests for HdfBackend abstract base class."""

    def test_is_abstract(self):
        """Test that HdfBackend is an abstract class."""
        from iwfm.hdf5.hdf_metadata_base import HdfBackend

        assert issubclass(HdfBackend, ABC)

    def test_cannot_instantiate_directly(self):
        """Test that HdfBackend cannot be instantiated directly."""
        from iwfm.hdf5.hdf_metadata_base import HdfBackend

        with pytest.raises(TypeError):
            HdfBackend()

    def test_abstract_methods(self):
        """Test that HdfBackend defines abstract methods."""
        from iwfm.hdf5.hdf_metadata_base import HdfBackend

        # Check that these methods are abstract
        abstract_methods = {
            'get_n_nodes',
            'get_n_elements',
            'get_n_layers',
            'get_n_timesteps',
            'get_timestep_info',
            'get_metadata',
            'close'
        }

        for method_name in abstract_methods:
            assert hasattr(HdfBackend, method_name), f"Missing method: {method_name}"

    def test_optional_methods_have_default(self):
        """Test that optional methods have default implementations."""
        from iwfm.hdf5.hdf_metadata_base import HdfBackend

        # These methods should have default implementations returning None
        optional_methods = [
            'get_node_ids',
            'get_element_ids',
            'get_node_coords',
            'get_element_nodes'
        ]

        for method_name in optional_methods:
            method = getattr(HdfBackend, method_name)
            assert method is not None, f"Missing optional method: {method_name}"


class TestHdfBackendConcreteImplementation:
    """Tests for creating concrete implementations of HdfBackend."""

    def test_can_create_subclass(self):
        """Test that a concrete subclass can be created."""
        from iwfm.hdf5.hdf_metadata_base import HdfBackend, HdfMetadata

        class TestBackend(HdfBackend):
            def get_n_nodes(self, verbose=False):
                return 100

            def get_n_elements(self, verbose=False):
                return 200

            def get_n_layers(self, verbose=False):
                return 3

            def get_n_timesteps(self, verbose=False):
                return 120

            def get_timestep_info(self, verbose=False):
                return ('10/31/1973_24:00', 1.0, '1MON')

            def get_metadata(self, verbose=False):
                return HdfMetadata(
                    n_nodes=100,
                    n_elements=200,
                    n_layers=3,
                    n_timesteps=120,
                    start_date='10/31/1973_24:00',
                    timestep_unit='1MON',
                    timestep_delta=1.0
                )

            def close(self):
                pass

        backend = TestBackend()
        assert backend.get_n_nodes() == 100
        assert backend.get_n_elements() == 200

    def test_optional_methods_return_none_by_default(self):
        """Test that optional methods return None in base class."""
        from iwfm.hdf5.hdf_metadata_base import HdfBackend, HdfMetadata

        class MinimalBackend(HdfBackend):
            def get_n_nodes(self, verbose=False):
                return 100

            def get_n_elements(self, verbose=False):
                return 200

            def get_n_layers(self, verbose=False):
                return 3

            def get_n_timesteps(self, verbose=False):
                return 120

            def get_timestep_info(self, verbose=False):
                return ('10/31/1973_24:00', 1.0, '1MON')

            def get_metadata(self, verbose=False):
                return HdfMetadata(
                    n_nodes=100,
                    n_elements=200,
                    n_layers=3,
                    n_timesteps=120,
                    start_date='10/31/1973_24:00',
                    timestep_unit='1MON',
                    timestep_delta=1.0
                )

            def close(self):
                pass

        backend = MinimalBackend()

        # Optional methods should return None by default
        assert backend.get_node_ids() is None
        assert backend.get_element_ids() is None
        assert backend.get_node_coords() is None
        assert backend.get_element_nodes() is None

    def test_missing_abstract_method_raises_error(self):
        """Test that missing abstract method raises TypeError."""
        from iwfm.hdf5.hdf_metadata_base import HdfBackend

        class IncompleteBackend(HdfBackend):
            def get_n_nodes(self, verbose=False):
                return 100
            # Missing other required methods

        with pytest.raises(TypeError):
            IncompleteBackend()


class TestHdfReaderInheritsFromBackend:
    """Tests to verify HdfReader inherits from HdfBackend."""

    def test_hdf_reader_is_subclass(self):
        """Test that HdfReader is a subclass of HdfBackend."""
        from iwfm.hdf5.hdf_metadata import HdfReader
        from iwfm.hdf5.hdf_metadata_base import HdfBackend

        assert issubclass(HdfReader, HdfBackend)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
