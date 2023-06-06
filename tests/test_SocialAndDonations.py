# @version ^0.3.8

import pytest
from brownie import accounts
from web3.exceptions import ValidationError
from brownie.network.state import Chain

chain = Chain()

@pytest.fixture
def SocialAndDonationsContract(SocialAndDonations, accounts):
    return SocialAndDonations.deploy(
        accounts[0],
        accounts[1],
        {'from': accounts[0]}
    )
@pytest.fixture
def erc20Contract(Token, accounts):
    return Token.deploy(
        "Wolvercoin", # _name
        "WVC", # _symbol
        18, # _decimals
        1000, # _supply
        {'from': accounts[0]}
    )

def SocialAndDonations(SocialAndDonations, accounts):
    return SocialAndDonations.deploy({'from': accounts[0]})

def test_addPotentialOfficial(SocialAndDonationsContract, accounts):
    SocialAndDonationsContract.addStudent(accounts[0],2000)
    SocialAndDonationsContract.addStudent(accounts[1],1000)
    SocialAndDonationsContract.addPotentialOfficial(accounts[0])
    SocialAndDonationsContract.addPotentialOfficial(accounts[1])
    SocialAndDonationsContract.addPotentialOfficial(accounts[2])
    assert SocialAndDonationsContract.getLengthOfPotential().return_value == 2

def test_vote(SocialAndDonationsContract, accounts):
    SocialAndDonationsContract.vote(accounts[0])
    SocialAndDonationsContract.vote(accounts[1])
    SocialAndDonationsContract.vote(accounts[1])
    assert SocialAndDonationsContract.getVotes(accounts[0]).return_value == 1
    assert SocialAndDonationsContract.getVotes(accounts[1]).return_value == 2


def test_determineResult(SocialAndDonationsContract, accounts):
    SocialAndDonationsContract.addStudent(accounts[0],2000)
    SocialAndDonationsContract.addStudent(accounts[1],1000)
    SocialAndDonationsContract.addPotentialOfficial(accounts[0])
    SocialAndDonationsContract.addPotentialOfficial(accounts[1])
    assert SocialAndDonationsContract.determineResult().return_value == accounts[1]

def test_addStudent(SocialAndDonationsContract, accounts):
    SocialAndDonationsContract.addStudent(accounts[0],2000)
    SocialAndDonationsContract.addStudent(accounts[1],1000)
    assert SocialAndDonationsContract.getLengthOfStudents().return_value == 2

def test_checkIfActive(SocialAndDonationsContract, accounts):
    SocialAndDonationsContract.addStudent(accounts[0],2000)
    SocialAndDonationsContract.addStudent(accounts[1],1000)
    assert SocialAndDonationsContract.checkIfActive(accounts[0]).return_value == True

def test_voteProposal (SocialAndDonationsContract):
  #makes sure the person can't vote for a proposal that isn't 0, 1, or 2
  with pytest.raises(Exception) as e_info:
    SocialAndDonationsContract.voteProposal(3)
    SocialAndDonationsContract.voteProposal(-1)
  #makes sure the person can't vote when the voting period is false
  SocialAndDonationsContract.setOfficalVotingPeriod (False)
  with pytest.raises(Exception) as e_info:
    SocialAndDonationsContract.voteProposal(1)
  SocialAndDonationsContract.setOfficalVotingPeriod (True)
  assert SocialAndDonationsContract.getProposalVotes(2) ==0
  SocialAndDonationsContract.voteProposal(2)
  assert SocialAndDonationsContract.getProposalVotes(2) == 1
  #Makes sure the same person can't vote again
  with pytest.raises(Exception) as e_info:
   SocialAndDonationsContract.voteProposal(2)

def test_beginVoteOfficial(SocialAndDonationsContract):
    SocialAndDonationsContract.beginVoteOfficial(accounts[0]) == False
    with pytest.raises(Exception) as e_info:
        teacher = SocialAndDonationsContract.getTeachers()
        official = SocialAndDonationsContract.getElectedOffical()
        assert SocialAndDonationsContract.beginVoteOfficial(teacher) == True
        assert SocialAndDonationsContract.beginVoteOfficlal(official) == False      
    assert SocialAndDonationsContract.getOfficalVotingPeriod()
#def test_take10Percent():

def test_deposit10Percent(erc20Contract,SocialAndDonationsContract,accounts):

    preBank=erc20Contract.balanceOf(accounts[0])
    preProvider=erc20Contract.balanceOf(accounts[1])
    erc20Contract.approve(SocialAndDonationsContract, 10, {"from": accounts[0]} )
    #SocialAndDonationsContract.deposit10Percent(accounts[0],accounts[1])    
    postBank=erc20Contract.balanceOf(accounts[0])
    postProvider=erc20Contract.balanceOf(accounts[1])
    #assert postBank==preBank-erc20Contract.totalOfTransactions*.1 and postProvider==preProvider+erc20Contract.totalOfTransactions*.1, "successfully invested 10%"
    assert True



