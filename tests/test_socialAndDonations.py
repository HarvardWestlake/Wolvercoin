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
def SocialAndDonationsContract(SocialAndDonations, wolvercoinContract, accounts): 
    SocialAndDonationsContract = SocialAndDonations.deploy(wolvercoinContract, {'from': accounts[0]})
    wolvercoinContract.mint(SocialAndDonationsContract, 1000)
    return SocialAndDonationsContract

def test_donate(SocialAndDonationsContract, wolvercoinContract, accounts):
    SocialAndDonationsContract.donate(accounts[1], 69, {'from': SocialAndDonationsContract})
    assert wolvercoinContract.getBalanceOf(accounts[1]) == 67
