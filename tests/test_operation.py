import ape
from ape import Contract
from utils.checks import check_strategy_totals
import pytest


def test_operation(
    chain,
    asset,
    strategy,
    user,
    deposit,
    amount,
    RELATIVE_APPROX,
    keeper,
):
    user_balance_before = asset.balanceOf(user)

    # Deposit to the strategy
    deposit()

    check_strategy_totals(
        strategy,
        total_assets=amount,
        total_debt=0,
        total_idle=amount,
        total_supply=amount,
    )

    chain.mine(1)

    # withdrawal
    strategy.withdraw(amount, user, user, sender=user)

    check_strategy_totals(
        strategy, total_assets=0, total_debt=0, total_idle=0, total_supply=0
    )

    assert (
        pytest.approx(asset.balanceOf(user), rel=RELATIVE_APPROX) == user_balance_before
    )


def test_profitable_report(
    chain,
    accounts,
    asset,
    strategy,
    deposit,
    user,
    management,
    amount,
    whale,
    RELATIVE_APPROX,
    keeper,
):
    # Deposit to the strategy
    user_balance_before = asset.balanceOf(user)

    # Deposit to the strategy
    deposit()

    check_strategy_totals(
        strategy,
        total_assets=amount,
        total_debt=0,
        total_idle=amount,
        total_supply=amount,
    )

    # TODO: Add some code before harvest #2 to simulate earning yield
    profit = amount // 100
    asset.transfer(strategy, address, profit, sender=whale)

    # Harvest 2: Realize profit
    chain.mine(1)
    before_pps = strategy.pricePerShare()

    strategy.report(sender=keeper)

    check_strategy_totals(
        strategy,
        total_assets=amount + profit,
        total_debt=0,
        total_idle=amount + profit,
        total_supply=amount + profit,
    )

    # needed for profits to unlock
    chain.pending_timestamp = (
        chain.pending_timestamp + strategy.maxProfitUnlockTime() - 1
    )
    chain.mine(timestamp=chain.pending_timestamp)

    check_strategy_totals(
        strategy,
        total_assets=amount + profit,
        total_debt=0,
        total_idle=amount + profit,
        total_supply=amount,
    )
    assert strategy.pricePerShare() > before_pps


def test_triggers(
    chain,
    daddy,
    strategy,
    asset,
    amount,
    deposit,
    user,
    weth,
    weth_amount,
    management,
    keeper,
):
    # Deposit to the strategy
    deposit()

    check_strategy_totals(
        strategy,
        total_assets=amount,
        total_debt=0,
        total_idle=amount,
        total_supply=amount,
    )

    assert strategy.tendTrigger(0) == False
