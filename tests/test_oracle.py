import ape
from ape import Contract, reverts, project
from utils.checks import check_strategy_totals
from utils.helpers import days_to_secs
import pytest


def check_oracle(oracle, strategy, user):
    # Check set up
    # TODO: Add checks for the setup

    current_apr = oracle.aprAfterDebtChange(strategy.address, 0)

    assert current_apr > 0
    # If APR is expected to be under 100%
    assert current_apr < int(1e18)

    # TODO: Uncomment if there are setter functions to test.
    """
    with reverts("Ownable: caller is not the owner"):
        oracle.setterFunction(setterVariable, sender=user)
    
    management = strategy.management()
    
    oracle.setterFunction(setterVariable, sender=management)
    """


def test__oracle(create_oracle, strategy, user):

    oracle = create_oracle()

    check_oracle(oracle, strategy, strategy)
