#version ^0.3.8

# @dev Basic testing for the voting system
# @author Evan Stokdyk (@Focus172)

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


def test_setContractMaintainer(votingContract, accounts):
    
    stopBadContractChange = False
    try:
        votingContract.setContractMaintainer(accounts[5], {'from': accounts[2]})
    except:
        stopBadContractChange = True
    assert stopBadContractChange, "Randoms should not be able to change maintainer"
    
    allowChanges = True
    try:
        votingContract.setContractMaintainer(accounts[5], {'from': accounts[0]})
    except:
        allowChanges = False
    assert allowChanges, "Maintainer should be able to change maintainer"

def test_burnCoin(votingContract, accounts):
    
    winningProp = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
    losingProp = "82e35a63ceba37e9646434c5dd412ea577147f1e4a41ccde1614253187e3dbf9"
    votingContract.activePropositions[winningProp] = 0
    votingContract.activePropositions[losingProp] = 0
    votingContract.voterCoinSupply += 100
    votingContract.voterCoinBalance[accounts[4]] = 50
    votingContract.voterCoinBalance[accounts[6]] = 50
    votingContract.vote(accounts[4],losingProp,10)
    votingContract.vote(accounts[6],winningProp,20)
    
    stopBadBurn = False
    try:
        votingContract.burnCoin(accounts[4])
    except:
        stopBadBurn = True
    assert stopBadBurn, "Coin should not be burned/returned if user is on losing side of the vote"

    allowBurn = True
    try:
        votingContract.burnCoin(accounts[6])
    except:
        allowBurn = False
    assert allowBurn, "Coin should be burned/returned if user is on winning side of the vote"