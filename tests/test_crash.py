#version ^0.3.8

import pytest
import brownie
from web3.exceptions import ValidationError
from brownie import accounts
from brownie.network.state import Chain

# . This runs before ALL tests
@pytest.fixture
def crashContract(Crash, Token, accounts):
    tokenContract = Token.deploy("Wolvercoin", "WVC", 18, 1000, {'from': accounts[0]})
    return Crash.deploy("0x0000000000000000000000000000000000000000", tokenContract, "0x0000000000000000000000000000000000000000", {'from': accounts[1]})

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

@pytest.fixture
def erc20Contract(Token, accounts):
    return Token.deploy("wolvercoin", "wvc", 18, 1000,{'from': accounts[0]})

@pytest.fixture
def gamblingContract(erc20Contract, codeGambling, accounts):
    return codeGambling.deploy(accounts[1], erc20Contract, {'from': accounts[0]})

def test_placeBets(gamblingContract, erc20Contract, accounts):
    assert erc20Contract.approve(gamblingContract.address, 12, {'from': accounts[0]})
    gamblingContract.placeBets(accounts[0], 12,{'from': accounts[0]})
    assert gamblingContract.getHashValue() == 12
    