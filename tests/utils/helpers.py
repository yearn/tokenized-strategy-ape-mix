import ape
import pytest


def days_to_secs(days: int) -> int:
    return 60 * 60 * 24 * days


def increase_time(chain, seconds):
    chain.pending_timestamp = chain.pending_timestamp + seconds
    chain.mine(timestamp=chain.pending_timestamp)


def get_strategy_totals(strategy):
    assets = strategy.totalAssets()
    supply = strategy.totalSupply()

    return (assets, supply)


def deposit(strategy, asset, amount, user):
    asset.approve(strategy.address, amount, sender=user)

    strategy.deposit(amount, user, sender=user)


def report(strategy):
    keeper = strategy.keeper()

    tx = strategy.report(sender=keeper)

    gain, loss = tx.return_value

    return (gain, loss)


def withdraw_and_check(strategy, asset, amount, user):
    balance_before = asset.balanceOf(user)

    strategy.withdraw(amount, user, user, sender=user)

    assert asset.balanceOf(user) - balance_before == amount


def check_normal_flow(chain, strategy, asset, amount, user):
    # Deposit into the strategy
    deposit(strategy, asset, amount, user)

    assert pytest.approx(strategy.totalAssets(), abs=2) == amount

    increase_time(chain, 15)

    report(strategy)

    # Increase time to unlock yield
    increase_time(chain, days_to_secs(strategy.profitMaxUnlockTime() - 1))

    # Withdraw
    withdraw_and_check(strategy, asset, amount, user)

    assert strategy.totalAssets() == 0
