#version ^0.3.7

# @dev Basic testing for the voting system
# @author Evan Stokdyk (@Focus172)
# @author Gavin Goldsmith (@Gav-G)
# @author Jack Moreland (@jmoreland57)

import pytest
from brownie import accounts
from web3.exceptions import ValidationError
from brownie.network.state import Chain

chain = Chain()

# . This runs before ALL tests
@pytest.fixture
def votingContract(VotingAndRep, accounts):
    return VotingAndRep.deploy(accounts[1], {'from': accounts[0]})
    

def _as_wei_value(base, conversion):
    if conversion == "wei":
        return base
    if conversion == "gwei":
        return base * (10 ** 9)
    return base * (10 ** 18)

def test_hasCoin(votingContract, accounts): 
    sampleContract = votingContract.address
    votingContract.incrementAccountVCBal(accounts[3],1000), "adds 1000 to accounts balance"
    votingContract.proposeVote(sampleContract, "Vote for Kian"), "starts a vote for Kian"
    votingContract.vote(accounts[3], votingContract.endBlock(sampleContract), 100), "User invests 100 coin into vote"
    assert votingContract.hasCoin(accounts[3], votingContract.endBlock(sampleContract)) == 100, "checks if it gets how much user invested in proposition"

def test_amountAvailable(votingContract, accounts):
    sampleContract = votingContract.address
    #votingContract.voterCoinBalance[accounts[3]] += 1000, "adds 1000 to accounts balance"
    votingContract.proposeVote(sampleContract, "Vote for cows"), "starts a vote for cows"
    votingContract.vote(accounts[3], votingContract.endBlock(sampleContract), 100), "User invests 100 coin into vote"
    votingContract.proposeVote(sampleContract, "Vote for sheep"), "starts a vote for sheep"
    votingContract.vote(accounts[3], votingContract.endBlock(sampleContract), 100), "User invests 100 coin into vote"
    votingContract.proposeVote(sampleContract, "Vote for clowns"), "starts a vote for clowns"
    votingContract.vote(accounts[3], votingContract.endBlock(sampleContract), 100), "User invests 100 coin into vote"
    assert votingContract.hasCoin(accounts[3]) == 700, "checks if amount available is according to what was invested"

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
    
    winningProp = "0xc0ffee254729296a45a3885639AC7E10F9d54979"
    losingProp = "0x999999cf1046e68e36E1aA2E0E07105eDDD1f08E"
    votingContract.setActiveProposition(winningProp, 0)
    votingContract.setActiveProposition(losingProp, 0)
    votingContract.setVoterCoinSupply(votingContract.voterCoinSupply() + 100)
    votingContract.setAccountVCBal(accounts[4],50)
    votingContract.setAccountVCBal(accounts[6],50)
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

def test_endVote(votingContract, accounts):
    winningProp = "0xc0ffee254729296a45a3885639AC7E10F9d54979"
    losingProp = "0x999999cf1046e68e36E1aA2E0E07105eDDD1f08E"
    votingContract.setActiveProposition(winningProp, 0)
    votingContract.setActiveProposition(losingProp, 0)
    votingContract.setVoterCoinSupply(votingContract.voterCoinSupply() + 100)
    votingContract.setAccountVCBal(accounts[4],50)
    votingContract.setAccountVCBal(accounts[6],50)
    votingContract.setVoterCoinSupply(100)
    votingContract.vote(accounts[4],losingProp,10)
    votingContract.vote(accounts[6],winningProp,20)
    assert votingContract.voterCoinStaked() == 30
    votingContract.finishVote(losingProp)
    votingContract.finishVote(winningProp)
    assert votingContract.voterCoinSupply() == 90
    assert votingContract.voterCoinStaked() == 0

def test_vote(votingContract, accounts):
    sampleContract = votingContract.address
    initialBal = votingContract.voterCoinBalance()[accounts[1]]
    totalInvestedBefore = votingContract.activePropositions()[votingContract.endBlock(sampleContract)]
    votingContract.vote(accounts[1], votingContract.endBlock(sampleContract), 10)

    # tests if user's votercoin balance decreases by specified amount
    assert votingContract.voterCoinBalance()[accounts[1]] == initialBal-10

    #tests if total amount of votercoin in proposition increases by specified amount
    assert votingContract.activePropositions()[votingContract.endBlock(sampleContract)] == (totalInvestedBefore + 10)
