#version ^0.3.8
# @dev Basic testing for the voting system
# @author Evan Stokdyk (@Focus172)

import pytest
import brownie
from brownie import accounts
from web3.exceptions import ValidationError
from brownie.network.state import Chain

chain = Chain()

#test for socialAndDonatios
@pytest.fixture
def socialAdnDonationsContract(socialAdnDonations, accounts): 
    return socialAdnDonations.deploy("0x0000000000000000000000000000000000000000" , {'from': accounts[0]})

@pytest.fixture
def erc20Contract(Token, accounts):
    return Token.deploy(
        "Wolvercoin", # _name
        "WVC", # _symbol
        18, # _decimals
        1000, # _supply
        {'from': accounts[0]}
    )

def test_voteOfficials (socialAdnDonationsContract):
    with pytest.raises(Exception) as e_info:
        socialAdnDonationsContract.voteOfficials()

    with pytest.raises(Exception) as e_info:
        socialAdnDonationsContract.endVoteOfficials()

def test_donate(socialAdnDonationsContract, erc20Contract):
    donator = accounts[4]
    reciever = accounts[5]
    admin = accounts[0]

    assert erc20Contract.mint(donator, 420, {'from': admin}) # Supply the account with some token
    assert str(erc20Contract.getBalanceOf(donator).return_value) == "420"
    socialAdnDonationsContract.donate(donator,reciever,69)
    assert str(erc20Contract.getBalanceOf(reciever).return_value) == "69"

    




"""
def test_voteProposal (socialAdnDonationsContract):
   one = socialAdnDonationsContract.getProposalVotes(2)
   socialAdnDonationsContract.voteProposal(2)
   two = socialAdnDonationsContract.getProposalVotes(2)
   assert one != two
"""
