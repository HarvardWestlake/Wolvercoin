#version ^0.3.8
import pytest
from brownie import accounts
from web3.exceptions import ValidationError

@pytest.fixture
def communityPotContract(CommunityPot, accounts):
    return CommunityPot.deploy({'from': accounts[0]})

def  _as_wei_value(base, conversion):
    if conversion == "wei":
        return base
    if conversion == "gwei":
        return base * (10 ** 9)
    return base * (10 ** 18)

def test_addMoney(communityPotContract):
    assert communityPotContract.getMoney() == 0, "initialize money to zero"
    communityPotContract.addMoney (10)
    assert communityPotContract.getMoney()==10

def test_setElectedOfficials (communityPotContract, accounts):
    newElectedOfficials =  [accounts[0],accounts[1],accounts[2]]
    assert newElectedOfficials!=communityPotContract.getElectedOfficials()
    communityPotContract.setElectedOfficials (newElectedOfficials)
    assert  newElectedOfficials==communityPotContract.getElectedOfficials()
