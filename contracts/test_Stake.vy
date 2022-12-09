import pytest
import brownie
from web3.exceptions import ValidationError

DEFAULT_GAS = 100000

# . This runs before ALL tests
@pytest.fixture
def stakeContract(Stake, accounts):
    return Stake.deploy(accounts[1], {'from': accounts[0]})

def test_unstake (stakeContract, accounts):
    #can only be run if accounts[0] staked less than 10
    assert stakeContract.unstake(accounts[0],10) == False
    assert stakeContract.unstake(accounts[0],8) == True
    #problem: need to wait 2 weeks to really test the if statement