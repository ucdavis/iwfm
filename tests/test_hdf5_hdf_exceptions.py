# test_hdf5_hdf_exceptions.py
# Tests for hdf5/hdf_exceptions.py - Custom exceptions for HDF5 module
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


class TestHdfErrorImports:
    """Tests for HdfError imports."""

    def test_import_from_hdf5(self):
        """Test import from iwfm.hdf5."""
        from iwfm.hdf5 import HdfError
        assert HdfError is not None

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.hdf5.hdf_exceptions import HdfError
        assert HdfError is not None

    def test_is_exception(self):
        """Test that HdfError is an Exception subclass."""
        from iwfm.hdf5.hdf_exceptions import HdfError
        assert issubclass(HdfError, Exception)


class TestHdfErrorUsage:
    """Tests for HdfError usage."""

    def test_can_raise(self):
        """Test that HdfError can be raised."""
        from iwfm.hdf5.hdf_exceptions import HdfError

        with pytest.raises(HdfError):
            raise HdfError("Test error")

    def test_can_catch(self):
        """Test that HdfError can be caught."""
        from iwfm.hdf5.hdf_exceptions import HdfError

        try:
            raise HdfError("Test error")
        except HdfError as e:
            assert str(e) == "Test error"

    def test_can_catch_as_exception(self):
        """Test that HdfError can be caught as Exception."""
        from iwfm.hdf5.hdf_exceptions import HdfError

        try:
            raise HdfError("Test error")
        except Exception as e:
            assert isinstance(e, HdfError)

    def test_has_docstring(self):
        """Test that HdfError has a docstring."""
        from iwfm.hdf5.hdf_exceptions import HdfError
        assert HdfError.__doc__ is not None


class TestBackendNotAvailableErrorImports:
    """Tests for BackendNotAvailableError imports."""

    def test_import_from_hdf5(self):
        """Test import from iwfm.hdf5."""
        from iwfm.hdf5 import BackendNotAvailableError
        assert BackendNotAvailableError is not None

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.hdf5.hdf_exceptions import BackendNotAvailableError
        assert BackendNotAvailableError is not None

    def test_is_hdf_error_subclass(self):
        """Test that BackendNotAvailableError is an HdfError subclass."""
        from iwfm.hdf5.hdf_exceptions import HdfError, BackendNotAvailableError
        assert issubclass(BackendNotAvailableError, HdfError)

    def test_is_exception_subclass(self):
        """Test that BackendNotAvailableError is an Exception subclass."""
        from iwfm.hdf5.hdf_exceptions import BackendNotAvailableError
        assert issubclass(BackendNotAvailableError, Exception)


class TestBackendNotAvailableErrorUsage:
    """Tests for BackendNotAvailableError usage."""

    def test_can_raise(self):
        """Test that BackendNotAvailableError can be raised."""
        from iwfm.hdf5.hdf_exceptions import BackendNotAvailableError

        with pytest.raises(BackendNotAvailableError):
            raise BackendNotAvailableError("h5py not installed")

    def test_can_catch_as_hdf_error(self):
        """Test that BackendNotAvailableError can be caught as HdfError."""
        from iwfm.hdf5.hdf_exceptions import HdfError, BackendNotAvailableError

        try:
            raise BackendNotAvailableError("h5py not installed")
        except HdfError as e:
            assert isinstance(e, BackendNotAvailableError)

    def test_message(self):
        """Test that error message is preserved."""
        from iwfm.hdf5.hdf_exceptions import BackendNotAvailableError

        msg = "h5py backend requires h5py module. Install with: pip install h5py"
        try:
            raise BackendNotAvailableError(msg)
        except BackendNotAvailableError as e:
            assert str(e) == msg

    def test_has_docstring(self):
        """Test that BackendNotAvailableError has a docstring."""
        from iwfm.hdf5.hdf_exceptions import BackendNotAvailableError
        assert BackendNotAvailableError.__doc__ is not None


class TestDataSourceErrorImports:
    """Tests for DataSourceError imports."""

    def test_import_from_hdf5(self):
        """Test import from iwfm.hdf5."""
        from iwfm.hdf5 import DataSourceError
        assert DataSourceError is not None

    def test_import_directly(self):
        """Test direct module import."""
        from iwfm.hdf5.hdf_exceptions import DataSourceError
        assert DataSourceError is not None

    def test_is_hdf_error_subclass(self):
        """Test that DataSourceError is an HdfError subclass."""
        from iwfm.hdf5.hdf_exceptions import HdfError, DataSourceError
        assert issubclass(DataSourceError, HdfError)

    def test_is_exception_subclass(self):
        """Test that DataSourceError is an Exception subclass."""
        from iwfm.hdf5.hdf_exceptions import DataSourceError
        assert issubclass(DataSourceError, Exception)


class TestDataSourceErrorUsage:
    """Tests for DataSourceError usage."""

    def test_can_raise(self):
        """Test that DataSourceError can be raised."""
        from iwfm.hdf5.hdf_exceptions import DataSourceError

        with pytest.raises(DataSourceError):
            raise DataSourceError("Attribute not found")

    def test_can_catch_as_hdf_error(self):
        """Test that DataSourceError can be caught as HdfError."""
        from iwfm.hdf5.hdf_exceptions import HdfError, DataSourceError

        try:
            raise DataSourceError("Attribute not found")
        except HdfError as e:
            assert isinstance(e, DataSourceError)

    def test_message(self):
        """Test that error message is preserved."""
        from iwfm.hdf5.hdf_exceptions import DataSourceError

        msg = "Required attribute 'NNodes' not found in HDF5 file"
        try:
            raise DataSourceError(msg)
        except DataSourceError as e:
            assert str(e) == msg

    def test_has_docstring(self):
        """Test that DataSourceError has a docstring."""
        from iwfm.hdf5.hdf_exceptions import DataSourceError
        assert DataSourceError.__doc__ is not None


class TestExceptionHierarchy:
    """Tests for exception hierarchy."""

    def test_hierarchy(self):
        """Test the exception inheritance hierarchy."""
        from iwfm.hdf5.hdf_exceptions import (
            HdfError,
            BackendNotAvailableError,
            DataSourceError
        )

        # HdfError is the base
        assert issubclass(HdfError, Exception)

        # Both specific errors inherit from HdfError
        assert issubclass(BackendNotAvailableError, HdfError)
        assert issubclass(DataSourceError, HdfError)

        # They are not subclasses of each other
        assert not issubclass(BackendNotAvailableError, DataSourceError)
        assert not issubclass(DataSourceError, BackendNotAvailableError)

    def test_catch_all_with_base_error(self):
        """Test that catching HdfError catches all specific errors."""
        from iwfm.hdf5.hdf_exceptions import (
            HdfError,
            BackendNotAvailableError,
            DataSourceError
        )

        errors_caught = []

        for ErrorClass in [BackendNotAvailableError, DataSourceError]:
            try:
                raise ErrorClass("test")
            except HdfError as e:
                errors_caught.append(type(e).__name__)

        assert 'BackendNotAvailableError' in errors_caught
        assert 'DataSourceError' in errors_caught


class TestExceptionChaining:
    """Tests for exception chaining support."""

    def test_can_chain_from_keyerror(self):
        """Test that exceptions can be chained from KeyError."""
        from iwfm.hdf5.hdf_exceptions import DataSourceError

        try:
            try:
                raise KeyError('NNodes')
            except KeyError as e:
                raise DataSourceError("Attribute not found") from e
        except DataSourceError as e:
            assert e.__cause__ is not None
            assert isinstance(e.__cause__, KeyError)

    def test_can_chain_from_importerror(self):
        """Test that exceptions can be chained from ImportError."""
        from iwfm.hdf5.hdf_exceptions import BackendNotAvailableError

        try:
            try:
                raise ImportError("No module named 'h5py'")
            except ImportError as e:
                raise BackendNotAvailableError("h5py not available") from e
        except BackendNotAvailableError as e:
            assert e.__cause__ is not None
            assert isinstance(e.__cause__, ImportError)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
