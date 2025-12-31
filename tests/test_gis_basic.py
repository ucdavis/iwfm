# test_gis_basic.py
# unit test for basic methods in iwfm.gis in the iwfm package
# Copyright (C) 2025 University of California
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
import math
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path


def _load_fn(module_name, file_name, fn_name):
    base = Path(__file__).resolve().parents[1] / "iwfm" / "gis" / file_name
    spec = spec_from_file_location(module_name, str(base))
    mod = module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return getattr(mod, fn_name)


bearing = _load_fn("bearing", "bearing.py", "bearing")
dms2dd = _load_fn("dms2dd", "dms2dd.py", "dms2dd")
dd2dms = _load_fn("dd2dms", "dd2dms.py", "dd2dms")
distance_sphere = _load_fn("distance_sphere", "distance_sphere.py", "distance_sphere")
is_northern = _load_fn("is_northern", "is_northern.py", "is_northern")
point_in_poly = _load_fn("point_in_poly", "point_in_poly.py", "point_in_poly")


def test_bearing_cardinal_directions():
    assert math.isclose(bearing([0.0, 0.0], [1.0, 0.0]), 0.0, abs_tol=1e-9)
    assert math.isclose(bearing([0.0, 0.0], [0.0, 1.0]), 90.0, abs_tol=1e-9)
    assert math.isclose(bearing([0.0, 0.0], [-1.0, 0.0]), 180.0, abs_tol=1e-9)
    assert math.isclose(bearing([0.0, 0.0], [0.0, -1.0]), 270.0, abs_tol=1e-9)


def test_dms2dd_known_values():
    lat_dd, lon_dd = dms2dd("34°3'30\"N", "118°15'0\"W")
    assert math.isclose(lat_dd, 34 + 3/60 + 30/3600, rel_tol=1e-9)
    assert math.isclose(lon_dd, -(118 + 15/60 + 0/3600), rel_tol=1e-9)


def test_dd2dms_then_dms2dd_roundtrip():
    lat, lon = 38.575, -121.478
    dms = dd2dms(lat, lon)
    lat_str, lon_str = dms.split(", ")
    # dms2dd accepts various separators via regex
    lat_dd, lon_dd = dms2dd(lat_str.replace("º", "°"), lon_str.replace("º", "°"))
    assert math.isclose(lat_dd, lat, rel_tol=1e-6)
    assert math.isclose(lon_dd, lon, rel_tol=1e-6)


def test_distance_sphere_units():
    # 1 degree of longitude at equator ~ 111.195 km
    d_km = distance_sphere([0.0, 0.0], [0.0, 1.0], units='km')
    assert math.isclose(d_km, 111.195, rel_tol=5e-3)
    d_mi = distance_sphere([0.0, 0.0], [0.0, 1.0], units='mi')
    assert math.isclose(d_mi, 69.0, rel_tol=1e-2)
    d_ft = distance_sphere([0.0, 0.0], [0.0, 1.0], units='ft')
    assert math.isclose(d_ft, 364000.0, rel_tol=2e-2)


def test_is_northern():
    assert is_northern(0.0) is True
    assert is_northern(45.0) is True
    assert is_northern(-0.0001) is False


def test_point_in_poly_inside_edge_outside():
    square = [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (0.0, 10.0)]
    assert point_in_poly(5.0, 5.0, square) is True  # inside
    assert point_in_poly(5.0, 0.0, square) is True  # on horizontal edge
    assert point_in_poly(15.0, 5.0, square) is False  # outside


