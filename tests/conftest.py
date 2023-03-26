import pytest
from ape import Contract, project


@pytest.fixture(scope="session")
def daddy(accounts):
    yield accounts["0xFEB4acf3df3cDEA7399794D0869ef76A6EfAff52"]


@pytest.fixture(scope="session")
def user(accounts):
    yield accounts[0]


@pytest.fixture(scope="session")
def rewards(accounts):
    yield accounts[1]


@pytest.fixture(scope="session")
def management(accounts):
    yield accounts[2]


@pytest.fixture(scope="session")
def keeper(accounts):
    yield accounts[3]


@pytest.fixture(scope="session")
def tokens():
    tokens = {
        "weth": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "dai": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
        "usdc": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
    }
    yield tokens


@pytest.fixture(scope="session")
def asset(tokens):
    yield Contract(tokens["dai"])


@pytest.fixture(scope="session")
def whale(accounts):
    # In order to get some funds for the token you are about to use,
    # The Balancer vault stays steady ballin on almost all tokens
    # NOTE: If `asset` is a balancer pool this may cause issues on amount checks.
    yield accounts["0xBA12222222228d8Ba445958a75a0704d566BF2C8"]


@pytest.fixture(scope="session")
def amount(asset, user, whale):
    amount = 100 * 10 ** asset.decimals()

    asset.transfer(user, amount, sender=whale)
    yield amount


@pytest.fixture(scope="session")
def weth(tokens):
    yield Contract(tokens["weth"])


@pytest.fixture(scope="session")
def weth_amount(user, weth):
    weth_amount = 10 ** weth.decimals()
    user.transfer(weth, weth_amount)
    yield weth_amount


# TODO: How to test on chains no library hasn't been deployed to?
"""
@pytest.fixture(scope="session")
def library(daddy):
    lib = daddy.deploy(project.dependencies["BaseStrategy"]["master"]['BaseLibrary.sol'])
    print(lib.address)
    return lib
"""


@pytest.fixture(scope="session")
def create_strategy(management, keeper, asset):
    def create_strategy(asset, performanceFee=0):
        strategy = management.deploy(project.Strategy, asset)
        strategy = project.IStrategy.at(strategy.address)

        strategy.setKeeper(keeper, sender=management)
        strategy.setPerformanceFee(performanceFee, sender=management)

        return strategy

    yield create_strategy


@pytest.fixture(scope="session")
def strategy(asset, create_strategy):
    strategy = create_strategy(asset)
    
    yield strategy


############ HELPER FUNCTIONS ############


@pytest.fixture(scope="session")
def deposit(strategy, asset, user, amount):
    def deposit(assets=amount, account=user):
        asset.approve(strategy, assets, sender=account)
        strategy.deposit(assets, account, sender=account)

    yield deposit


@pytest.fixture(scope="session")
def RELATIVE_APPROX():
    yield 1e-5
