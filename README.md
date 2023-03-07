# V2 Base Strategy Adapter

This repo is to allow you to write a strategy for YearnV3 that will work with a Yearn V2 vault.

All adaptations are already implemented in BaseStrategyAdapter.sol.

You will only need to override the three functions in Strategy.sol of '_invest', 'freeFunds' and '_invested'. With the option to also override '_tend' and 'tendTrigger' if needed.

## How to start

### Clone the repo

    git clone https://github.com/Schlagonia/V2-Base-Strategy-Adapter

    cd V2-Base-Strategy-Adapter

### Set up your virtual enviorment

    python3 -m venv venv

    source venv/bin/acitvate

### Install Ape and all dependencies

    pip install -r requirements-dev.txt
    
    yarn
    
    ape plugins install .
    
    ape compile
    
    ape test
    
### Set your enviorment Variables

    export WEB3_INFURA_PROJECT_ID=yourInfuraApiKey

See the ApeWorx [documentation](https://docs.apeworx.io/ape/stable/) and [github](https://github.com/ApeWorX/ape) for more information.