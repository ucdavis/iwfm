import pytest
from iwfm.bnds2mask import bnds2mask

def test_bnds2mask():
    """Test the bnds2mask function."""
    # Example input data for the test
    example_bnds = [
        [0, 0],
        [0, 1],
        [1, 1],
        [1, 0]
    ]
    expected_output = "Expected output based on the function's logic"

    # Call the function with the example input
    result = bnds2mask(example_bnds)

    # Assert the result matches the expected output
    assert result == expected_output, f"Expected {expected_output}, but got {result}"