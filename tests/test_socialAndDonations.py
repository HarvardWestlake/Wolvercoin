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
def socialAndDonationsContract(socialAndDonations, accounts):
    return socialAndDonations.deploy("0x0000000000000000000000000000000000000000" , {'from': accounts[0]})

with pytest.raises(Exception) as e_info:
    socialAndDonationsContract.voteOfficials()

with pytest.raises(Exception) as e_info:
    socialAndDonationsContract.endVoteOfficials()

def test_voteProposal (socialAndDonationsContract):
   one = socialAndDonationsContract.getProposalVotes(2)
   socialAndDonationsContract.voteProposal(2)
   two = socialAndDonationsContract.getProposalVotes(2)
   assert one != two
    

#def test_donate():
    #b: bool = False
    #balance = accounts[1].balance()
    #socialAndDonationsContract.donate(accounts[1].address, accounts[0].balance)
   # 'accounts[0].transfer(accounts[1], "10 ether", gas_price=0)'
    #if(accounts[0].balance == 0):
       # b == True
    #assert b == True 
   # """

def test_beginVoteOfficial(socialAndDonationsContract):
    socialAndDonationsContract.beginVoteOfficial(accounts[0])
    assert socialAndDonationsContract.getOfficalVotingPeriod