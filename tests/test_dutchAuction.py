#version ^0.3.7

import pytest
from brownie import accounts
from web3.exceptions import ValidationError
from brownie.network.state import Chain

chain = Chain()

# . This runs before ALL tests
@pytest.fixture
def dutchAuctionContract(DutchAuction, Token, accounts):
    TokenContract = Token.deploy("str", "string", 8, 12, accounts[9], {'from':accounts[0]})
    NFTContract = Token.deploy("unused", "notused", 8, 12, accounts[9], {'from':accounts[0]})
    return DutchAuction.deploy(100, 100, 200, NFTContract, TokenContract, {'from': accounts[0]})

def _as_wei_value(base, conversion):
    if conversion == "wei":
        return base
    if conversion == "gwei":
        return base * (10 ** 9)
    return base * (10 ** 18)

def test_endAuction(dutchAuctionContract, accounts):
    assert dutchAuctionContract.getEndDate() != 0
    dutchAuctionContract.endAuction()
    #assert privateGoodContract.getEndDate() == 0
