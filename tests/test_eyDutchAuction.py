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
def erc721Contract(NFT, accounts):
    return NFT.deploy(
        "TopT", # password
        {'from': accounts[0]}
    )

@pytest.fixture
def DutchAuctionContract(EYDutchAuction, erc20Contract, erc721Contract, accounts):
    return EYDutchAuction.deploy(
        erc20Contract,
        erc721Contract,
        {'from': accounts[0]}
    )

