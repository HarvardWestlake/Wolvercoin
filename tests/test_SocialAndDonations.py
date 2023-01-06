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
    SocialAndDonations.addPotentialOfficial(accounts[0])
    SocialAndDonations.addPotentialOfficial(accounts[1])
    assert SocialAndDonations.getLengthOfPotential().return_value == 2

def test_vote(SocialAndDonations, accounts):
    SocialAndDonations.vote(accounts[0])
    SocialAndDonations.vote(accounts[1])
    SocialAndDonations.vote(accounts[1])
    assert SocialAndDonations.getVotes(accounts[0]).return_value == 1
    assert SocialAndDonations.getVotes(accounts[1]).return_value == 2


def test_determineResult(SocialAndDonations, accounts):
    SocialAndDonations.addPotentialOfficial(accounts[0])
    SocialAndDonations.addPotentialOfficial(accounts[1])
    assert SocialAndDonations.determineResult().return_value == accounts[1]
