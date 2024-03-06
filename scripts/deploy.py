from ape import project, accounts, chain
import click

deployer = accounts.load("")


def deploy():
    print(f"You are using: 'deployer' [{deployer.address}]")
    print("Deploying a new strategy on ChainID", chain.chain_id)

    if input("Do you want to continue? [y/N]: ").lower() != "y":
        return

    publish_source = click.confirm("Verify source on etherscan?")

    # Address of the underlying asset to use
    asset = ""
    # Name for your strategy
    name = ""

    if input(f"Deploy strategy for {asset}, called {name}?  [y/N]: ").lower() != "y":
        return

    strategy = deployer.deploy(project.Strategy, asset, name, publish=publish_source)

    print(f"Deployed new strategy to: {strategy.address}")


def main():
    deploy()
