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
def SocialAndDonationsContract(SocialAndDonations, accounts):
    return SocialAndDonations.deploy("0x0000000000000000000000000000000000000000" , {'from': accounts[0]})

with pytest.raises(Exception) as e_info:
    SocialAndDonationsContract.voteOfficials()

with pytest.raises(Exception) as e_info:
    SocialAndDonationsContract.endVoteOfficials()

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

   one : uint256
   one = SocialAndDonationsContract.getProposalVotes(2)
   SocialAndDonationsContract.voteProposal(2)
   two : uint256
   two = SocialAndDonationsContract.getProposalVotes(2)
   assert one == 0
   assert two == 1
   #Makes sure the same person can't vote again
   with pytest.raises(Exception) as e_info:
    SocialAndDonationsContract.voteProposal(2)
   

   
   
    


#def test_donate():
    #b: bool = False
    #balance = accounts[1].balance()
    #socialAndDonationsContract.donate(accounts[1].address, accounts[0].balance)
   # 'accounts[0].transfer(accounts[1], "10 ether", gas_price=0)'
    #if(accounts[0].balance == 0):
       # b == True
    #assert b == True 
   # """

def test_beginVoteOfficial(SocialAndDonationsContract):
    SocialAndDonationsContract.beginVoteOfficial(accounts[0])
    assert SocialAndDonationsContract.getOfficalVotingPeriod