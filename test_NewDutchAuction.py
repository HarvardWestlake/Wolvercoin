#version ^0.3.7

import pytest
from brownie import accounts
from web3.exceptions import ValidationError
from brownie.network.state import Chain

chain = Chain()
time = 0
#chain.sleep(uint256)
#chain.time()

# . This runs before ALL tests
@pytest.fixture
def newDutchAuctionContract(NewDutchAuction, Token, accounts):
    NFTContract = Token.deploy("unused", "notused", 8, 12, {'from':accounts[0]})
    time = chain.time()
    return NewDutchAuction.deploy(2000, 10, NFTContract, 12345, 100, {'from': accounts[0]})

def _as_wei_value(base, conversion):
    if conversion == "wei":
        return base
    if conversion == "gwei":
        return base * (10 ** 9)
    return base * (10 ** 18)

def test___init__(newDutchAuctionContract, accounts):
    assert newDutchAuctionContract.DURATION == 100
    assert newDutchAuctionContract.startingPrice == 2000
    assert newDutchAuctionContract.discountRate == 10
    assert newDutchAuctionContract.startAt == time
    assert newDutchAuctionContract.expiresAt == time + 100

def test_getPrice(newDutchAuctionContract, accounts):
    elapsed = chain.time() - time
    price = newDutchAuctionContract.startingPrice - (newDutchAuctionContract.discountRate * elapsed)
    assert newDutchAuctionContract.getPrice() == price
    chain.sleep(10)
    elapsed = elapsed + 10
    price = newDutchAuctionContract.startingPrice - (newDutchAuctionContract.discountRate * elapsed)
    assert newDutchAuctionContract.getPrice() == price

def test_buy(newDutchAuctionContract, accounts):
    accounts.transferFrom(accounts[0], accounts[1], 5000)
    accounts[1].newDutchAuctionContract.buy()
    assert NFTContract.ownerOf(12345) == accounts[1]