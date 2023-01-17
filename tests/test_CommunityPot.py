#version ^0.3.8
import pytest
from brownie import accounts
from web3.exceptions import ValidationError

MONEY=500

@pytest.fixture
def communityPotContract(CommunityPot, accounts):
    return CommunityPot.deploy(accounts[1], accounts[2], {'from': accounts[0]})

def  _as_wei_value(base, conversion):
    if conversion == "wei":
        return base
    if conversion == "gwei":
        return base * (10 ** 9)
    return base * (10 ** 18)

def test_addMoney(communityPotContract):
    assert communityPotContract.getMoney() == 0, "initialize money to zero"
    communityPotContract.AddMoney (10)
    assert communityPotContract.getMoney()==10

def test_setElectedOfficials (communityPotContract, accounts):
    newElectedOfficials =  [accounts[0],accounts[1],accounts[2]]
    assert newElectedOfficials!=communityPotContract.getElectedOfficials()
    communityPotContract.SetElectedOfficials (newElectedOfficials)
    assert  newElectedOfficials==communityPotContract.getElectedOfficials()

def test_VerifyElectedOfficial(communityPotContract, accounts):
     assert communityPotContract.VerifyElectedOfficial(accounts[2])==False
     newElectedOfficials =  [accounts[0],accounts[1],accounts[2]]
     communityPotContract.SetElectedOfficials (newElectedOfficials)
     assert communityPotContract.VerifyElectedOfficial(accounts[2])==True
     

def test_Transact(communityPotContract, accounts):
    with pytest.raises(Exception) as e_info:
        communityPotContract.Transact(MONEY, accounts[1])