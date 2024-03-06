import ape
from ape import Contract

# This test should not be overridden and checks that
# no function signature collisions occurred from the custom functions.
# Does not check functions that are strategy dependant and will be checked in other tests
def test_function_collisions(strategy, asset, management, rewards, user, keeper):
    wad = int(1e18)

    with ape.reverts("initialized"):
        strategy.initialize(
            asset, "name", management, rewards, keeper, sender=management
        )

    # Check view functions
    assert strategy.convertToAssets(wad) == wad
    assert strategy.convertToShares(wad) == wad
    assert strategy.previewDeposit(wad) == wad
    assert strategy.previewMint(wad) == wad
    assert strategy.previewWithdraw(wad) == wad
    assert strategy.previewRedeem(wad) == wad
    assert strategy.totalAssets() == 0
    assert strategy.totalSupply() == 0
    assert strategy.unlockedShares() == 0
    assert strategy.asset() == asset
    assert strategy.apiVersion() == "3.0.2"
    assert strategy.MAX_FEE() == 5_000
    assert strategy.fullProfitUnlockDate() == 0
    assert strategy.profitUnlockingRate() == 0
    assert strategy.lastReport() > 0
    assert strategy.pricePerShare() == 10 ** asset.decimals()
    assert not strategy.isShutdown()
    assert strategy.symbol() == f"ys{asset.symbol()}"
    assert strategy.decimals() == asset.decimals()

    # Assure modifiers are working
    with ape.reverts("!management"):
        strategy.setPendingManagement(user, sender=user)
    with ape.reverts("!pending"):
        strategy.acceptManagement(sender=user)
    with ape.reverts("!management"):
        strategy.setKeeper(user, sender=user)
    with ape.reverts("!management"):
        strategy.setEmergencyAdmin(user, sender=user)
    with ape.reverts("!management"):
        strategy.setPerformanceFee(int(2_000), sender=user)
    with ape.reverts("!management"):
        strategy.setPerformanceFeeRecipient(user, sender=user)
    with ape.reverts("!management"):
        strategy.setProfitMaxUnlockTime(1, sender=user)

    # Assure checks are being used
    with ape.reverts("Cannot be self"):
        strategy.setPerformanceFeeRecipient(strategy.address, sender=management)
    with ape.reverts("too long"):
        strategy.setProfitMaxUnlockTime(int(2**256 - 1), sender=management)

    assert strategy.balanceOf(user) == 0
    assert strategy.allowance(keeper, user) == 0
    assert strategy.approve(user, wad, sender=keeper)
    assert strategy.allowance(keeper, user) == wad
