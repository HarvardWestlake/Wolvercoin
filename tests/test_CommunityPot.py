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

def test_WorkingTransact(communityPotContract, erc20Contract, accounts):
    erc20Contract.transfer(communityPotContract.getPotAddress(), 50, {'from': accounts[0]}) #idk if it is correct address 
    communityPotContract.addMoney(50) #fairly certain addMoney isn't doing what it should
    assert str(erc20Contract.getBalanceOf(communityPotContract.getPotAddress())) == "50"

    #idk idk idk
    senderAccount=communityPotContract.getPotAddress()
    erc20Contract.approve(accounts[2], 25, {"from": senderAccount})
    communityPotContract.Transact(25, accounts[2])

    assert communityPotContract.getMoney()==25
    assert str(erc20Contract.getBalanceOf(accounts[2])) == "25" #this assumes each account starts w/ 0 money
    
      
def test_NotEnoughToTransact(communityPotContract, accounts):
    with pytest.raises(Exception) as e_info:
        communityPotContract.Transact(MONEY, accounts[1])
    