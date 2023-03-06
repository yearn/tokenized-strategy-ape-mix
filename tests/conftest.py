import pytest
from ape import Contract, project


@pytest.fixture
def gov(accounts):
    yield accounts["0xFEB4acf3df3cDEA7399794D0869ef76A6EfAff52"]


@pytest.fixture
def user(accounts):
    yield accounts[0]


@pytest.fixture
def rewards(accounts):
    yield accounts[1]


@pytest.fixture
def guardian(accounts):
    yield accounts[2]


@pytest.fixture
def management(accounts):
    yield accounts[3]


@pytest.fixture
def strategist(accounts):
    yield accounts[4]


@pytest.fixture
def keeper(accounts):
    yield accounts[5]


@pytest.fixture
def token(weth):
    yield weth
    # token_address = "0x6b175474e89094c44da98b954eedeac495271d0f"  # this should be the address of the ERC-20 used by the strategy/vault (DAI)
    # yield Contract(token_address)


@pytest.fixture
def whale(accounts):
    # In order to get some funds for the token you are about to use,
    # it impersonate an exchange address to use it's funds.
    yield accounts["0x030bA81f1c18d280636F32af80b9AAd02Cf0854e"]


@pytest.fixture
def amount(token, user, whale):
    amount = 100 * 10 ** token.decimals()

    token.transfer(user, amount, sender=whale)
    yield amount


@pytest.fixture
def weth():
    token_address = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    yield Contract(token_address)


@pytest.fixture
def weth_amount(user, weth):
    weth_amount = 10 ** weth.decimals()
    user.transfer(weth, weth_amount)
    yield weth_amount

@pytest.fixture
def vault(gov, rewards, guardian, management, token):
    vault = guardian.deploy(project.dependencies["yearnV2"]["0.4.6"].Vault)
    vault.initialize(token, gov, rewards, "", "", guardian, management, sender=gov)
    vault.setDepositLimit(2**256 - 1, sender=gov)
    vault.setManagement(management, sender=gov)
    yield vault


@pytest.fixture
def strategy(strategist, keeper, vault, gov, token):
    strategy = strategist.deploy(project.Strategy, token, vault)
    strategy.setKeeper(keeper, sender=strategist)
    vault.addStrategy(strategy, 10_000, 0, 2**256 - 1, 0, sender=gov)
    yield strategy


@pytest.fixture(scope="session")
def RELATIVE_APPROX():
    yield 1e-5
