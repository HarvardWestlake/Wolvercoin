import pytest
import brownie
from web3.exceptions import ValidationError

# . This runs before ALL tests
@pytest.fixture
def stakeContract(Stake, accounts):
    return Stake.deploy(accounts[1], {'from': accounts[0]})
    #I'm passing in accounts[1] as the bank address

@pytest.fixture
def WolvercoinContract(Wolvercoin, accounts):
    return Wolvercoin.deploy("Wolvercoin", "WVC", 10, 10000000, {'from': accounts[0]})

def test_nonexistentAccount (stakeContract, accounts):
    assert stakeContract.stakeAmounts(accounts[0]) == 0, "An account that has not staked should have a balance of 0"

def test_unstakeForNonexistentAccount (stakeContract, WolvercoinContract, accounts):
    badAccountFail = False
    try:
        stakeContract.unstake(accounts[0],10,WolvercoinContract)
    except:
        badAccountFail = True
    assert badAccountFail, "Accounts without money should not be able to unstake"

#def test_unstakeLessThanTwoWeeks (stakeContract, accounts):
    #this can only be run once the stake method is merged into the code

    #stakeContract.stake(accounts[0], 10)
    #assert stakeContract.unstake(accounts[0],11) == (False, 0)
    #assert stakeContract.unstake(accounts[0],9) == (True, 6)


    #will test the wait two weeks if condition once we figure out how to change the timestamp