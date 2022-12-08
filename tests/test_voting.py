# @dev Basic testing for the voting system
# @author Evan Stokdyk (@Focus172)

# @version 0.3.7
import pytest
from brownie import accounts
from web3.exceptions import ValidationError
from brownie.network.state import Chain

chain = Chain()

# . This runs before ALL tests
@pytest.fixture
def votingContract(VotingAndRep, accounts):
    return VotingAndRep.deploy({'from': accounts[0]})
    

def _as_wei_value(base, conversion):
    if conversion == "wei":
        return base
    if conversion == "gwei":
        return base * (10 ** 9)
    return base * (10 ** 18)

def test_contractDeployment(votingContract, accounts):
    assert votingContract.voteDuration() == 100, "Voting period should be initialized"
    assert votingContract.contractMaintainer() == accounts[0].address, "Maintainer should be initailized to creator"

def test_proposeVote(votingContract, accounts):
    sampleContract = votingContract.address

    # test that all the values are updated
    votingContract.proposeVote(sampleContract, "Vote for Pedro")
    assert votingContract.endBlock(sampleContract) == chain[-1]['number'] + 100, "Vote should be able to be proposed"
    
    votingContract.proposeVote(accounts[3], "Fry About It! :(", {'pay': 1000})
    assert votingContract.endBlock(accounts[3]) == chain[-1]['number'] + 100, "Donation vote should be able to be proposed"
    
    assert votingContract.endBlock(accounts[2]) == 0, "Non-existant Vote should not have data"
    
    # test that you can pay it

    # test that you can't call it in bad tasts
    assert True


def test_setDiabled(votingContract, accounts):
    assert True