#version ^0.3.8

import pytest
import brownie
from web3.exceptions import ValidationError
from brownie import accounts
from brownie.network.state import Chain

# . This runs before ALL tests
@pytest.fixture
def activeUserContract(ActiveUser, accounts):
    return ActiveUser.deploy(accounts[1], {'from': accounts[0]})

@pytest.fixture
def erc20Contract(Token, accounts):
    return Token.deploy("Wolvercoin", "WVC", 18, 1000,{'from': accounts[0]})

@pytest.fixture
def crashContract(Crash, Token, accounts):
    return Crash.deploy(activeUserContract, erc20Contract, "0x0000000000000000000000000000000000000000", {'from': accounts[1]})

# @pytest.fixturexw
# def spendingContract(erc20Contract, codeGambling, accounts):
#     return codeGambling.deploy(accounts[1], erc20Contract, {'from': accounts[0]})

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
# seems like a big confusion because the pot account address = the placer of bets

def test_placeBets(spendingContract, erc20Contract, accounts):
    tokenWVC = 0
    crash = 1
    player = 2
    assert erc20Contract.approve(accounts[2], 12, {'from': accounts[0]})
    crashContract.placeBets(accounts[2], 12, {'from': accounts[2]})
    assert erc20Contract.getBalanceOf(accounts[1]) == 12
    assert crashContract.getHashValue({'from': accounts[2]}) == 12

def test_withdrawBet(crashContract, erc20Contract, accounts)
    #this needs to approve money from the pot to the gambler. need pot address
    assert erc20Contract.approve(accounts[1], 12, {'from': accounts[0]})
    crashContract.withdrawBet(accounts[2], {'from': accounts[0]})
    assert crashContract.getHashValue({'from': accounts[2]}) == 0