import ape
from ape import Contract, reverts, project
from utils.checks import check_strategy_totals
from utils.helpers import days_to_secs
import pytest


def check_oracle(oracle, asset, user, management):
    # Check set up
    # TODO: Add checks for the setup

    current_apr = oracle.aprAfterDebtChange(asset.address, 0)

    assert current_apr > 0
    # If APR is expected to be under 100%
    assert current_apr < int(1e18)

    # TODO: Uncomment if there are setter functions to test.
    """
    with reverts("Not today MoFo"):
        oracle.setterFunction(setterVariable, sender=user)
    
    oracle.setterFunction(setterVariable, sender=management)
    """


def test__oracle(create_oracle, asset, user, management):

    oracle = create_oracle()

    check_oracle(
        oracle,
        asset,
        user,
        management,
    )
