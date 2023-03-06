# TODO: Add tests that show proper migration of the strategy to a newer one
#       Use another copy of the strategy to simulate the migration
#       Show that nothing is lost!

import pytest
from ape import project


def test_migration(
    chain,
    token,
    vault,
    strategy,
    amount,
    strategist,
    keeper,
    gov,
    user,
    RELATIVE_APPROX,
):
    # Deposit to the vault and harvest
    token.approve(vault.address, amount, sender=user)
    vault.deposit(amount, sender=user)
    chain.mine(1)
    strategy.harvest(sender=keeper)

    assert pytest.approx(strategy.estimatedTotalAssets(), rel=RELATIVE_APPROX) == amount

    # migrate to a new strategy
    new_strategy = strategist.deploy(project.Strategy, token, vault)
    vault.migrateStrategy(strategy, new_strategy, sender=gov)
    assert (
        pytest.approx(new_strategy.estimatedTotalAssets(), rel=RELATIVE_APPROX)
        == amount
    )
