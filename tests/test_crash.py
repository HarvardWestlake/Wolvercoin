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

@pytest.fixture
def erc20Contract(Token, accounts):
    return Token.deploy("Wolvercoin", "WVC", 18, 1000,{'from': accounts[0]})

# @pytest.fixture
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
    assert erc20Contract.approve(crashContract.address, 12, {'from': accounts[0]})
    crashContract.placeBets(accounts[0], 12,{'from': accounts[0]})
    assert crashContract.getHashValue() == 12

def test_withdrawBet(crashContract, erc20Contract, accounts)
    #this needs to approve money from the pot to the gambler. need pot address
    assert erc20Contract.approve(crashContract.address, {'from': accounts[0]})
    crashContract.withdrawBet(accounts[0], {'from': accounts[0]})
    assert crashContract.getHashValue() == 0