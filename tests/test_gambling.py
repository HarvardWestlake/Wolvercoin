#version ^0.3.8

import pytest
import brownie
from web3.exceptions import ValidationError

# . This runs before ALL tests
@pytest.fixture
def crashContract(Gambling, accounts):
    return Gambling.deploy({'from': accounts[1]})

def test_crashUpdating(crashContract, accounts):
    multiplierInit = crashContract.getMultiplier()
    txn1 = crashContract.updateCrash()
    newMultiplier = crashContract.getMultiplier()
    assert newMultiplier != multiplierInit

