#version ^0.3.7

import pytest
from brownie import accounts
from web3.exceptions import ValidationError
from brownie.network.state import Chain

chain = Chain()

# . This runs before ALL tests
@pytest.fixture
def dutchAuctionContract(DutchAuction, ERC20, accounts):
    ERC20Contract = ERC20.deploy("str", "string", 8, 12, {'from':accounts[0]})
    NFTContract = ERC20.deploy("unused", "notused", 8, 12, {'from':accounts[0]})
    return DutchAuction.deploy(100, 100, 200, NFTContract, ERC20Contract, {'from': accounts[0]})

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

def test_countdown(dutchAuctionContract, accounts):
    assert dutchAuctionContract._countdown() != 0
    
