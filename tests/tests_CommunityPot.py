#version ^0.3.8
import pytest
import brownie
from web3.exceptions import ValidationError

@pytest.fixture
def communityPotContract (CommunityPot, accounts):
    return CommunityPot.deploy({'from': accounts[0]})

def  _as_wei_value(base, conversion):
    if conversion == "wei":
        return base
    if conversion == "gwei":
        return base * (10 ** 9)
    return base * (10 ** 18)

def test_addMoney(communityPotContract, accounts):
    assert communityPotContract.getMoney() ==0
    communityPotContract.addMoney (10)
    assert communityPotContract.getMoney() ==10

def test_setElectedOfficials (communityPotContract, accounts):
    newElectedOfficials = dynArray [address, 3]
    newElectedOfficials.append(accounts[0])
    newElectedOfficials.append(accounts[1])
    newElectedOfficials.append(accounts[2])
    assert newElectedOfficials!=communityPotContract.getElectedOfficials()
    communityPotContract.setElectedOfficials (newElectedOfficials)
    assert  newElectedOfficials==communityPotContract.getElectedOfficials()
