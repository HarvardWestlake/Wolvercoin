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

def test_callToERC20(publicGoodsContract, erc20Contract, accounts):
    print(publicGoodsContract.testCallToERC20().return_value)
    print("CA: " + publicGoodsContract.address)
    assert False

# def test_contribute(publicGoodsContract, erc20Contract, accounts):
#     creatorOfGood = accounts[5]
#     donator = accounts[4]
#     admin = accounts[0]

#     # User starts with lots of eth in their account so no need to mint
#     assert publicGoodsContract.createGood("Pizza Party", 10, {'from': creatorOfGood}), "createGood failed"
#     assert erc20Contract.mint(donator, 69420, {'from': admin}) # Supply the account with some token
#     assert str(erc20Contract.getBalanceOf(donator).return_value) == "69420"
#     assert erc20Contract.approve(publicGoodsContract.address, 69420, {'from': donator}) # Approve expenditure
#     assert str(erc20Contract.getApprovedAmountOf(donator, publicGoodsContract.address).return_value) == "69420"
#     # assert erc20Contract.burnFrom(donator, 40, {'from': publicGoodsContract.address})
#     assert publicGoodsContract.contribute("Pizza Party", 3, {'from': donator}), "contribute failed"
#     # returnVal = publicGoodsContract.getContributionTotal("Pizza Party", {'from': accounts[0]}).return_value
#     # assert str(returnVal) == "3", "getContributionTotal returned wrong value"

# def test_retract(publicGoodsContract, accounts):
#     # TODO for @monkeymatt2023
#     raise NotImplementedError

# def test_complete(publicGoodsContract, accounts):
#     assert publicGoodsContract.createGood("Laser Tag Party", 10, {'from': accounts[0]}), "createGood failed"
#     assert erc20Contract.mint(accounts[0], 69420, {'from': accounts[0]})
#     assert erc20Contract.approve(publicGoodsContract.address, 69420, {'from': accounts[0]})
#     assert publicGoodsContract.contribute("Laser Tag Party", 3, {'from': accounts[0]}), "contribute failed"
#     assert publicGoodsContract.complete("Laser Tag Party")

#     assert publicGoodsContract.createGood("French Toast Party", 10, {'from': accounts[0]}), "createGood failed"
#     assert erc20Contract.mint(accounts[0], 69420, {'from': accounts[0]})
#     assert erc20Contract.approve(publicGoodsContract.address, 69420, {'from': accounts[0]})
#     assert publicGoodsContract.contribute("French Toast Party", 10, {'from': accounts[0]}), "contribute failed"
#     assert publicGoodsContract.complete("French Toast Party")
