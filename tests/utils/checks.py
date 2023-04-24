import pytest


def assert_strategy_reported(log, strategy, gain, loss, performance_fee, protocol_fee):
    assert log.strategy == strategy
    assert log.gain == gain
    assert log.loss == loss
    assert log.performance_fee == performance_fee
    assert log.protocol_fee == protocol_fee


def check_strategy_totals(strategy, total_assets, total_debt, total_idle):
    assert pytest.approx(strategy.totalAssets(), abs=2) == total_assets
    assert pytest.approx(strategy.totalDebt(), abs=2) == total_debt
    assert pytest.approx(strategy.totalIdle(), abs=2) == total_idle


def check_strategy_mins(strategy, min_total_assets, min_total_debt, min_total_idle):
    assert strategy.totalAssets() >= min_total_assets
    assert strategy.totalDebt() >= min_total_debt
    assert strategy.totalIdle() >= min_total_idle
