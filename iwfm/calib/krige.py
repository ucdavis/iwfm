# krige.py 
# Perform spatial interpolation from grid A to grid B using kriging factors.
# Copyright (C) 2020-2023 University of California
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

def krige(A, B):
    """ krige() - Perform spatial interpolation using kriging factors from grid A to grid B.

    Parameters
    ----------
    A : list
        List of tuples representing grid A points. Each tuple contains (id, x, y) coordinates.
    
    B : list
        List of tuples representing grid B points. Each tuple contains (id, x, y, value) coordinates.
    
    Returns
    -------
    kriging_factors : list
        List of lists containing kriging factor floats for spatial interpolation.
    """
    import numpy as np
    from scipy.spatial.distance import cdist

    kriging_factors = []

    for a_id, ax, ay in A:
        # Calculate the distances from each point in B to all points in A
        distances = cdist([(ax, ay)], [(bx, by) for _, bx, by, _ in B])
        
        # Compute kriging factors (inverse distance weights) for each point in A
        weights = 1 / distances
        
        # Normalize the weights to sum up to 1
        normalized_weights = weights / np.sum(weights)
        
        # Append the kriging factors for the current point in B to the list
        kriging_factors.append(normalized_weights.tolist()[0])
    print(len(kriging_factors))
    return kriging_factors


# Sample data for grid A
new_points = [
    (1, 1.0, 2.0),
    (2, 2.0, 3.0),
    (3, 5.0, 4.0),
    (4, 6.0, 7.0),
    (5, 10.0, 4.0),
    (6, 6.0, 3.0),
    (7, 8.0, 1.0),
]

# Sample data for grid B
base_points = [
    (1, 2.0, 1.0, 80.0),
    (2, 3.0, 3.0, 120.0),
    (3, 4.0, 6.0, 85.0),
    (4, 5.0, 10.0, 40.0),
    (5, 7.0, 8.0, 50.0),
    (6, 8.0, 6.0, 55.0),
    (7, 10.0, 6.0, 80.0),
    (8, 7.0, 3.0, 50.0),
    (9, 5.0, 1.0, 120.0),
    (10, 9.0, 1.0, 55.0),
]


if __name__ == '__main__':

    # Perform kriging interpolation
    krige_factors = krige(new_points, base_points)
    print(krige_factors)
