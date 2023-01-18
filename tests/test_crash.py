#version ^0.3.8

import pytest
import brownie
from web3.exceptions import ValidationError
from brownie import accounts
from brownie.network.state import Chain

# . This runs before ALL tests
@pytest.fixture
def activeUserContract(ActiveUser, accounts):
    return ActiveUser.deploy(accounts[0], {'from': accounts[0]})

@pytest.fixture
def erc20Contract(Token, accounts):
    return Token.deploy("Wolvercoin", "WVC", 18, 1000,{'from': accounts[0]})

@pytest.fixture
def crashContract(Crash, activeUserContract, erc20Contract, accounts):
    return Crash.deploy(activeUserContract, erc20Contract, {'from': accounts[1]})


def test_crashFromRandom(crashContract, accounts):
    assert False == crashContract.getCrashFromRandomNumber(100).return_value
    assert False == crashContract.getCrashFromRandomNumber(900).return_value
    assert True == crashContract.getCrashFromRandomNumber(999).return_value

def test_crashGamble(crashContract, accounts):
    multiplierInit = crashContract.getMultiplier()
    crashContract.getCrashGambleHelper(450)
    newMultiplier = crashContract.getMultiplier()
    print (newMultiplier)
    print (multiplierInit)
    assert newMultiplier != multiplierInit
    
def test_crashUpdating(crashContract, accounts):
    multiplierInit = crashContract.getMultiplier()
    crashContract.updateCrash()
    newMultiplier = crashContract.getMultiplier()
    print (newMultiplier)
    print (multiplierInit)
    assert newMultiplier != multiplierInit
    
    chain = Chain()

# @dev basic testing for placeBet 
# @author Ava Weinrot 



def test_placeBets(crashContract, erc20Contract, accounts):
    #pot is accounts[1]
    #gambler is accounts[2]
    
    #assert erc20Contract.approve(accounts[2], 12, {'from': accounts[2]})
    
    potBefore = erc20Contract.getBalanceOf(accounts[1])
    crashContract.placeBets(accounts[2], 12,{'from': accounts[2]})
    potAfter = erc20Contract.getBalanceOf(accounts[1])
    
    assert potAfter - potBefore == 12
    assert crashContract.getHashValue() == 12
    