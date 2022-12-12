#version ^0.3.8
import pytest
import brownie

DEFAULT_GAS = 100000

# TODO: Tests are failing because this points to elon musk's ETH address,
# not a real ERC20 contract address. Change once ERC20 contract is implemented
ERC20_ADDRESS = "0x83fbdFB42df1eA8cD02a9B28a8F62Cb219D48561"

@pytest.fixture
def publicGoodsContract(PublicGoods, accounts):
    return PublicGoods.deploy(
        ERC20_ADDRESS, # erc20address
        {'from': accounts[0]}
    )

def test_createGood(publicGoodsContract, accounts):
    # TODO for @exoskeleton-1729
    raise NotImplementedError

def test_contribute(publicGoodsContract, accounts):
    assert publicGoodsContract.contribute("stevo", 3.0)
    assert publicGoodsContract.names[0] == "stevo", "correct name"

def test_retract(publicGoodsContract, accounts):
    # TODO for @monkeymatt2023
    raise NotImplementedError

def test_complete(publicGoodsContract, accounts):
    assert publicGoodsContract.createGood("Fortnite", 100)
    assert publicGoodsContract.contribute("Fortnite", 50)
    # TODO: when ERC20 contract is implemented, make sure it mints when public good is ended without reaching goal
    assert publicGoodsContract.complete("Fortnite")