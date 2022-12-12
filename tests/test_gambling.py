#version ^0.3.8

import pytest
import brownie
from web3.exceptions import ValidationError

# . This runs before ALL tests
@pytest.fixture
def crashContract(Gambling, ActiveUser, accounts):
    activeUserContract = ActiveUser.deploy(accounts[0], {'from':accounts[1]})
    activeUserContract.setCurrentGradYear(2022)
    activeUserContract.addUser(accounts[2])
    activeUserContract.setCurrentGradYear(2023)
    activeUserContract.addUser(accounts[3])
    return Gambling.deploy(activeUserContract, {'from': accounts[1]})

def crashStart():
    crashContract.__init__()

def test_crashUpdating(crashContract, accounts):
    multiplierInit = crashContract.getMultiplier()
    txn1 = crashContract.updateCrash()
    newMultiplier = crashContract.getMultiplier()
    assert newMultiplier != multiplierInit

