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
def wolvercoinContract(Token, accounts):
    return Token.deploy("Wolvercoin", "WVC", 10, 1000000000000000000, {'from': accounts[0]})

@pytest.fixture
def SocialAndDonationsContract(SocialAndDonations, accounts): 
    SocialAndDonations.deploy(wolvercoinContract, {'from': accounts[0]})
    return SocialAndDonationsContract

def test_donate(socialAdnDonationsContract, wolvercoinContract):
    donator = accounts[4]
    reciever = accounts[5]
    admin = accounts[1]
    assert wolvercoinContract.mint(donator, 420, {'from': admin}) # Supply the account with some token
    assert wolvercoinContract.mint(reciever, 420, {'from': admin}) # Supply the account with some token
    assert str(wolvercoinContract.getBalanceOf(donator).return_value) == "420"
    assert str(wolvercoinContract.getBalanceOf(reciever).return_value) == "420"
    SocialAndDonationsContract.donate(donator,reciever,69)
