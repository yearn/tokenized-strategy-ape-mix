// SPDX-License-Identifier: GPL-3.0
pragma solidity 0.8.18;

import {AprOracleBase} from "@periphery/AprOracleBase.sol";


contract StrategyAprOracle is AprOracleBase {

    constructor() AprOracleBase("Strategy Apr Oracle Example"){}

    /**
     * @notice Will return the expected Apr of a strategy post a debt change.
     * @dev _delta is a signed integer so that it can also repersent a debt
     * decrease.
     *
     * _delta will be == 0 to get the current apr.
     *
     * This will potentially be called during non-view functions so gas 
     * effeciency should be taken into account.
     *
     * @param _delta The difference in debt.
     * @return . The expected apr for the strategy.
     */
    function aprAfterDebtChange(
        address _asset,
        int256 _delta
    ) external view override returns (uint256) {
        // TODO: Implement any neccesary logic to return the most accurate
        //      APR estimation for the strategy.
    }
}