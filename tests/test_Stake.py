#version ^0.3.7
import pytest
import brownie
from web3.exceptions import ValidationError

# . This runs before ALL tests
@pytest.fixture
def stakeContract(Stake, Wolvercoin, accounts):
    wolvercoinContract = Wolvercoin.deploy("Wolvercoin", "WVC", 10, 10000000, {'from': accounts[0]})
    return Stake.deploy(accounts[1], wolvercoinContract, {'from': accounts[0]})
    #I'm passing in accounts[1] as the bank address

def test_nonexistentAccount (stakeContract, accounts):
    assert stakeContract.stakeAmounts(accounts[0]) == 0, "An account that has not staked should have a balance of 0"

def test_unstakeForNonexistentAccount (stakeContract, accounts):
    badAccountFail = False
    try:
        stakeContract.unstake(accounts[0],10)
    except:
        badAccountFail = True
    assert badAccountFail, "Accounts without money should not be able to unstake"

#def test_unstakeMoreThanStaked (stakeContract, accounts):
    #this can only be run once the stake method is merged into the code
    #stakeContract.stake(accounts[0], 10)
    #badAccountFail = False
    #try:
        #stakeContract.unstake(accounts[0],11)
    #except:
        #badAccountFail = True
    #assert badAccountFail, "Account cannot unstake more than they have staked"

#def test_validUnstake (stakeContract, accounts):
 #    stakeContract.stake(accounts[0], 10)
  #   assert stakeContract.unstake(accounts[0],9), "Account can unstake less than they have staked"
   #  assert stakeContract.stakeAmounts(accounts[0]) == 1, "Account should only have 1 coin left staked"
    # assert stakeContract.newAmt == 6, "Account should get back 6 coins (2/3 of the unstaked amt)"


    #will test the wait two weeks if condition once we figure out how to change the timestamp