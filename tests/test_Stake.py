#version ^0.3.7
import pytest
import brownie
from web3.exceptions import ValidationError

DEFAULT_GAS = 100000

# . This runs before ALL tests
@pytest.fixture
def wolvercoinContract(Token, accounts):
    return Token.deploy("Wolvercoin", "WVC", 10, 1000000000000000000, {'from': accounts[0]})

@pytest.fixture
def stakeContract(Stake, ActiveUser, wolvercoinContract, accounts):
    activeUserContract = ActiveUser.deploy (accounts[0], {'from': accounts[0]})
    activeUserContract.addUser (accounts[0], {'from': accounts[0]})
    return Stake.deploy(accounts[1], wolvercoinContract, activeUserContract, {'from': accounts[0]})
    #I'm passing in accounts[1] as the bank address

def test_checkActiveUser (stakeContract, wolvercoinContract, accounts):
    wolvercoinContract.approve (accounts [3], 1000, {'from': stakeContract})
    wolvercoinContract.approve (accounts [1], 1000, {'from': stakeContract})
    badAccountFail = False 
    try:
        stakeContract.stake (accounts[3], 10)
    except:
        badAccountFail = True
    assert badAccountFail, "Accounts that are not active users should not be able to stake"

def test_nonexistentAccount (stakeContract, accounts):
    assert stakeContract.stakeAmounts(accounts[0]) == 0, "An account that has not staked should have a balance of 0"

def test_unstakeForNonexistentAccount (stakeContract, accounts):
    badAccountFail = False
    try:
        stakeContract.unstake(accounts[0],2)
    except:
        badAccountFail = True
    assert badAccountFail, "Accounts without money should not be able to unstake"

def test_unstakeMoreThanStaked (stakeContract, wolvercoinContract, accounts):
    wolvercoinContract.approve (accounts [0], 1000, {'from': stakeContract})
    wolvercoinContract.approve (accounts [1], 1000, {'from': stakeContract})
    stakeContract.stake(accounts[0], 1) 
    badAccountFail = False
    try:
        stakeContract.unstake(accounts[0], 2)
    except:
        badAccountFail = True
    assert badAccountFail, "Account cannot unstake more than they have staked"

def test_validUnstake (stakeContract, wolvercoinContract, accounts):
     wolvercoinContract.approve (accounts [0], 1000, {'from': stakeContract})
     wolvercoinContract.approve (accounts [1], 1000, {'from': stakeContract})
     assert stakeContract.stake (accounts[0], 10)
     #assert stakeContract.unstake(accounts[0],9), "Account can unstake less than they have staked"
     #assert stakeContract.stakeAmounts(accounts[0]) == 1, "Account should only have 1 coin left staked"
     #assert stakeContract.newAmt () == 6, "Account should get back 6 coins (2/3 of the unstaked amt)"
     


    #will test the wait two weeks if condition once we figure out how to change the timestamp