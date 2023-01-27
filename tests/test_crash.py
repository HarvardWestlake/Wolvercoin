#version ^0.3.8

import pytest
import brownie
from web3.exceptions import ValidationError
from brownie import accounts
from brownie.network.state import Chain

# . This runs before ALL tests
@pytest.fixture
def crashContract(Crash, activeUserContract, wolvercoinContract, accounts):
    return Crash.deploy(activeUserContract, wolvercoinContract, {'from': accounts[1]})

@pytest.fixture
def activeUserContract(ActiveUser, accounts):
    return ActiveUser.deploy(accounts[1], {'from': accounts[0]})

@pytest.fixture
def wolvercoinContract(Token, Crash, accounts):
    return Token.deploy("wolvercoin", "wvc", 18, 1000,{'from': accounts[0]})

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

#@pytest.fixture
#def gamblingContract(erc20Contract, Crash, accounts):
 #   return codeGambling.deploy(accounts[1], erc20Contract, {'from': accounts[0]})

def test_placeBets(crashContract, wolvercoinContract, accounts):
    #account that deploys wolvercoin
    #token.deploy will be from an account
    #have to do minting from og account that created the wolvercoin -----> isnt this done in the creation of the contract?
    assert wolvercoinContract.approve(crashContract, 12, {'from': accounts[0]})
    crashContract.placeBets(12, {'from': accounts[0]}) #trying to place bet using money from accounts [1] which was transferred from accounts [0]
    assert crashContract.getHashValue(accounts[0]) == 12 
    