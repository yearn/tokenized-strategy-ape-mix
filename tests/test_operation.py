import ape
from ape import Contract
from utils.checks import check_strategy_totals
import pytest


def test_operation(
    chain,
    asset,
    library,
    strategy,
    user,
    deposit,
    amount,
    RELATIVE_APPROX,
    keeper,
):
    user_balance_before = asset.balanceOf(user)

    # Deposit to the strategy
    print("Depositing!!")
    deposit()
    print(f"Deposited {user_balance_before - asset.balanceOf(user)}")
    print(f"Assets {strategy.totalAssets()}")

    check_strategy_totals(
        strategy,
        total_assets=amount,
        total_debt=0,
        total_idle=amount,
        total_supply=amount
    )

    chain.mine(1)

    # withdrawal
    strategy.withdraw(amount, user, user, sender=user)

    check_strategy_totals(
        strategy,
        total_assets=0,
        total_debt=0,
        total_idle=0,
        total_supply=0
    )

    assert (
        pytest.approx(asset.balanceOf(user), rel=RELATIVE_APPROX) == user_balance_before
    )

"""
def test_profitable_report(
    chain,
    accounts,
    asset,
    strategy,
    user,
    management,
    amount,
    whale,
    RELATIVE_APPROX,
    keeper,
):
    # Deposit to the strategy
    asset.approve(strategy.address, amount, sender=user)
    strategy.deposit(amount, sender=user)
    assert asset.balanceOf(strategy.address) == amount

    # Harvest 1: Send funds through the strategy
    chain.mine(1)
    strategy.harvest(sender=keeper)
    assert pytest.approx(strategy.estimatedTotalAssets(), rel=RELATIVE_APPROX) == amount

    # TODO: Add some code before harvest #2 to simulate earning yield
    asset.transfer(strategy, amount // 100, sender=whale)

    # Harvest 2: Realize profit
    chain.mine(1)
    before_pps = strategy.pricePerShare()
    strategy.harvest(sender=keeper)
    chain.mine(3600 * 6)  # 6 hrs needed for profits to unlock
    chain.mine(1)
    profit = asset.balanceOf(strategy.address)  # Profits go to strategy
    # TODO: Uncomment the lines below
    assert asset.balanceOf(strategy) + profit > amount
    assert strategy.pricePerShare() > before_pps


def test_change_debt(
    chain,
    daddy,
    asset,
    strategy,
    user,
    management,
    amount,
    RELATIVE_APPROX,
    keeper,
):
    # Deposit to the strategy and harvest
    asset.approve(strategy.address, amount, sender=user)
    strategy.deposit(amount, sender=user)
    strategy.updateStrategyDebtRatio(strategy.address, 5_000, sender=daddy)
    chain.mine(1)
    strategy.harvest(sender=keeper)
    half = int(amount / 2)

    assert pytest.approx(strategy.estimatedTotalAssets(), rel=RELATIVE_APPROX) == half

    strategy.updateStrategyDebtRatio(strategy.address, 10_000, sender=daddy)
    chain.mine(1)
    strategy.harvest(sender=keeper)
    assert pytest.approx(strategy.estimatedTotalAssets(), rel=RELATIVE_APPROX) == amount

    # In order to pass this tests, you will need to implement prepareReturn.
    # TODO: uncomment the following lines.
    strategy.updateStrategyDebtRatio(strategy.address, 5_000, sender=daddy)
    chain.mine(1)
    strategy.harvest(sender=keeper)
    assert pytest.approx(strategy.estimatedTotalAssets(), rel=RELATIVE_APPROX) == half


def test_triggers(
    chain,
    daddy,
    strategy,
    asset,
    amount,
    user,
    weth,
    weth_amount,
    management,
    keeper,
):
    # Deposit to the strategy and harvest
    asset.approve(strategy.address, amount, sender=user)
    strategy.deposit(amount, sender=user)
    strategy.updateStrategyDebtRatio(strategy.address, 5_000, sender=daddy)
    chain.mine(1)
    strategy.harvest(sender=keeper)

    strategy.harvestTrigger(0)
    strategy.tendTrigger(0)
"""