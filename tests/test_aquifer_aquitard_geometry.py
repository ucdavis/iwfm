#!/usr/bin/env python
# test_aquifer_aquitard_geometry.py
# Unit tests for iwfm_aquifer_bottom, iwfm_aquifer_thickness, iwfm_aquifer_top,
# iwfm_aquitard_bottom, iwfm_aquitard_thickness, iwfm_aquitard_top
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
import copy


# ---------------------------------------------------------------------------
# Helper functions to build strat data
# ---------------------------------------------------------------------------
# iwfm_strat_arrays() mutates its input (via list.pop), so every test
# must pass a fresh deep copy.
#
# strat format: [[node_id, elevation, aqtard1, aqfer1, aqtard2, aqfer2, ...], ...]
# ---------------------------------------------------------------------------

def make_strat_1node_2layer():
    """Single node, 2 layers with non-zero aquitard thicknesses.

    Node 1: elev=100, Layer 1: aquitard=10 aquifer=30, Layer 2: aquitard=5 aquifer=20

    Expected geometry (from land surface down):
        Layer 0: aquitard_top=100, aquitard_bot=90, aquifer_top=90, aquifer_bot=60
        Layer 1: aquitard_top=60,  aquitard_bot=55, aquifer_top=55, aquifer_bot=35
    """
    return [[1, 100.0, 10.0, 30.0, 5.0, 20.0]]


def make_strat_1node_1layer():
    """Single node, 1 layer.

    Node 1: elev=200, Layer 1: aquitard=15 aquifer=85

    Expected geometry:
        Layer 0: aquitard_top=200, aquitard_bot=185, aquifer_top=185, aquifer_bot=100
    """
    return [[1, 200.0, 15.0, 85.0]]


def make_strat_zero_aquitard():
    """Zero aquitard thickness (common in practice).

    Node 1: elev=500, Layer 1: aquitard=0 aquifer=100, Layer 2: aquitard=0 aquifer=150

    Expected geometry:
        Layer 0: aquitard_top=500, aquitard_bot=500, aquifer_top=500, aquifer_bot=400
        Layer 1: aquitard_top=400, aquitard_bot=400, aquifer_top=400, aquifer_bot=250
    """
    return [[1, 500.0, 0.0, 100.0, 0.0, 150.0]]


def make_strat_multi_node():
    """3 nodes, 2 layers each.

    Node 1: elev=100, L1: aqtard=10 aqfer=30, L2: aqtard=5  aqfer=20
    Node 2: elev=150, L1: aqtard=0  aqfer=50, L2: aqtard=0  aqfer=40
    Node 3: elev=80,  L1: aqtard=5  aqfer=25, L2: aqtard=10 aqfer=15
    """
    return [
        [1, 100.0, 10.0, 30.0, 5.0, 20.0],
        [2, 150.0, 0.0, 50.0, 0.0, 40.0],
        [3, 80.0, 5.0, 25.0, 10.0, 15.0],
    ]


def make_strat_c2vsimcg():
    """First 3 nodes from C2VSimCG-2025 Stratigraphy.dat (4 layers, zero aquitards)."""
    return [
        [1, 576.95, 0.0, 113.69, 0.0, 106.37, 0.0, 152.80, 0.0, 50.0],
        [2, 683.75, 0.0, 176.92, 0.0, 119.59, 0.0, 116.60, 0.0, 50.0],
        [3, 712.80, 0.0, 190.84, 0.0, 121.52, 0.0, 101.99, 0.0, 50.0],
    ]


# ---------------------------------------------------------------------------
# Tests for iwfm_aquifer_top
# ---------------------------------------------------------------------------
class TestIwfmAquiferTop:
    """Tests for iwfm.iwfm_aquifer_top()"""

    def test_single_node_single_layer(self):
        """Aquifer top equals land surface minus aquitard thickness."""
        import iwfm
        result = iwfm.iwfm_aquifer_top(copy.deepcopy(make_strat_1node_1layer()))
        assert len(result) == 1
        assert result[0] == [185.0]

    def test_single_node_two_layers(self):
        """Aquifer top for each layer with non-zero aquitard."""
        import iwfm
        result = iwfm.iwfm_aquifer_top(copy.deepcopy(make_strat_1node_2layer()))
        assert result[0] == pytest.approx([90.0, 55.0])

    def test_zero_aquitard(self):
        """When aquitard is zero, aquifer top equals aquitard top."""
        import iwfm
        result = iwfm.iwfm_aquifer_top(copy.deepcopy(make_strat_zero_aquitard()))
        assert result[0] == pytest.approx([500.0, 400.0])

    def test_multiple_nodes(self):
        """Verify aquifer top for all nodes."""
        import iwfm
        result = iwfm.iwfm_aquifer_top(copy.deepcopy(make_strat_multi_node()))
        assert len(result) == 3
        assert result[0] == pytest.approx([90.0, 55.0])
        assert result[1] == pytest.approx([150.0, 100.0])
        assert result[2] == pytest.approx([75.0, 40.0])

    def test_c2vsimcg_data(self):
        """Verify with real C2VSimCG-2025 stratigraphy data."""
        import iwfm
        result = iwfm.iwfm_aquifer_top(copy.deepcopy(make_strat_c2vsimcg()))
        # Node 1: zero aquitards, so aquifer tops are cumulative from 576.95
        assert result[0] == pytest.approx([576.95, 463.26, 356.89, 204.09])

    def test_return_shape(self):
        """Result has one entry per node, each with one value per layer."""
        import iwfm
        strat = copy.deepcopy(make_strat_multi_node())
        result = iwfm.iwfm_aquifer_top(strat)
        assert len(result) == 3
        for node_vals in result:
            assert len(node_vals) == 2


# ---------------------------------------------------------------------------
# Tests for iwfm_aquifer_bottom
# ---------------------------------------------------------------------------
class TestIwfmAquiferBottom:
    """Tests for iwfm.iwfm_aquifer_bottom()"""

    def test_single_node_single_layer(self):
        """Aquifer bottom equals aquifer top minus aquifer thickness."""
        import iwfm
        result = iwfm.iwfm_aquifer_bottom(copy.deepcopy(make_strat_1node_1layer()))
        # 200 - 15 (aquitard) - 85 (aquifer) = 100
        assert result[0] == [100.0]

    def test_single_node_two_layers(self):
        """Aquifer bottom for each layer."""
        import iwfm
        result = iwfm.iwfm_aquifer_bottom(copy.deepcopy(make_strat_1node_2layer()))
        assert result[0] == pytest.approx([60.0, 35.0])

    def test_zero_aquitard(self):
        """Aquifer bottom with zero aquitard thickness."""
        import iwfm
        result = iwfm.iwfm_aquifer_bottom(copy.deepcopy(make_strat_zero_aquitard()))
        assert result[0] == pytest.approx([400.0, 250.0])

    def test_multiple_nodes(self):
        """Verify aquifer bottom for all nodes."""
        import iwfm
        result = iwfm.iwfm_aquifer_bottom(copy.deepcopy(make_strat_multi_node()))
        assert result[0] == pytest.approx([60.0, 35.0])
        assert result[1] == pytest.approx([100.0, 60.0])
        assert result[2] == pytest.approx([50.0, 25.0])

    def test_c2vsimcg_data(self):
        """Verify with real C2VSimCG-2025 stratigraphy data."""
        import iwfm
        result = iwfm.iwfm_aquifer_bottom(copy.deepcopy(make_strat_c2vsimcg()))
        assert result[0] == pytest.approx([463.26, 356.89, 204.09, 154.09])

    def test_bottom_below_top(self):
        """Aquifer bottom must always be below aquifer top."""
        import iwfm
        strat = copy.deepcopy(make_strat_multi_node())
        strat2 = copy.deepcopy(make_strat_multi_node())
        tops = iwfm.iwfm_aquifer_top(strat)
        bots = iwfm.iwfm_aquifer_bottom(strat2)
        for i in range(len(tops)):
            for j in range(len(tops[i])):
                assert bots[i][j] <= tops[i][j]


# ---------------------------------------------------------------------------
# Tests for iwfm_aquifer_thickness
# ---------------------------------------------------------------------------
class TestIwfmAquiferThickness:
    """Tests for iwfm.iwfm_aquifer_thickness()"""

    def test_single_node_single_layer(self):
        """Return aquifer thickness for single layer."""
        import iwfm
        result = iwfm.iwfm_aquifer_thickness(copy.deepcopy(make_strat_1node_1layer()))
        assert result[0] == [85.0]

    def test_single_node_two_layers(self):
        """Return aquifer thickness for each layer."""
        import iwfm
        result = iwfm.iwfm_aquifer_thickness(copy.deepcopy(make_strat_1node_2layer()))
        assert result[0] == pytest.approx([30.0, 20.0])

    def test_multiple_nodes(self):
        """Verify aquifer thicknesses for all nodes."""
        import iwfm
        result = iwfm.iwfm_aquifer_thickness(copy.deepcopy(make_strat_multi_node()))
        assert result[0] == pytest.approx([30.0, 20.0])
        assert result[1] == pytest.approx([50.0, 40.0])
        assert result[2] == pytest.approx([25.0, 15.0])

    def test_c2vsimcg_data(self):
        """Verify with real C2VSimCG-2025 stratigraphy data."""
        import iwfm
        result = iwfm.iwfm_aquifer_thickness(copy.deepcopy(make_strat_c2vsimcg()))
        assert result[0] == pytest.approx([113.69, 106.37, 152.80, 50.0])
        assert result[1] == pytest.approx([176.92, 119.59, 116.60, 50.0])

    def test_thickness_equals_top_minus_bottom(self):
        """Aquifer thickness should equal aquifer_top minus aquifer_bottom."""
        import iwfm
        strat1 = copy.deepcopy(make_strat_multi_node())
        strat2 = copy.deepcopy(make_strat_multi_node())
        strat3 = copy.deepcopy(make_strat_multi_node())
        tops = iwfm.iwfm_aquifer_top(strat1)
        bots = iwfm.iwfm_aquifer_bottom(strat2)
        thicks = iwfm.iwfm_aquifer_thickness(strat3)
        for i in range(len(tops)):
            for j in range(len(tops[i])):
                assert thicks[i][j] == pytest.approx(tops[i][j] - bots[i][j])


# ---------------------------------------------------------------------------
# Tests for iwfm_aquitard_top
# ---------------------------------------------------------------------------
class TestIwfmAquitardTop:
    """Tests for iwfm.iwfm_aquitard_top()"""

    def test_single_node_single_layer(self):
        """Aquitard top of first layer equals land surface elevation."""
        import iwfm
        result = iwfm.iwfm_aquitard_top(copy.deepcopy(make_strat_1node_1layer()))
        assert result[0] == [200.0]

    def test_single_node_two_layers(self):
        """Aquitard top for each layer."""
        import iwfm
        result = iwfm.iwfm_aquitard_top(copy.deepcopy(make_strat_1node_2layer()))
        # Layer 0: top = land surface = 100
        # Layer 1: top = bottom of aquifer above = 60
        assert result[0] == pytest.approx([100.0, 60.0])

    def test_zero_aquitard(self):
        """When aquitard thickness is zero, top equals bottom."""
        import iwfm
        strat = copy.deepcopy(make_strat_zero_aquitard())
        strat2 = copy.deepcopy(make_strat_zero_aquitard())
        tops = iwfm.iwfm_aquitard_top(strat)
        from iwfm.iwfm_aquitard_bottom import iwfm_aquitard_bottom
        bots = iwfm_aquitard_bottom(strat2)
        for j in range(len(tops[0])):
            assert tops[0][j] == pytest.approx(bots[0][j])

    def test_first_layer_equals_elevation(self):
        """Aquitard top of layer 0 always equals land surface elevation."""
        import iwfm
        result = iwfm.iwfm_aquitard_top(copy.deepcopy(make_strat_multi_node()))
        assert result[0][0] == pytest.approx(100.0)
        assert result[1][0] == pytest.approx(150.0)
        assert result[2][0] == pytest.approx(80.0)

    def test_c2vsimcg_data(self):
        """Verify with real C2VSimCG-2025 stratigraphy data."""
        import iwfm
        result = iwfm.iwfm_aquitard_top(copy.deepcopy(make_strat_c2vsimcg()))
        assert result[0] == pytest.approx([576.95, 463.26, 356.89, 204.09])


# ---------------------------------------------------------------------------
# Tests for iwfm_aquitard_bottom
# ---------------------------------------------------------------------------
class TestIwfmAquitardBottom:
    """Tests for iwfm.iwfm_aquitard_bottom()"""

    def test_single_node_single_layer(self):
        """Aquitard bottom equals land surface minus aquitard thickness."""
        import iwfm
        result = iwfm.iwfm_aquitard_bottom(copy.deepcopy(make_strat_1node_1layer()))
        # 200 - 15 = 185
        assert result[0] == [185.0]

    def test_single_node_two_layers(self):
        """Aquitard bottom for each layer."""
        import iwfm
        result = iwfm.iwfm_aquitard_bottom(copy.deepcopy(make_strat_1node_2layer()))
        assert result[0] == pytest.approx([90.0, 55.0])

    def test_zero_aquitard(self):
        """When aquitard thickness is zero, bottom equals top."""
        import iwfm
        result = iwfm.iwfm_aquitard_bottom(copy.deepcopy(make_strat_zero_aquitard()))
        # With zero aquitard, bottom = top = 500 for layer 0, 400 for layer 1
        assert result[0] == pytest.approx([500.0, 400.0])

    def test_multiple_nodes(self):
        """Verify aquitard bottom for all nodes."""
        import iwfm
        result = iwfm.iwfm_aquitard_bottom(copy.deepcopy(make_strat_multi_node()))
        assert result[0] == pytest.approx([90.0, 55.0])
        assert result[1] == pytest.approx([150.0, 100.0])
        assert result[2] == pytest.approx([75.0, 40.0])

    def test_aquitard_bottom_equals_aquifer_top(self):
        """Aquitard bottom must equal aquifer top (they share the boundary)."""
        import iwfm
        strat1 = copy.deepcopy(make_strat_multi_node())
        strat2 = copy.deepcopy(make_strat_multi_node())
        aqtard_bot = iwfm.iwfm_aquitard_bottom(strat1)
        aqfer_top = iwfm.iwfm_aquifer_top(strat2)
        for i in range(len(aqtard_bot)):
            assert aqtard_bot[i] == pytest.approx(aqfer_top[i])

    def test_c2vsimcg_data(self):
        """Verify with real C2VSimCG-2025 stratigraphy data."""
        import iwfm
        result = iwfm.iwfm_aquitard_bottom(copy.deepcopy(make_strat_c2vsimcg()))
        # Zero aquitards, so bottom = top for each layer
        assert result[0] == pytest.approx([576.95, 463.26, 356.89, 204.09])


# ---------------------------------------------------------------------------
# Tests for iwfm_aquitard_thickness
# ---------------------------------------------------------------------------
class TestIwfmAquitardThickness:
    """Tests for iwfm.iwfm_aquitard_thickness()"""

    def test_single_node_single_layer(self):
        """Return aquitard thickness for single layer."""
        import iwfm
        result = iwfm.iwfm_aquitard_thickness(copy.deepcopy(make_strat_1node_1layer()))
        assert result[0] == [15.0]

    def test_single_node_two_layers(self):
        """Return aquitard thickness for each layer."""
        import iwfm
        result = iwfm.iwfm_aquitard_thickness(copy.deepcopy(make_strat_1node_2layer()))
        assert result[0] == pytest.approx([10.0, 5.0])

    def test_zero_thickness(self):
        """Zero aquitard thickness is valid and common."""
        import iwfm
        result = iwfm.iwfm_aquitard_thickness(copy.deepcopy(make_strat_zero_aquitard()))
        assert result[0] == pytest.approx([0.0, 0.0])

    def test_multiple_nodes(self):
        """Verify aquitard thicknesses for all nodes."""
        import iwfm
        result = iwfm.iwfm_aquitard_thickness(copy.deepcopy(make_strat_multi_node()))
        assert result[0] == pytest.approx([10.0, 5.0])
        assert result[1] == pytest.approx([0.0, 0.0])
        assert result[2] == pytest.approx([5.0, 10.0])

    def test_thickness_equals_top_minus_bottom(self):
        """Aquitard thickness should equal aquitard_top minus aquitard_bottom."""
        import iwfm
        strat1 = copy.deepcopy(make_strat_multi_node())
        strat2 = copy.deepcopy(make_strat_multi_node())
        strat3 = copy.deepcopy(make_strat_multi_node())
        tops = iwfm.iwfm_aquitard_top(strat1)
        bots = iwfm.iwfm_aquitard_bottom(strat2)
        thicks = iwfm.iwfm_aquitard_thickness(strat3)
        for i in range(len(tops)):
            for j in range(len(tops[i])):
                assert thicks[i][j] == pytest.approx(tops[i][j] - bots[i][j])

    def test_c2vsimcg_data(self):
        """All C2VSimCG nodes have zero aquitard thickness."""
        import iwfm
        result = iwfm.iwfm_aquitard_thickness(copy.deepcopy(make_strat_c2vsimcg()))
        for node_vals in result:
            assert node_vals == pytest.approx([0.0, 0.0, 0.0, 0.0])


# ---------------------------------------------------------------------------
# Cross-function consistency tests
# ---------------------------------------------------------------------------
class TestGeometryConsistency:
    """Verify geometric relationships between all six functions."""

    def test_layer_stacking_order(self):
        """Elevation must decrease: aquitard_top >= aquitard_bot = aquifer_top >= aquifer_bot."""
        import iwfm
        for make_fn in [make_strat_1node_2layer, make_strat_multi_node, make_strat_c2vsimcg]:
            s1, s2, s3, s4 = [copy.deepcopy(make_fn()) for _ in range(4)]
            aqtard_top = iwfm.iwfm_aquitard_top(s1)
            aqtard_bot = iwfm.iwfm_aquitard_bottom(s2)
            aqfer_top = iwfm.iwfm_aquifer_top(s3)
            aqfer_bot = iwfm.iwfm_aquifer_bottom(s4)
            for i in range(len(aqtard_top)):
                for j in range(len(aqtard_top[i])):
                    assert aqtard_top[i][j] >= aqtard_bot[i][j]
                    assert aqtard_bot[i][j] == pytest.approx(aqfer_top[i][j])
                    assert aqfer_top[i][j] >= aqfer_bot[i][j]

    def test_layer_continuity(self):
        """Aquifer bottom of layer j must equal aquitard top of layer j+1."""
        import iwfm
        s1, s2 = copy.deepcopy(make_strat_multi_node()), copy.deepcopy(make_strat_multi_node())
        aqfer_bot = iwfm.iwfm_aquifer_bottom(s1)
        aqtard_top = iwfm.iwfm_aquitard_top(s2)
        for i in range(len(aqfer_bot)):
            nlayers = len(aqfer_bot[i])
            for j in range(nlayers - 1):
                assert aqfer_bot[i][j] == pytest.approx(aqtard_top[i][j + 1])

    def test_total_depth(self):
        """Sum of all thicknesses must equal land surface minus deepest aquifer bottom."""
        import iwfm
        strat_data = make_strat_1node_2layer()
        elev = strat_data[0][1]  # 100.0

        s1, s2 = copy.deepcopy(strat_data), copy.deepcopy(strat_data)
        aqtard_thick = iwfm.iwfm_aquitard_thickness(s1)
        aqfer_thick = iwfm.iwfm_aquifer_thickness(s2)

        total = sum(aqtard_thick[0]) + sum(aqfer_thick[0])
        # 10 + 30 + 5 + 20 = 65

        s3 = copy.deepcopy(make_strat_1node_2layer())
        aqfer_bot = iwfm.iwfm_aquifer_bottom(s3)
        deepest = aqfer_bot[0][-1]  # 35.0

        assert total == pytest.approx(elev - deepest)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
