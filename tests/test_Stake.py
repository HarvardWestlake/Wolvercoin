#version ^0.3.7
import pytest
import brownie
from web3.exceptions import ValidationError
from brownie.network.state import Chain
chain = Chain()

DEFAULT_GAS = 100000

# Account Details
# 0 - Deployer
# 1:3 - User

# . This runs before ALL tests
@pytest.fixture
def wolvercoinContract(Token, accounts):
    return Token.deploy("Wolvercoin", "WVC", 18, 4200000000000, {'from': accounts[0]})

@pytest.fixture
def activeUserContract(ActiveUser, accounts):
    activeUserContract = ActiveUser.deploy(accounts[0], {'from': accounts[0]})
    activeUserContract.setCurrentGradYear(2021, {'from': accounts[0]})
    activeUserContract.addUser(accounts[0], {'from': accounts[0]})
    activeUserContract.addUser(accounts[1], {'from': accounts[0]})
    activeUserContract.addUser(accounts[2], {'from': accounts[0]})
    activeUserContract.addUser(accounts[3], {'from': accounts[0]})
    return activeUserContract

@pytest.fixture
def stakeContract(Stake, activeUserContract, wolvercoinContract, accounts):
    stakeContract = Stake.deploy(wolvercoinContract, activeUserContract, {'from': accounts[0]})
    # when first deploying, the stakeContract should be given an initial amount (like a bank's reserve) 
    # hopefully this amount doesn't run out - we might need to add a functionality to ensure that the bank always has reserves
    wolvercoinContract.mint (stakeContract, 1000000)
    return stakeContract

def test_checkActiveUser(stakeContract, wolvercoinContract, activeUserContract, accounts):
    wolvercoinContract.approve (accounts [3], 1000, {'from': stakeContract})
    badAccountFail = False 
    try:
        stakeContract.stake (accounts[3], 10)
    except:
        badAccountFail = True
    assert badAccountFail, "Accounts that are not active users should not be able to stake"

def test_nonexistentAccount(stakeContract, wolvercoinContract, activeUserContract, accounts):
    assert stakeContract.stakeAmounts(accounts[0]) == 0, "An account that has not staked should have a balance of 0"

def test_unstakeForNonexistentAccount(stakeContract, wolvercoinContract, activeUserContract, accounts):
    badAccountFail = False
    try:
        stakeContract.unstake(accounts[0],2)
    except:
        badAccountFail = True
    assert badAccountFail, "Accounts without money should not be able to unstake"

def test_stake(stakeContract, wolvercoinContract, accounts):
    # Setup
    wolvercoinContract.mint (accounts[1], 1000, {'from': accounts[0]})
    originalAmountInAccount = int(wolvercoinContract.balanceOf(accounts[1]))
    assert originalAmountInAccount == 1000, "Account should have 1000 coins before test begins"

    # Test (start by approving)
    wolvercoinContract.approve (stakeContract, 10, {'from': accounts[1]})
    stakeContract.stake(accounts[1], 10, {'from': accounts[1]}) 
    assert stakeContract.stakeAmounts(accounts[1]) == 10, "Account should have 1 coin staked"
    assert int(wolvercoinContract.balanceOf(accounts[1])) == int(originalAmountInAccount - 10), "Account should have 10 coins staked"

def test_unstakeMoreThanStaked (stakeContract, wolvercoinContract, accounts):
    wolvercoinContract.mint (accounts[1], 1000, {'from': accounts[0]})
    wolvercoinContract.approve (stakeContract, 1000, {'from': accounts[1]})
    stakeContract.stake(accounts[1], 10, {'from': accounts[1]}) 
    with pytest.raises(Exception) as e_info:
        stakeContract.unstake(accounts[1], 20, {'from', accounts[1]}), "Account cannot unstake more than they have staked"

def test_validUnstake (stakeContract, wolvercoinContract, accounts):
    wolvercoinContract.mint (accounts[1], 1000, {'from': accounts[0]})
    wolvercoinContract.approve (stakeContract, 1000, {'from': accounts[1]})
    originalAmountInAccount = int(wolvercoinContract.balanceOf(accounts[1]))
    stakeContract.stake(accounts[1], 10, {'from': accounts[1]}) 
    stakeContract.unstake(accounts[1], 10, {'from': accounts[1]})
    assert stakeContract.stakeAmounts(accounts[1]) == 0, "Account should have 0 coins staked"
    assert int(wolvercoinContract.balanceOf(accounts[1])) == int(originalAmountInAccount), "Account should have 10 coins unstaked"

"""
def test_waitLessThanTwoWeeks (stakeContract, wolvercoinContract, accounts):
    wolvercoinContract.mint (accounts[1], 1000, {'from': accounts[0]})
    wolvercoinContract.approve (stakeContract, 1000, {'from': accounts[1]})
    originalAmountInAccount = int(wolvercoinContract.balanceOf(accounts[1]))
    stakeContract.stake(accounts[1], 10, {'from': accounts[1]})
    currentChainTime = chain.time()
    chain.sleep(1210000)
    assert chain.time() == (currentChainTime + 1210000)

    # Should check unstaked balance before unstaking

    #stakeContract.unstake (accounts[1], 10)
    #assert stakeContract.stakeAmounts(accounts[1]) == 0, "Account should have 0 coins left"
    #assert int(wolvercoinContract.balanceOf(accounts [1])) == int(originalAmountInAccount - 10),"Account should get back 12 coins (10*14*10/100))"

def test_waitMoreThanTwoWeeks (stakeContract, wolvercoinContract, accounts):
    wolvercoinContract.approve (stakeContract, 1000, {'from': stakeContract})
    wolvercoinContract.approve (accounts[0], 1000, {'from': stakeContract})
    originalAmountInAccount = int(wolvercoinContract.balanceOf(accounts[0]))
    assert wolvercoinContract.balanceOf (stakeContract) > 0
    assert stakeContract.stake (accounts[0], 12)
    currentChainTime = chain.time()
    chain.sleep(1814400)
    assert chain.time() == (currentChainTime + 1814400)
    stakeContract.unstake (accounts[0], 12)
    assert int(wolvercoinContract.balanceOf(accounts [0])) == int(originalAmountInAccount + 13), "Account should get back 25 coins (12*21*10/100))"
"""