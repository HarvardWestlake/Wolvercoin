#version ^0.3.7
import pytest
import brownie
from web3.exceptions import ValidationError
from brownie.network.state import Chain
chain = Chain()

DEFAULT_GAS = 100000

# . This runs before ALL tests
@pytest.fixture
def wolvercoinContract(Token, accounts):
    return Token.deploy("Wolvercoin", "WVC", 10, 1000000000000000000, {'from': accounts[0]})

@pytest.fixture
def activeUserContract(ActiveUser, accounts):
    activeUserContract = ActiveUser.deploy (accounts[0], {'from': accounts[0]})
    activeUserContract.addUser (accounts[0], {'from': accounts[0]})
    return activeUserContract

@pytest.fixture
def stakeContract(Stake, activeUserContract, wolvercoinContract, accounts):
    stakeContract = Stake.deploy(wolvercoinContract, activeUserContract, {'from': accounts[0]})
    # when first deploying, the stakeContract should be given an initial amount (like a bank's reserve) 
    # hopefully this amount doesn't run out - we might need to add a functionality to ensure that the bank always has reserves
    wolvercoinContract.mint (stakeContract, 1000000)
    return stakeContract

def test_checkActiveUser (stakeContract, wolvercoinContract, activeUserContract, accounts):
    wolvercoinContract.approve (accounts [3], 1000, {'from': stakeContract})
    badAccountFail = False 
    try:
        stakeContract.stake (accounts[3], 10)
    except:
        badAccountFail = True
    assert badAccountFail, "Accounts that are not active users should not be able to stake"

def test_nonexistentAccount (stakeContract, wolvercoinContract, activeUserContract, accounts):
    assert stakeContract.stakeAmounts(accounts[0]) == 0, "An account that has not staked should have a balance of 0"

def test_unstakeForNonexistentAccount (stakeContract, wolvercoinContract, activeUserContract, accounts):
    badAccountFail = False
    try:
        stakeContract.unstake(accounts[0],2)
    except:
        badAccountFail = True
    assert badAccountFail, "Accounts without money should not be able to unstake"

def test_unstakeMoreThanStaked (stakeContract, wolvercoinContract, accounts):
    wolvercoinContract.approve (stakeContract, 1000, {'from': stakeContract})
    stakeContract.stake(accounts[0], 1) 
    badAccountFail = False
    try:
        stakeContract.unstake(accounts[0], 2)
    except:
        badAccountFail = True
    assert badAccountFail, "Account cannot unstake more than they have staked"

def test_validUnstake (stakeContract, wolvercoinContract, accounts):
    wolvercoinContract.approve (stakeContract, 1000, {'from': stakeContract})
    originalAmountInAccount = int(wolvercoinContract.balanceOf(accounts[0]))
    assert stakeContract.stake (accounts[0], 10)
    assert stakeContract.unstake(accounts[0],9), "Account can unstake less than they have staked"
    assert stakeContract.stakeAmounts(accounts[0]) == 1, "Account should only have 1 coin left staked"
    assert int(wolvercoinContract.balanceOf(accounts[0])) == int(originalAmountInAccount - 4), "Account should get back 6 coins (2/3 of the unstaked amt)"

def test_waitExactlyTwoWeeks (stakeContract, wolvercoinContract, accounts):
    wolvercoinContract.approve (stakeContract, 1000, {'from': stakeContract})
    wolvercoinContract.approve (accounts[0], 1000, {'from': stakeContract})
    originalAmountInAccount = int(wolvercoinContract.balanceOf(accounts[0]))
    assert stakeContract.stake (accounts[0], 12)
    currentChainTime = chain.time()
    chain.sleep(1210000)
    assert chain.time() == (currentChainTime + 1210000)
    stakeContract.unstake (accounts[0], 9)
    assert stakeContract.stakeAmounts(accounts[0]) == 3, "Account should have 3 coins left"
    assert int(wolvercoinContract.balanceOf(accounts [0])) == int(originalAmountInAccount), "Account should get back 12 coins (9*14*10/100))"

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