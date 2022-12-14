import pytest
from brownie import accounts
from web3.exceptions import ValidationError
from brownie.network.state import Chain

chain = Chain()

# . This runs before ALL tests
@pytest.fixture
def votingContract(VotingAndRep, accounts):
    return VotingAndRep.deploy(accounts[0], {'from': accounts[0]})
    

def _as_wei_value(base, conversion):
    if conversion == "wei":
        return base
    if conversion == "gwei":
        return base * (10 ** 9)
    return base * (10 ** 18)

def test_contractDeployment(votingContract, accounts):
    assert votingContract.voteDuration() == 100, "Voting period should be initialized"


def test_proposeVote(votingContract, accounts):
    sampleContract = votingContract.address

    # test that all the values are updated in base case
    votingContract.proposeVote(sampleContract, "Vote for Pedro")
    assert votingContract.endBlock(sampleContract) == chain[-1]['number'] + 100, "Vote should be able to be proposed"
    assert votingContract.storedDonation(sampleContract) == 0, "No money should be saved if none is paid"

    # test that all the values are updated when paid
    votingContract.proposeVote(accounts[3], "Fry About It! :(", {'value': 1000})
    assert votingContract.endBlock(accounts[3]) == chain[-1]['number'] + 100, "Donation vote should be able to be proposed"
    assert votingContract.storedDonation(accounts[3]) == 1000, "Should be keeping track of money sent with vote"
    
    # test that values are empty when there is not contract
    assert votingContract.endBlock(accounts[2]) == 0, "Non-existant Vote should not have data"
    assert votingContract.storedDonation(accounts[2]) == 0, "Empty votes should not have money in them"


def test_setDisbled(votingContract, accounts):

    badDisableFail = False
    try:
        votingContract.setDisabled(True, {'from': accounts[3]})
    except:
        badDisableFail = True
    assert badDisableFail, "Random accounts should not be able to disable the contract"


    # This code relies on adding admins which is not a problem I want to solve but has been tested independently
    """
    votingContract.setDisabled(True, {'from': accounts[0]})

    runWhenDisabledfail = False
    try:
        votingContract.proposeVote(accounts[5], "sample message")
    except:
        runWhenDisabledfail = True
    assert runWhenDisabledfail, "Contract should not function while diabled"
    
    votingContract.setDisabled(False, {'from': accounts[0]})

    contractReenabled = True
    try:
        votingContract.proposeVote(accounts[5], "sample message")
    except:
        contractReenabled = False
    assert contractReenabled, "Contract should be able to be re-enabled"
    """