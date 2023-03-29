# Tokenized Strategy Mix for Yearn V3 strategies

This repo will allow you to write, test and deploy V3 "Tokenized Strategies".

You will only need to override the three functions in Strategy.sol of '_invest', 'freeFunds' and '_totalInvested'. With the option to also override `_tend`, `tendTrigger`, `availableDepositLimit` and `availableWithdrawLimit` if desired.

## How to start

### Requirements
    Python >=3.8.0, <=3.10
    Yarn
    Node.js >=14
    Hardhat

### Fork this repository

    git clone https://github.com/user/tokenized-strategy-ape-mix

    cd tokenized-strategy-ape-mix

### Set up your virtual enviorment

    python3 -m venv venv

    source venv/bin/activate

### Install Ape and all dependencies

    pip install -r requirements.txt
    
    yarn
    
    ape plugins install .
    
    ape compile
    
    ape test
    
### Set your enviorment Variables

    export WEB3_INFURA_PROJECT_ID=your_infura_api_key

    export ETHERSCAN_API_KEY=your_api_key

## Strategy Writing

### Good to know

To create your own tokenized strategy you will need to override at least 3 functions outlined in `Strategy.sol`. An in depth description for each function is provide above each function in `Strategy.sol`.

It is important to remeber the defualt behavior for the any tokenized strategy is to be a permisionless vault, so functions such as _invest and _freeFunds can be called by anyone and care should be taken when implementing manipulatable logic such as swaps/lp movements. Strategists can choose to limit deposit/withdraws by overriding the `availableWithdrawLimit` and `availableDepositLimit` function if it is needed for safety.

It is recommended to build strategies on the assumption that reports will happen based on the strategies specific `profitMaxUnlockTime`. Since this is the only time _totalInvested will be called any strategies that need more frequent checks, updates should override then _tend and tendTrigger functions for any needed mid report maintanance.

The only global variable from the BaseStrategy that can be access from storage is `asset`. If other global variables are needed for your specific implementation you can use the default `BaseLibrary` variable to easily retrieve any other needed variables withen the implementation such as totalAssets, totalDebt, isShutdown etc.

EX:

    require(!BaseLibrary.isShutdown(), "strategy is shutdown");

NOTE: It is not possible to write to the global storage state of a strategy internally post deployment. You will need to make external calls from the `manamagement` address to configure any of the desired variables.

To include permisioned function such as extra setters the two modifiers of `onlyManagement` and `onlyManagementAndKeepers` are available by default.

To make strategy writing as simple as possible there is a suite of optional 'Periphery Helper' contracts that can be inherited by your strategy to provide standardized and tested functionality for things like swaps. A full list of the periphery contracts can be view here https://github.com/Schlagonia/tokenized-strategy-periphery.

Cloning is available natively through the BaseStrategy and can also be done easily using `BaseLibrary.clone(...)`. The cloning function will initialize all defualt storage needed for the BaseStrategy as sepecified in the parameters of the clone function, but an internal initialize function will need to be used for any implementation specific initialization such as approvals.

NOTE: When cloning while using Periphery Helpers you should make sure to reset all variables from the helper contract that will be used. The periphery contracts leave all global variables as non-constants so they can be overriden by the implementations. This means when cloning they will all default back to 0, address(0) etc.

The symbol used for each tokenized strategy is set automatically with a standardized approach based of the `asset`'s symbol. Strategists should use the `name` parameter in constructor for a unique and descriptive name that encapsulates their specific strategy.

All other functionality such as reward selling, emergency functions, upgradability etc. is up to the strategist to determine what fits their vision the best. Due to the ability for strategies to stand alone from a Vault it is expected and encouraged for strategists to experiment with more complex, risky or previously unfeasible strategies.

### APR Oracles

In order for easy integration with Vaults, frontends, debt allocaters etc. There is the option to also create an apr oracle contract for your specific contract implementation that should return the expected apr of the strategy based on some give debtChange. 

### Testing

Due to the nature of the BaseStrategy utilizing an external library for the majority of its logic the default interface for any tokenized strategy will not allow proper testing of all functions. Testing of your strategy should utilize the pre built `ITokenizedStrategy` interface to cast any deployed strategy through for testingo as seen in the confest example. You can add any external function that you add for your specific implementation to this interface to be able to test all functions with one variable. 

E.X.

    strategy = management.deploy(project.Strategy, asset)
    strategy =  project.ITokenizedStrategy.at(strategy.address)

Due to the permisionless nature of the tokenized strategies all tests are written without integration with any meta vault funding it. While those tests can be added all V3 vaults utilize the ERC-4626 standard for deposit/withdraws and accounting so they should be able to be plugged in easily to any number of different vaults with the same `asset`.

### Deployment

#### Contract Verification

See the ApeWorx [documentation](https://docs.apeworx.io/ape/stable/) and [github](https://github.com/ApeWorX/ape) for more information.
