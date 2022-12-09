import brownie
from web3.exceptions import ValidationError

DEFAULT_GAS = 100000

# . This runs before ALL tests
@pytest.fixture
def stakeContract(Stake, accounts):
    return Stake.deploy(accounts[1], {'from': accounts[0]})
    #I'm passing in accounts[1] as the bank address I think?

def test_unstake (stakeContract, accounts):
    #this test can only be run once the stake method is merged into the code
    stakeContract.stake(accounts[0], 9)
    assert stakeContract.unstake(accounts[0],10) == False
    assert stakeContract.unstake(accounts[0],8) == True
    #will test the wait two weeks if condition once we figure out how to change the timestamp