import ape
from ape import Contract
from utils.constants import MAX_BPS
from utils.helpers import days_to_secs, increase_time, withdraw_and_check
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

    assert strategy.totalAssets() == amount

    increase_time(chain, 10)

    # withdrawal
    withdraw_and_check(strategy, asset, amount, user)

    assert strategy.totalAssets() == 0

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

    assert strategy.totalAssets() == amount

    # TODO: Add some code to simulate earning yield
    to_airdrop = amount // 100

    asset.transfer(strategy.address, to_airdrop, sender=whale)

    # Harvest 2: Realize profit
    chain.mine(10)

    before_pps = strategy.pricePerShare()

    tx = strategy.report(sender=keeper)

    profit, loss = tx.return_value

    assert profit >= to_airdrop

    assert strategy.totalAssets() == amount + profit

    # needed for profits to unlock
    increase_time(chain, strategy.profitMaxUnlockTime() - 1)

    assert strategy.totalAssets() == amount + profit

    assert strategy.pricePerShare() > before_pps

    # withdrawal
    strategy.redeem(amount, user, user, sender=user)

    assert asset.balanceOf(user) > user_balance_before


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
    factory,
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

    assert strategy.totalAssets() == amount

    # TODO: Add some code to simulate earning yield
    to_airdrop = amount // 100

    asset.transfer(strategy.address, to_airdrop, sender=whale)

    chain.mine(10)

    before_pps = strategy.pricePerShare()

    tx = strategy.report(sender=keeper)

    profit, loss = tx.return_value

    assert profit > 0

    (protocol_fee, protocol_fee_recipient) = factory.protocol_fee_config(
        sender=strategy.address
    )

    expected_performance_fee = (
        (profit * performance_fee // MAX_BPS) * (10_000 - protocol_fee) // MAX_BPS
    )

    assert strategy.totalAssets() == amount + profit

    # needed for profits to unlock
    increase_time(chain, strategy.profitMaxUnlockTime() - 1)

    assert strategy.totalAssets() == amount + profit

    assert strategy.pricePerShare() > before_pps

    tx = strategy.redeem(amount, user, user, sender=user)

    assert asset.balanceOf(user) > user_balance_before

    rewards_balance_before = asset.balanceOf(rewards)

    strategy.redeem(expected_performance_fee, rewards, rewards, sender=rewards)

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
    assert strategy.tendTrigger()[0] == False

    # Deposit to the strategy
    deposit()

    # Check Trigger
    assert strategy.tendTrigger()[0] == False

    chain.mine(days_to_secs(1))

    # Check Trigger
    assert strategy.tendTrigger()[0] == False

    strategy.report(sender=keeper)

    # Check Trigger
    assert strategy.tendTrigger()[0] == False

    # needed for profits to unlock
    increase_time(chain, strategy.profitMaxUnlockTime() - 1)

    # Check Trigger
    assert strategy.tendTrigger()[0] == False

    strategy.redeem(amount, user, user, sender=user)

    # Check Trigger
    assert strategy.tendTrigger()[0] == False
