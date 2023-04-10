import ape
from ape import Contract
from utils.constants import MAX_BPS
from utils.checks import check_strategy_totals
from utils.utils import days_to_secs, increase_time
import pytest


def test__operation(
    chain,
    asset,
    strategy,
    user,
    deposit,
    amount,
    RELATIVE_APPROX,
):
    user_balance_before = asset.balanceOf(user)

    # Deposit to the strategy
    deposit()

    # TODO: Implement logic so totalDebt ends > 0
    check_strategy_totals(
        strategy,
        total_assets=amount,
        total_debt=0,
        total_idle=amount,
        total_supply=amount,
    )

    chain.mine(10)

    # withdrawal
    strategy.withdraw(amount, user, user, sender=user)

    check_strategy_totals(
        strategy, total_assets=0, total_debt=0, total_idle=0, total_supply=0
    )

    assert asset.balanceOf(user) == user_balance_before


def test_profitable_report(
    chain,
    asset,
    strategy,
    deposit,
    user,
    amount,
    whale,
    RELATIVE_APPROX,
    keeper,
):
    # Deposit to the strategy
    user_balance_before = asset.balanceOf(user)

    # Deposit to the strategy
    deposit()

    # TODO: Implement logic so totalDebt ends > 0
    check_strategy_totals(
        strategy,
        total_assets=amount,
        total_debt=0,
        total_idle=amount,
        total_supply=amount,
    )

    # TODO: Add some code to simulate earning yield
    to_airdrop = amount // 100

    asset.transfer(strategy.address, to_airdrop, sender=whale)

    # Harvest 2: Realize profit
    chain.mine(10)

    before_pps = strategy.pricePerShare()

    tx = strategy.report(sender=keeper)

    profit, loss = tx.return_value

    assert profit >= to_airdrop

    # TODO: Implement logic so totalDebt == amount + profit
    check_strategy_totals(
        strategy,
        total_assets=amount + profit,
        total_debt=0,
        total_idle=amount + profit,
        total_supply=amount + profit,
    )

    # needed for profits to unlock
    increase_time(chain, strategy.profitMaxUnlockTime() - 1)

    check_strategy_totals(
        strategy,
        total_assets=amount + profit,
        total_debt=0,
        total_idle=amount + profit,
        total_supply=amount,
    )
    assert strategy.pricePerShare() > before_pps

    # withdrawal
    strategy.redeem(amount, user, user, sender=user)

    check_strategy_totals(
        strategy, total_assets=0, total_debt=0, total_idle=0, total_supply=0
    )

    assert asset.balanceOf(user) == user_balance_before + profit


def test__profitable_report__with_fee(
    chain,
    asset,
    strategy,
    deposit,
    user,
    management,
    rewards,
    amount,
    whale,
    RELATIVE_APPROX,
    keeper,
):
    # Set performance fee to 10%
    performance_fee = int(1_000)
    strategy.setPerformanceFee(performance_fee, sender=management)

    # Deposit to the strategy
    user_balance_before = asset.balanceOf(user)

    # Deposit to the strategy
    deposit()

    # TODO: Implement logic so totalDebt ends > 0
    check_strategy_totals(
        strategy,
        total_assets=amount,
        total_debt=0,
        total_idle=amount,
        total_supply=amount,
    )

    # TODO: Add some code to simulate earning yield
    to_airdrop = amount // 100

    asset.transfer(strategy.address, to_airdrop, sender=whale)

    chain.mine(10)

    before_pps = strategy.pricePerShare()

    tx = strategy.report(sender=keeper)

    profit, loss = tx.return_value

    assert profit > 0

    expected_performance_fee = profit * performance_fee // MAX_BPS

    # TODO: Implement logic so totalDebt == amount + profit
    check_strategy_totals(
        strategy,
        total_assets=amount + profit,
        total_debt=0,
        total_idle=amount + profit,
        total_supply=amount + profit,
    )

    # needed for profits to unlock
    increase_time(chain, strategy.profitMaxUnlockTime() - 1)

    check_strategy_totals(
        strategy,
        total_assets=amount + profit,
        total_debt=0,
        total_idle=amount + profit,
        total_supply=amount + expected_performance_fee,
    )

    assert strategy.pricePerShare() > before_pps

    tx = strategy.redeem(amount, user, user, sender=user)

    assert asset.balanceOf(user) > user_balance_before

    rewards_balance_before = asset.balanceOf(rewards)

    strategy.redeem(expected_performance_fee, rewards, rewards, sender=rewards)

    check_strategy_totals(
        strategy,
        total_assets=0,
        total_debt=0,
        total_idle=0,
        total_supply=0,
    )

    assert asset.balanceOf(rewards) >= rewards_balance_before + expected_performance_fee


def test__tend_trigger(
    chain,
    strategy,
    asset,
    amount,
    deposit,
    keeper,
    user,
):
    # Check Trigger
    assert strategy.tendTrigger() == False

    # Deposit to the strategy
    deposit()

    # Check Trigger
    assert strategy.tendTrigger() == False

    chain.mine(days_to_secs(1))

    # Check Trigger
    assert strategy.tendTrigger() == False

    strategy.report(sender=keeper)

    # Check Trigger
    assert strategy.tendTrigger() == False

    # needed for profits to unlock
    increase_time(chain, strategy.profitMaxUnlockTime() - 1)

    # Check Trigger
    assert strategy.tendTrigger() == False

    strategy.redeem(amount, user, user, sender=user)

    # Check Trigger
    assert strategy.tendTrigger() == False
