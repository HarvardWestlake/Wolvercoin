#version ^0.3.7

import pytest
from brownie import accounts
from web3.exceptions import ValidationError
from brownie.network.state import Chain

chain = Chain()

# . This runs before ALL tests
@pytest.fixture
def newDutchAuctionContract(NewDutchAuction, Token, accounts):
    NFTContract = Token.deploy("unused", "notused", 8, 12, {'from':accounts[0]})
    return NewDutchAuction.deploy(200, 10, NFTContract, 12345, 1000, {'from': accounts[0]})

def _as_wei_value(base, conversion):
    if conversion == "wei":
        return base
    if conversion == "gwei":
        return base * (10 ** 9)
    return base * (10 ** 18)

def test_getPrice(newDutchAuctionContract, accounts):
    assert newDutchAuctionContract

def test_buy(newDutchAuctionContract, accounts):
    assert