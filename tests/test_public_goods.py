#version ^0.3.8
import pytest
import brownie

DEFAULT_GAS = 100000

@pytest.fixture
def erc20Contract(ERC20, accounts):
    return ERC20.deploy(
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
    assert publicGoodsContract.createGood("Pizza Party", 10, {'from': accounts[0]}), "createGood failed"
    assert erc20Contract.mint(accounts[0], 69420, {'from': accounts[0]}) # Supply the account with some token
    assert erc20Contract.approve(publicGoodsContract.address, 69420, {'from': accounts[0]}) # Approve expenditure
    assert publicGoodsContract.contribute("Pizza Party", 3, {'from': accounts[0]}), "contribute failed"
    # The line above doesn't work
    # I get a VirtualMachineError: revert
    # but when I comment out the offending line in ERC20.vy it just fails on the line before o-o

    returnVal = publicGoodsContract.getContributionTotal("Pizza Party", {'from': accounts[0]}).return_value
    assert str(returnVal) == "3", "getContributionTotal returned wrong value"

def test_retract(publicGoodsContract, accounts):
    # TODO for @monkeymatt2023
    raise NotImplementedError

def test_complete(publicGoodsContract, accounts):
    assert publicGoodsContract.createGood("Laser Tag Party", 10, {'from': accounts[0]}), "createGood failed"
    assert erc20Contract.mint(accounts[0], 69420, {'from': accounts[0]})
    assert erc20Contract.approve(publicGoodsContract.address, 69420, {'from': accounts[0]})
    assert publicGoodsContract.contribute("Laser Tag Party", 3, {'from': accounts[0]}), "contribute failed"
    assert publicGoodsContract.complete("Laser Tag Party")

    assert publicGoodsContract.createGood("French Toast Party", 10, {'from': accounts[0]}), "createGood failed"
    assert erc20Contract.mint(accounts[0], 69420, {'from': accounts[0]})
    assert erc20Contract.approve(publicGoodsContract.address, 69420, {'from': accounts[0]})
    assert publicGoodsContract.contribute("French Toast Party", 10, {'from': accounts[0]}), "contribute failed"
    assert publicGoodsContract.complete("French Toast Party")
