import pytest


def assert_strategy_reported(log, strategy, gain, loss, performance_fee, protocol_fee):
    assert log.strategy == strategy
    assert log.gain == gain
    assert log.loss == loss
    assert log.performance_fee == performance_fee
    assert log.protocol_fee == protocol_fee
