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
        return socialAdnDonations.deploy({'from': accounts[0]})

with pytest.raises(Exception) as e_info:
    socialAdnDonationsContract.voteOfficials()

with pytest.raises(Exception) as e_info:
    socialAdnDonationsContract.endVoteOfficials()

    def test_voteProposal (proposalNumber: uint256):
        b: bool = False
        socialAdnDonationsContract.voteProposal(2)
        if socialAdnDonations.proposalVotes[2] == 1:
            b = True
        assert b = True
    
    def test_beginVoteOfficial(user: address):
        isTeacher = True
        if (isTeacher == True):
            assert self.officialVotingPeriod == True  
        else:
            asser self.officialVotingPeriod == False
        

      
        