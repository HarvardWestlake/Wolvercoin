#version ^0.3.8

import pytest
import brownie
from web3.exceptions import ValidationError

# . This runs before ALL tests
@pytest.fixture
def crashContract(Crash, accounts):
    return Crash.deploy({'from': accounts[1]})

@external
def test_placeBet(gambler: address, amount: uint256)

@external
def test_withdrawBet(gambler: address)
def test_crashUpdating(crashContract, accounts):
    multiplierInit = crashContract.getMultiplier()
    crashContract.updateCrash()
    newMultiplier = crashContract.getMultiplier()
    print (newMultiplier)
    print (multiplierInit)
    assert newMultiplier != multiplierInit