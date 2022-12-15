#version ^0.3.8
import pytest
import brownie

DEFAULT_GAS = 100000

@pytest.fixture
def erc20Contract(Token, accounts):
    return Token.deploy(
        "Wolvercoin", # _name
        "WVC", # _symbol
        18, # _decimals
        1000, # _supply
        {'from': accounts[0]}
    )

@pytest.fixture
def publicGoodsContract(PublicGoods, erc20Contract, accounts):
    return PublicGoods.deploy(
        erc20Contract,
        {'from': accounts[0]}
    )


def test_createGood(publicGoodsContract, accounts):
    assert publicGoodsContract.createGood("Ice Cream Party", 10, {'from': accounts[0]}), "createGood failed"
    returnVal = publicGoodsContract.getGoal("Ice Cream Party", {'from': accounts[0]}).return_value
    assert str(returnVal) == "10", "getGoal returned wrong value"

def test_contribute(publicGoodsContract, erc20Contract, accounts):
    creatorOfGood = accounts[5]
    donator = accounts[4]
    admin = accounts[0]

    # User starts with lots of eth in their account so no need to mint
    assert publicGoodsContract.createGood("Pizza Party", 10, {'from': creatorOfGood}), "createGood failed"

    assert erc20Contract.mint(donator, 69420, {'from': admin}) # Supply the account with some token
    assert str(erc20Contract.getBalanceOf(donator).return_value) == "69420"
    
    assert erc20Contract.approve(publicGoodsContract.address, 69420, {'from': donator}) # Approve expenditure
    assert str(erc20Contract.getApprovedAmountOf(donator, publicGoodsContract.address).return_value) == "69420"
    
    assert publicGoodsContract.contribute("Pizza Party", 3, {'from': donator}), "contribute failed"
    
    returnVal = publicGoodsContract.getContributionTotal("Pizza Party", {'from': accounts[0]}).return_value
    assert str(returnVal) == "3", "getContributionTotal returned wrong value"
    assert str(erc20Contract.getBalanceOf(donator).return_value) == str(69420 - 3)

def test_retract(publicGoodsContract, erc20Contract, accounts):
    creatorOfGood = accounts[5]
    donator = accounts[4]
    admin = accounts[0]

    assert publicGoodsContract.createGood("Monkey Party", 10, {'from': creatorOfGood}), "createGood failed"

    assert publicGoodsContract.retract("Monkey Party", 1, {'from': admin}), "retract failed"

    assert erc20Contract.mint(donator, 69420, {'from': admin}) # Supply the account with some token
    assert str(erc20Contract.getBalanceOf(donator).return_value) == "69420"

    assert erc20Contract.approve(publicGoodsContract.address, 69420, {'from': donator}) # Approve expenditure
    assert str(erc20Contract.getApprovedAmountOf(donator, publicGoodsContract.address).return_value) == "69420"

    assert publicGoodsContract.contribute("Monkey Party", 3, {'from': donator}), "contribute failed"
    assert publicGoodsContract.retract("Monkey Party", 1, {'from': admin}), "retract failed"

    #retract doesn't subtract from donator amount or total contributions
    assert str(erc20Contract.getBalanceOf(donator).return_value) == str(69420 - 2)
    returnVal = publicGoodsContract.getContributionTotal("Monkey Party", {'from': admin}).return_value
    assert str(returnVal) == "2", "getContributionTotal returned wrong value"

def test_complete_goal_achieved(publicGoodsContract, erc20Contract, accounts):
    creatorOfGood = accounts[6]
    donator = accounts[7]
    admin = accounts[0]

    assert publicGoodsContract.createGood("French Toast Party", 10, {'from': creatorOfGood}), "createGood failed"

    assert erc20Contract.mint(donator, 69420, {'from': admin})
    assert str(erc20Contract.getBalanceOf(donator).return_value) == "69420"
    
    assert erc20Contract.approve(publicGoodsContract.address, 69420, {'from': donator})
    assert str(erc20Contract.getApprovedAmountOf(donator, publicGoodsContract.address).return_value) == "69420"
    
    assert publicGoodsContract.contribute("French Toast Party", 10, {'from': donator}), "contribute failed"
    
    returnVal = publicGoodsContract.getContributionTotal("French Toast Party", {'from': accounts[0]}).return_value
    assert str(returnVal) == "10", "getContributionTotal returned wrong value"
    assert str(erc20Contract.getBalanceOf(donator).return_value) == str(69420 - 10)

    assert publicGoodsContract.complete("French Toast Party", {'from': creatorOfGood})
    assert str(erc20Contract.getBalanceOf(donator).return_value) == str(69420 - 10)

def test_complete_goal_not_achieved(publicGoodsContract, erc20Contract, accounts):
    creatorOfGood = accounts[6]
    donator = accounts[7]
    admin = accounts[0]

    assert publicGoodsContract.createGood("French Toast Party", 10, {'from': creatorOfGood}), "createGood failed"

    assert erc20Contract.mint(donator, 69420, {'from': admin})
    assert str(erc20Contract.getBalanceOf(donator).return_value) == "69420"
    
    assert erc20Contract.approve(publicGoodsContract.address, 69420, {'from': donator})
    assert str(erc20Contract.getApprovedAmountOf(donator, publicGoodsContract.address).return_value) == "69420"
    
    assert publicGoodsContract.contribute("French Toast Party", 3, {'from': donator}), "contribute failed"
    assert str(erc20Contract.getBalanceOf(donator).return_value) == str(69420 - 3)
    
    returnVal = publicGoodsContract.getContributionTotal("French Toast Party", {'from': accounts[0]}).return_value
    assert str(returnVal) == "3", "getContributionTotal returned wrong value"
    assert str(erc20Contract.getBalanceOf(donator).return_value) == str(69420 - 3)

    assert publicGoodsContract.complete("French Toast Party", {'from': creatorOfGood})
    assert str(erc20Contract.getBalanceOf(donator).return_value) == "69420" # Make sure user got their money back