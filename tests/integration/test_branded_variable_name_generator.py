"""
Tests of our generation of branded variable names
"""

# Tests to write:
# - Given a CMIP6 variable name and cell methods, do we get expected output
# - Match the behaviour specified in the excel table
# - Given a branded variable, get back to CMIP6 variable and cell methods
# - Round tripping
# - If you give an uncreognised name, you get a sensible error

from contextlib import nullcontext as does_not_raise

import pytest


@pytest.mark.parametrize(
    ["variable", "cell_methods", "exp", "expectation"],
    (
        pytest.param(
            "tas", "time: mean area: mean", "tas-tavg-hx-u-u", id="tas-average"
        ),
        ("hfds", "time: mean area: sum", "hfds-tavg-hx-s-u"),
        ("junk", "time: mean area: sum", "hfds-tavg-hx-s-u"),
    ),
)
def test_basic(variable, cell_methods, exp):
    res = get_branded_variable(variable=variable, cell_methods=cell_methods)

    assert res == exp


@pytest.mark.parametrize(
    ["variable", "expectation"],
    (
        pytest.param("tas", does_not_raise()),
        pytest.param(
            "junk", pytest.raises(KeyError, match="some helpful error message here")
        ),
    ),
)
def test_unrecognised_variable_raises(variable, expectation):
    with expectation:
        get_branded_variable(variable=variable, cell_methods="not used")
