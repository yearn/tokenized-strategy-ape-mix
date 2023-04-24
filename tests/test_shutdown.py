import ape
from ape import Contract, reverts
from utils.checks import check_strategy_totals, check_strategy_mins
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

    check_strategy_totals(
        strategy, total_assets=amount, total_debt=0, total_idle=amount
    )

    chain.mine(14)

    # Need to shutdown the strategy, withdraw and then report the updated balances
    strategy.shutdownStrategy(sender=management)

    check_strategy_mins(
        strategy, min_total_assets=amount, min_total_debt=0, min_total_idle=amount
    )

    # withdrawal
    strategy.redeem(amount, user, user, sender=user)

    check_strategy_totals(strategy, total_assets=0, total_debt=0, total_idle=0)

    assert (
        pytest.approx(asset.balanceOf(user), rel=RELATIVE_APPROX) == user_balance_before
    )


# TODO: Add tests for any emergency function added.
