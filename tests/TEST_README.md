# IWFM Package Unit Test Scripts fo Unix/Linux

This directory contains unix/linux shell scripts for running unit tests for the iwfm package.

## Test Scripts

### `run_tests.sh` - Comprehensive Test Runner

A full-featured test runner with detailed logging and reporting capabilities.

**Features:**
- Colored output for better readability
- Detailed logging to timestamped files
- Individual test file breakdown
- Coverage reporting (if coverage package installed)
- Error extraction and separate error log
- Summary statistics and reports

**Usage:**
```bash
# Run all tests with full logging
./run_tests.sh

# Clean previous logs and run tests
./run_tests.sh --clean

# Install test dependencies
./run_tests.sh --install-deps

# Get help
./run_tests.sh --help
```

**Environment Variables:**
```bash
# Pass additional arguments to pytest
PYTEST_ARGS='-x' ./run_tests.sh  # Stop on first failure
PYTEST_ARGS='-v -s' ./run_tests.sh  # Verbose with output
```

### `run_tests_simple.sh` - Simple Test Runner

A lightweight script for quick test runs with basic logging.

**Features:**
- Quick execution
- Simple timestamped log output
- Individual test file summary
- Basic pass/fail reporting

**Usage:**
```bash
# Run all tests with simple logging
./run_tests_simple.sh
```

## Log Files

Both scripts generate log files in the following locations:

### Comprehensive Script (`run_tests.sh`)
- `test_logs/test_run_YYYYMMDD_HHMMSS.log` - Main detailed log
- `test_logs/test_summary_YYYYMMDD_HHMMSS.log` - Summary report
- `test_logs/test_errors_YYYYMMDD_HHMMSS.log` - Error-only log
- `test_logs/htmlcov/` - HTML coverage report (if coverage installed)

### Simple Script (`run_tests_simple.sh`)
- `test_results_YYYYMMDD_HHMMSS.log` - Combined output log

## Test Coverage Summary

The current test suite includes:

### Test Files Created
1. **`test_math_utils.py`** - Mathematical utility functions
   - `logtrans()`, `round()`, `column_sum()`
2. **`test_text_processing.py`** - Text manipulation functions
   - `skip_ahead()`, `pad_front()`, `pad_back()`, `pad_both()`, `print_to_string()`
3. **`test_dictionary_utils.py`** - Dictionary utility functions
   - `inverse_dict()`, `list2dict()`, `file2dict()`, `hyd_dict()`
4. **`test_finite_element.py`** - Finite element methods
   - `get_elem_centroids()`, `elem_poly_coords()`, `nearest()`
5. **`test_additional_datetime.py`** - Additional date/time functions
   - `secs_between()` and edge cases for existing date functions
6. **`test_budget_functions.py`** - Budget processing functions
   - `budget_info()`, existence checks for `bud2csv()` and `buds2xl()`

### Existing Test Files
- `test_distance.py` - Distance calculations
- `test_cfs2afd.py` - Unit conversions
- `test_date2text.py`, `test_month_day.py`, etc. - Date/time functions
- `test_file_ops.py` - File operations
- `test_gis_basic.py` - GIS utility functions
- And many more...

## Current Test Results

As of the latest run:
- **Total tests**: 183
- **Passed**: 157 (85.8%)
- **Failed**: 13 (7.1%)
- **Skipped**: 13 (7.1%)

### Known Issues
Some tests fail due to:
1. Missing dependencies (`requests`, `xlsxwriter`, etc.)
2. Platform-specific functionality (Excel COM on Windows)
3. Minor bugs in source code (missing imports, edge cases)
4. Test setup issues (temporary file creation)

## Requirements

### Python Environment
The scripts expect a Python virtual environment at `.venv/` with the following packages:
- `pytest` (automatically installed if missing)
- `coverage` (optional, for coverage reports)
- `shapely`, `pandas`, `numpy` (for iwfm package functionality)

### Setting Up Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\\Scripts\\activate  # Windows

# Install dependencies
pip install pytest coverage shapely pandas numpy

# Or use the install script
./run_tests.sh --install-deps
```

## Continuous Integration

These scripts are designed to work in CI/CD environments:

### Exit Codes
- `0` - All tests passed
- `1` - Some tests failed
- Other codes - Script errors

### Sample CI Usage
```yaml
# Example GitHub Actions step
- name: Run Tests
  run: |
    cd iwfm
    ./run_tests.sh
  continue-on-error: false
```

## Development Workflow

1. **Development**: Make changes to iwfm package
2. **Quick Test**: Run `./run_tests_simple.sh` for fast feedback
3. **Full Test**: Run `./run_tests.sh` for comprehensive testing
4. **Review**: Check log files for detailed results
5. **Fix**: Address any failing tests
6. **Commit**: Commit changes with confidence

## Adding New Tests

To add new tests:
1. Create test file in `tests/` directory following `test_*.py` naming
2. Use pytest conventions and existing test files as examples
3. Run test scripts to verify new tests work
4. Update this README if adding new test categories

## Troubleshooting

### Common Issues
1. **"No module named pytest"**: Run `./run_tests.sh --install-deps`
2. **Permission denied**: Run `chmod +x run_tests*.sh`
3. **Python not found**: Check virtual environment setup
4. **Import errors**: Install missing dependencies

### Debug Mode
For debugging test failures:
```bash
# Run with verbose output and stop on first failure
PYTEST_ARGS='-v -s -x' ./run_tests.sh

# Run specific test file
.venv/bin/python -m pytest tests/test_specific.py -v
```

## Contributing

When contributing new tests:
1. Follow existing test patterns and naming conventions
2. Include both positive and negative test cases
3. Test edge cases and error conditions
4. Update documentation as needed
5. Ensure tests pass before submitting pull requests