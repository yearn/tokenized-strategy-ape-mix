import pytest


def assert_strategy_reported(log, gain, loss, performance_fee, protocol_fee):
    assert log.strategy == strategy_address
    assert log.gain == gain
    assert log.loss == loss
    assert log.performance_fee == performance_fee
    assert log.protocol_fee == protocol_fee


def check_strategy_totals(strategy, total_assets, total_debt, total_idle):
    assert pytest.approx(strategy.totalAssets(), abs=1) == total_assets
    assert strategy.totalDebt() == total_debt
    assert pytest.approx(strategy.totalIdle(), abs=1) == total_idle


def check_strategy_totals(strategy, total_assets, total_debt, total_idle, total_supply):
    assert pytest.approx(strategy.totalAssets(), abs=1) == total_assets
    assert strategy.totalDebt() == total_debt
    assert pytest.approx(strategy.totalIdle(), abs=1) == total_idle
    # will adjust the accuracy based on token decimals
    assert (
        pytest.approx(strategy.totalSupply(), rel=10 ** -(strategy.decimals() * 2 // 3))
        == total_supply
    )
