#version ^0.3.8
# @dev Basic testing for the voting system
# @author Evan Stokdyk (@Focus172)

import pytest
from brownie import accounts
from web3.exceptions import ValidationError
from brownie.network.state import Chain

chain = Chain()

#test for socialAndDonatios
@pytest.fixture
def socialAdnDonationsContract(socialAdnDonations, accounts): 
    return socialAdnDonations.deploy("0x0000000000000000000000000000000000000000" , {'from': accounts[0]})

def test_voteOfficials (socialAdnDonationsContract):
    with pytest.raises(Exception) as e_info:
        socialAdnDonationsContract.voteOfficials()

    with pytest.raises(Exception) as e_info:
        socialAdnDonationsContract.endVoteOfficials()

def test_donate(socialAdnDonationsContract, accounts):
    b: bool = False
    balance = accounts[0].balance()
    socialAdnDonationsContract.donate(accounts[0],accounts[1],balance, {'from' : accounts[0]})
    if(accounts[0].balance == 0):
        b == True
    assert b == True
"""
def test_voteProposal (socialAdnDonationsContract):
   one = socialAdnDonationsContract.getProposalVotes(2)
   socialAdnDonationsContract.voteProposal(2)
   two = socialAdnDonationsContract.getProposalVotes(2)
   assert one != two
"""
