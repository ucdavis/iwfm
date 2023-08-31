from krige import krige
import numpy as np

def par2iwfm(A, B):
    """ par2iwfm() - Implement krige function to create new parameter values.

    Parameters
    ----------
    A : list
        List of tuples representing grid A points. Each tuple contains (id, x, y) coordinates.
    
    B : list
        List of tuples representing grid B points. Each tuple contains (id, x, y, value) coordinates.
    
    Returns
    -------
    a_values : list
        List of calculated floats representing values for A in B's grid
    """

    #  get krige factors and base set values
    krige_factors = krige(A, B)
    values = [val for _, _, _, val in B]
  
    #  convert to numpy arrays for computation
    first_array = np.array(values)
    second_array = np.array(krige_factors)
    
    #  Element-wise matrix multiplication
    a_value_array = first_array * second_array
    a_values = [np.sum(array) for array in a_value_array]

    return a_values

# Sample data for grid A
new_set = [
    (1, 1.0, 2.0),
    (2, 2.0, 3.0),
    (3, 5.0, 4.0),
    (4, 6.0, 7.0),
    (5, 10.0, 4.0),
    (6, 6.0, 3.0),
    (7, 8.0, 1.0),
    (8, 12.0, 12.0),
]

# Sample data for grid B
base_set = [
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

# Sample larger data for grid B
base_set_big = [
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
    (11, 1.0, 14.0, 70.0),
    (12, 4.0, 14.5, 70.0),
    (13, 8.0, 12.0, 75.0),
    (14, 10.0, 15.0, 65.0),
    (15, 14.0, 13.0, 63.0),
    (16, 16.0, 11.0, 57.0),
    (17, 14.0, 2.0, 75.0),
    (18, 16.0, 6.0, 62.0),
]


if __name__ == '__main__':

    a_values = par2iwfm(new_set, base_set)
    print(a_values)
