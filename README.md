# Tokenized Strategy Mix for Yearn V3 strategies

This repo will allow you to write, test and deploy V3 "Tokenized Strategies" using [Ape Worx](https://www.apeworx.io/).

You will only need to override the three functions in Strategy.sol of `_deployFunds`, `_freeFunds` and `_harvestAndReport`. With the option to also override `_tend`, `_tendTrigger`, `availableDepositLimit`, `availableWithdrawLimit` and `_emergencyWithdraw` if desired.

For a more complete overview of how the Tokenized Strategies work please visit the [TokenizedStrategy Repo](https://github.com/yearn/tokenized-strategy).

## How to start

### Requirements
    Python >=3.8.0, <=3.10
    Yarn
    Node.js >=14
    Hardhat

### Fork this repository

    git clone https://github.com/user/tokenized-strategy-ape-mix

    cd tokenized-strategy-ape-mix

### Set up your virtual environment

    python3 -m venv venv

    source venv/bin/activate

Tip: You can make them persistent by adding the variables in ~/.env (ENVVAR=... format), then adding the following in .bashrc: `set -a; source "$HOME/.env"; set +a`

### Install Ape and all dependencies

    pip install -r requirements.txt
    
    yarn
    
    ape plugins install .
    
    ape compile
    
    ape test
    
### Set your environment Variables

    export WEB3_INFURA_PROJECT_ID=your_infura_api_key

    export ETHERSCAN_API_KEY=your_api_key

Tip: You can make them persistent by adding the variables in ~/.env (ENVVAR=... format), then adding the following in .bashrc: `set -a; source "$HOME/.env"; set +a`

## Strategy Writing

For a complete guide to creating a Tokenized Strategy please visit: https://docs.yearn.fi/developers/v3/strategy_writing_guide

See the ApeWorx [documentation](https://docs.apeworx.io/ape/stable/) and [github](https://github.com/ApeWorX/ape) for more information.
