# Tokenized Strategy Mix for Yearn V3 strategies

This repo will allow you to write, test and deploy V3 "Tokenized Strategies".

You will only need to override the three functions in Strategy.sol of '_invest', 'freeFunds' and '_totalInvested', with the option to override '_tend' and 'tendTrigger' if needed.

## How to start

### Requirements
    Python >=3.8.0, <=3.10.x
    Yarn
    Node.js >=14
    Hardhat

### Fork this repository

    git clone https://github.com/user/tokenized-strategy-ape-mix

    cd tokenized-strategy-ape-mix

### Set up your virtual environment

    python3 -m venv venv

    source venv/bin/activate

### Install Ape and all dependencies

    pip install -r requirements.txt
    
    yarn
    
    ape plugins install .
    
    ape compile
    
    ape test
    
### Set your environment Variables

    export WEB3_INFURA_PROJECT_ID=your_infura_api_key

    export ETHERSCAN_API_KEY=your_api_key

You can make them persistent by adding the variables in ~/.env (ENVVAR=... format), then adding the following in .bashrc: `set -a; source "$HOME/.env"; set +a`

### Strategy Writing

#### Periphery Helpers

See the ApeWorx [documentation](https://docs.apeworx.io/ape/stable/) and [github](https://github.com/ApeWorX/ape) for more information.
