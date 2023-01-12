#version ^0.3.7

import pytest
from brownie import accounts
from web3.exceptions import ValidationError
from brownie.network.state import Chain

chain = Chain()
time = 0
#chain.sleep(uint)
#chain.time()

# . This runs before ALL tests
@pytest.fixture
def newDutchAuctionContract(NewDutchAuction, Token, accounts):
    NFTContract = Token.deploy("unused", "notused", 8, 100000, {'from':accounts[0]})
    NFTContract.transferFrom(accounts[0], accounts[1], 5000, {'from':accounts[0]})
    time = time + chain.time()
    return NewDutchAuction.deploy(2000, 10, NFTContract, 12345, 100, {'from': accounts[0]})

def _as_wei_value(base, conversion):
    if conversion == "wei":
        return base
    if conversion == "gwei":
        return base * (10 ** 9)
    return base * (10 ** 18)

def test___init__(newDutchAuctionContract, accounts):
    assert newDutchAuctionContract.getDURATION({'from': accounts[0]}).return_value == 100
    assert newDutchAuctionContract.getSeller({'from': accounts[0]}).return_value == accounts[0]
    assert newDutchAuctionContract.getStartingPrice({'from': accounts[0]}).return_value == 2000
    assert newDutchAuctionContract.getDiscountRate({'from': accounts[0]}).return_value == 10
    assert newDutchAuctionContract.getStartAt({'from': accounts[0]}).return_value == time
    assert newDutchAuctionContract.getExpiresAt({'from': accounts[0]}).return_value == time + 100

def test_getPrice(newDutchAuctionContract, accounts):
    elapsed = chain.time() - time
    price = newDutchAuctionContract.getStartingPrice({'from': accounts[0]}).return_value - (newDutchAuctionContract.getDiscountRate({'from': accounts[0]}).return_value * elapsed)
    assert newDutchAuctionContract.getPrice({'from': accounts[0]}).return_value == price
    chain.sleep(10)
    elapsed = elapsed + 10
    price = newDutchAuctionContract.getStartingPrice({'from': accounts[0]}) - (newDutchAuctionContract.getDiscountRate({'from': accounts[0]}).return_value * elapsed)
    assert newDutchAuctionContract.getPrice({'from': accounts[0]}).return_value == price

def test_buy(newDutchAuctionContract, accounts):
    nft = newDutchAuctionContract.getNft({'from': accounts[1]})
    newDutchAuctionContract.buy({'from': accounts[1]})
    assert nft.ownerOf(12345) == accounts[1]