# Tokenized Strategy Mix for Yearn V3 strategies

This repo will allow you to write, test and deploy V3 "Tokenized Strategies".

You will only need to override the three functions in Strategy.sol of '_invest', 'freeFunds' and '_totalInvested'. With the option to also override '_tend' and 'tendTrigger' if needed.

## How to start

### Clone the repo

    git clone https://github.com/Schlagonia/tokenized-strategy-ape-mix

    cd tokenized-strategy-ape-mix

### Set up your virtual enviorment

    python3 -m venv venv

    source venv/bin/acitvate

### Install Ape and all dependencies

    pip install -r requirements.txt
    
    yarn
    
    ape plugins install .
    
    ape compile
    
    ape test
    
### Set your enviorment Variables

    export WEB3_INFURA_PROJECT_ID=your_infura_api_key

    export ETHERSCAN_API_KEY=your_api_key

See the ApeWorx [documentation](https://docs.apeworx.io/ape/stable/) and [github](https://github.com/ApeWorX/ape) for more information.