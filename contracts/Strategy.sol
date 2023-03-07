// SPDX-License-Identifier: GPL-3.0
pragma solidity 0.8.15;

import {BaseStrategyAdapter, ERC20} from "./BaseStrategyAdapter.sol";

// Import interfaces for many popular DeFi projects, or add your own!
//import "../interfaces/<protocol>/<Interface>.sol";

// NOTE: Should use the 'asset' variable to get the address of the vaults token rather than 'want'
// NOTE: To implement permissioned functions you can use the onlyManagement and onlyKeepers modifiers

contract Strategy is BaseStrategyAdapter {
    constructor(
        address _asset,
        address _vault
    ) BaseStrategyAdapter(_asset, "Strategy Example", _vault) {}

    /**
     * @notice Should invest up to '_amount' of 'asset'.
     * @dev Should do any needed parameter checks. 0 may be passed in as '_amount'.
     *
     * Both permisionless deposits and permissioned reports will lead to this function being called with all currently idle funds sent as '_amount'.
     * The '_reported' bool is how to differeniate between the two. If true this means it was called at the end of a report with the potential of coming
     * through a trusted relay and therefore safe to perform otherwise manipulatable transactions.
     *
     * @param _amount The amount of 'asset' that the strategy should attemppt to deposit in the yield source.
     * @param _reported Bool repersenting if this is part of a permissined 'report'.
     */
    function _invest(uint256 _amount, bool _reported) internal override {
        // TODO: implement deposit logice EX:
        //
        //      lendingpool.deposit(asset, _amount ,0);
    }

    /**
     * @notice Will attempt to free the '_amount' of 'asset'.
     * @dev The amount of 'asset' that is already loose has already been accounted for.
     *
     * Should do any needed parameter checks, '_amount' may be more than is actually available.
     *
     * Should not rely on asset.balanceOf(address(this)) calls other than for diff accounting puroposes.
     *
     * @param _amount, The amount of 'asset' to be freed.
     */
    function _freeFunds(uint256 _amount) internal override {
        // TODO: implement withdraw logic EX:
        //
        //      lendingPool.withdraw(asset, _amount);
    }

    /**
     * @notice Internal non-view function to return the accurate amount of funds currently held by the Strategy
     * @dev This should do any needed harvesting, rewards selling, accrual etc. to get the most accurate view of current assets.
     *
     * This can leave any or all assets uninvested if desired as there will always be a _invest() call at the end of the report
     * with '_reported' set as true to differentiate between a normal deposit.
     *
     * Care should be taken when relying on oracles or swap values rather than actual amounts as all Strategy profit/loss accounting
     * will be done based on this returned value.
     *
     * All applicable assets including loose assets should be accounted for in this function.
     *
     * @return _invested A trusted and accurate account for the total amount of 'asset' the strategy currently holds.
     */
    function _totalInvested() internal override returns (uint256 _invested) {
        // TODO: Implement harvesting logic and accurate accounting EX:
        //
        //      _claminAndSellRewards();
        //      _invested = aToken.balanceof(address(this)) + ERC20(asset).balanceOf(address(this));
        _invested = ERC20(asset).balanceOf(address(this));
    }

    /*//////////////////////////////////////////////////////////////
                    OPTIONAL TO OVERRIDE BY STRATEGIST
    //////////////////////////////////////////////////////////////*/

    // NOTE: Should avoid overriding `harvestTrigger` if possible, rather adjust maxReportDelay post
    //      deployment for time based harvest cycle which is how V3 should operate

    /**
     * @notice Optional function for strategist to override that can be called in between reports
     * @dev If '_tend' is used tendTrigger() will also need to be overridden.
     *
     * This call can only be called by a persionned role so may be sent through protected relays.
     *
     * This can be used to harvest and compound rewards, deposit idle funds, perform needed
     * poisition maintence or anything else that doesn't need a full report for.
     *
     * @param _totalIdle The current amount of idle funds that are available to invest.
     *
    function _tend(uint256 _totalIdle) internal override {}
    */

    /**
     * @notice Optional trigger to override if tend() will be used by the strategy.
     * 
     * @dev This is the V3 tendTrigger to be used. No callCost parameter is needed.
     * 
     * This must be implemented if the strategy hopes to invoke _tend().
     *
     * @return . Should return true if tend() should be called by keeper or false if not.
     *
    function tendTrigger() public view virtual returns (bool) {
        return false;
    }
    */
}
