#version ^0.3.8
import pytest
from brownie import accounts
from web3.exceptions import ValidationError

MONEY=500
#thank you eric 
@pytest.fixture
def erc20Contract(Token, accounts):
    return Token.deploy(
        "Wolvercoin", # _name
        "WVC", # _symbol
        18, # _decimals
        1000, # _supply
        {'from': accounts[0]}
    )

#check if def line is correct
@pytest.fixture
def communityPotContract(CommunityPot, erc20Contract, accounts): #edited
    return CommunityPot.deploy(accounts[4], erc20Contract, {'from': accounts[0]}) #edited

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

def test_VerifyElectedOfficial(communityPotContract, accounts):
    newElectedOfficials =  [accounts[0],accounts[1],accounts[2]] #so apparently you need these 3 lines first?? idk
    communityPotContract.setElectedOfficials (newElectedOfficials)
    assert  newElectedOfficials==communityPotContract.getElectedOfficials()

    assert communityPotContract.VerifyElectedOfficial(accounts[0])==True
    assert communityPotContract.VerifyElectedOfficial(accounts[1])==True
    assert communityPotContract.VerifyElectedOfficial(accounts[2])==True
    assert communityPotContract.VerifyElectedOfficial(accounts[5])==False #edited 
      
def test_NotEnoughToTransact(communityPotContract, accounts):
    with pytest.raises(Exception) as e_info:
        communityPotContract.Transact(MONEY, accounts[1])
    