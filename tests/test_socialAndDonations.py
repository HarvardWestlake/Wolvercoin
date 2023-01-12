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
def socialAdnDonationsContract(socialAdnDonations, accounts,): 
    return socialAdnDonations.deploy(wolvercoinContract, {'from': accounts[0]})

def wolvercoinContract(Wolvercoin, accounts):
    return Wolvercoin.deploy("Wolvercoin", "WVC", 10, 1000000000000000000, {'from': accounts[0]})

def test_voteOfficials (socialAdnDonationsContract):
    with pytest.raises(Exception) as e_info:
        socialAdnDonationsContract.voteOfficials()

    with pytest.raises(Exception) as e_info:
        socialAdnDonationsContract.endVoteOfficials()

def test_donate(socialAdnDonationsContract, wolvercoinContract):
    donator = accounts[4]
    reciever = accounts[5]
    admin = accounts[1]
    assert wolvercoinContract.mint(donator, 420, {'from': admin}) # Supply the account with some token
    assert wolvercoinContract.mint(reciever, 420, {'from': admin}) # Supply the account with some token
    assert str(wolvercoinContract.getBalanceOf(donator).return_value) == "420"
    assert str(wolvercoinContract.getBalanceOf(reciever).return_value) == "420"
    socialAdnDonationsContract.donate(donator,reciever,69)

