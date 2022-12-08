import pytest
import brownie
from web3.exceptions import ValidationError

DEFAULT_GAS = 100000

# . This runs before ALL tests
@pytest.fixture
def stakeContract(Stake, accounts):
    return Stake.deploy(accounts[1], {'from': accounts[0]})
    #i do not know what this does
    #problem: how can I make sure that Stake has access to all the ERC20 methods?

def test_unstake ():
    stakeContract.unstake(accounts[0],5)
    #problem: need to wait 2 weeks to really test the if statement
    #problem: must use stake before unstaking