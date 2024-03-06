import ape
from ape import Contract, reverts
from utils.helpers import days_to_secs
import pytest


def test__shutdown__can_withdraw(
    chain,
    asset,
    strategy,
    user,
    deposit,
    amount,
    management,
    RELATIVE_APPROX,
    keeper,
):
    user_balance_before = asset.balanceOf(user)

    # Deposit to the strategy
    deposit()

    assert strategy.totalAssets() == amount

    chain.mine(14)

    # Need to shutdown the strategy, withdraw and then report the updated balances
    strategy.shutdownStrategy(sender=management)

    assert strategy.totalAssets() >= amount

    # withdrawal
    strategy.redeem(amount, user, user, sender=user)

    assert strategy.totalAssets() == 0

    assert (
        pytest.approx(asset.balanceOf(user), rel=RELATIVE_APPROX) == user_balance_before
    )


# TODO: Add tests for any emergency function added.
