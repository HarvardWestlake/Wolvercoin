import pytest
from brownie import accounts
from brownie.network.state import Chain

chain = Chain()

# . This runs before ALL tests
@pytest.fixture
def votingContract(VotingAndRep, accounts):
    return VotingAndRep.deploy(accounts[0], 100, {'from': accounts[0]})

def _as_wei_value(base, conversion):
    if conversion == "wei":
        return base
    if conversion == "gwei":
        return base * (10 ** 9)
    return base * (10 ** 18)

def test_hasCoin(votingContract, accounts): 
    sampleContract = votingContract.address
    votingContract.mint(accounts[3], 1000, {'from': accounts[0]}) # adds 1000VC to accounts balance
    votingContract.proposeVote(sampleContract, "Vote for Kian") # starts a vote for Kian
    votingContract.vote(sampleContract, 100, {'from': accounts[3]}) # User invests 100 coin into vote
    assert votingContract.amountInFavor(sampleContract, accounts[3]) == 100, "Should be able to see money in vote"

def test_amountAvailable(votingContract, accounts):
    sampleContract = votingContract.address
    votingContract.mint(accounts[3], 1000, {'from': accounts[0]}) # adds 1000VC to accounts balance
    votingContract.proposeVote(sampleContract, "Vote for cows")# starts a vote for cows
    votingContract.vote(sampleContract, 100, {'from': accounts[3]}) # User invests 100 coin into vote

    failCase = False
    try:
        votingContract.proposeVote(sampleContract, "Vote for sheep"), "starts a vote for sheep"
    except:
        failCase = True
    assert failCase, "should not be able to make vote for something that already exists"

    assert votingContract.vote(sampleContract, 100, {'from': accounts[3]}), "User invests 100 coin into vote"
    assert votingContract.balanceOf(accounts[3]) == 800, "checks if amount available is according to what was invested"

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

def test_setContractMaintainer(votingContract, accounts):
    
    stopBadContractChange = False
    try:
        votingContract.setContractMaintainer(accounts[5], {'from': accounts[2]})
    except:
        stopBadContractChange = True
    assert stopBadContractChange, "Randoms should not be able to change maintainer"

def test_setDisbled(votingContract, accounts):

    badDisableFail = False
    try:
        votingContract.setDisabled(True, {'from': accounts[3]})
    except:
        badDisableFail = True
    assert badDisableFail, "Random accounts should not be able to disable the contract"

def test_vote(votingContract, accounts):
    sampleContract = votingContract.address

    votingContract.mint(accounts[1], 1000, {'from': accounts[0]}) # adds 1000VC to accounts balance
    initialBal = votingContract.balanceOf(accounts[1])
    totalInvestedBefore = votingContract.activePropositions(sampleContract)
    votingContract.vote(sampleContract, 10, {'from': accounts[1]})

    # tests if user's votercoin balance decreases by specified amount
    assert votingContract.balanceOf(accounts[1]) == initialBal-10

    #tests if total amount of votercoin in proposition increases by specified amount
    assert votingContract.activePropositions(sampleContract) == (totalInvestedBefore + 10)


def test_finishVote(votingContract, accounts):
    winningProp = address("0xc0ffee254729296a45a3885639AC7E10F9d54979")
    losingProp = address("0x999999cf1046e68e36E1aA2E0E07105eDDD1f08E")

    votingContract.mint(accounts[1], 10000, {'from': accounts[0]}) # account 1 balance: 10_000

    votingContract.proposeVote(winningProp, "you should vote for this thing", {'from': accounts[1]}, {'value': 1000})  # account 1 balance: 9_000

    votingContract.vote(winningProp, 7000) # account 1 balance: 2_000

    stopBadEndVote = False
    try:
        votingContract.finishVote(winningProp)
    except:
        stopBadEndVote = True
    assert stopBadEndVote, "Vote should not be ended before period"

    chain.mine(200) # skiping to well past the end of the vote

    # votingContract.finishVote(winningProp)
    # as they won half of 7_000 should be returned
    # this means they should get 3_500 back
    # account 1 balance: 5_500
    assert votingContract.votingContract.balanceOf(accounts[1]) == 5500
    assert votingContract.voterCoinStaked() == 0



# need to test running code works and that you can pass something that isn't a contract

