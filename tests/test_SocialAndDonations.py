# @version ^0.3.8

import pytest
from brownie import accounts
from web3.exceptions import ValidationError
from brownie.network.state import Chain

chain = Chain()

@pytest.fixture
def SocialAndDonations(SocialAndDonations, accounts):
    return SocialAndDonations.deploy({'from': accounts[0]})

def test_addPotentialOfficial(SocialAndDonations, accounts):
    SocialAndDonations.addStudent(accounts[0],2000)
    SocialAndDonations.addStudent(accounts[1],1000)
    SocialAndDonations.addPotentialOfficial(accounts[0])
    SocialAndDonations.addPotentialOfficial(accounts[1])
    SocialAndDonations.addPotentialOfficial(accounts[2])
    assert SocialAndDonations.getLengthOfPotential().return_value == 2

def test_vote(SocialAndDonations, accounts):
    SocialAndDonations.vote(accounts[0])
    SocialAndDonations.vote(accounts[1])
    SocialAndDonations.vote(accounts[1])
    assert SocialAndDonations.getVotes(accounts[0]).return_value == 1
    assert SocialAndDonations.getVotes(accounts[1]).return_value == 2


def test_determineResult(SocialAndDonations, accounts):
    SocialAndDonations.addStudent(accounts[0],2000)
    SocialAndDonations.addStudent(accounts[1],1000)
    SocialAndDonations.addPotentialOfficial(accounts[0])
    SocialAndDonations.addPotentialOfficial(accounts[1])
    assert SocialAndDonations.determineResult().return_value == accounts[1]

def test_addStudent(SocialAndDonations, accounts):
    SocialAndDonations.addStudent(accounts[0],2000)
    SocialAndDonations.addStudent(accounts[1],1000)
    assert SocialAndDonations.getLengthOfStudents().return_value == 2

def test_checkIfActive(SocialAndDonations, accounts):
    SocialAndDonations.addStudent(accounts[0],2000)
    SocialAndDonations.addStudent(accounts[1],1000)
    assert SocialAndDonations.checkIfActive(accounts[0]).return_value == True

def test_voteProposal (SocialAndDonations):
  #makes sure the person can't vote for a proposal that isn't 0, 1, or 2
  with pytest.raises(Exception) as e_info:
    SocialAndDonations.voteProposal(3)
    SocialAndDonations.voteProposal(-1)
  #makes sure the person can't vote when the voting period is false
  SocialAndDonations.setOfficalVotingPeriod (False)
  with pytest.raises(Exception) as e_info:
    SocialAndDonations.voteProposal(1)
  SocialAndDonations.setOfficalVotingPeriod (True)
  assert SocialAndDonations.getProposalVotes(2) ==0
  SocialAndDonations.voteProposal(2)
  assert SocialAndDonations.getProposalVotes(2) == 1
  #Makes sure the same person can't vote again
  with pytest.raises(Exception) as e_info:
   SocialAndDonations.voteProposal(2)

def test_beginVoteOfficial(SocialAndDonations):
    SocialAndDonations.beginVoteOfficial(accounts[0]) == False
    with pytest.raises(Exception) as e_info:
        teacher = SocialAndDonations.getTeachers()
        official = SocialAndDonations.getElectedOffical()
        assert SocialAndDonations.beginVoteOfficial(teacher) == True
        assert SocialAndDonations.beginVoteOfficlal(official) == False      
    assert SocialAndDonations.getOfficalVotingPeriod()



