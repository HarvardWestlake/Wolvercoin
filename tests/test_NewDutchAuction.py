#version ^0.3.7

import pytest
from brownie import accounts
from web3.exceptions import ValidationError
from brownie.network.state import Chain

import brownie

chain = Chain()
#chain.sleep(uint)
#chain.time()

# . This runs before ALL tests
@pytest.fixture
def newDutchAuctionContract(NewDutchAuction, Token, accounts):
    NFTContract = Token.deploy("unused", "notused", 8, 100000, {'from':accounts[0]})
    NFTContract.transferFrom(accounts[0], accounts[1], 50000, {'from':accounts[0]})
    NFTContract.transferFrom(accounts[0], accounts[2], 900, {'from':accounts[0]})
    return NewDutchAuction.deploy(2000, 10, NFTContract, 12345, 100, {'from': accounts[0]})

def _as_wei_value(base, conversion):
    if conversion == "wei":
        return base
    if conversion == "gwei":
        return base * (10 ** 9)
    return base * (10 ** 18)

def test___init__(newDutchAuctionContract, accounts):
    #make sure that constructor performs as expected
    time = chain.time()
    assert newDutchAuctionContract.getDURATION({'from': accounts[0]}).return_value == 100
    assert newDutchAuctionContract.getSeller({'from': accounts[0]}).return_value == accounts[0]
    assert newDutchAuctionContract.getStartingPrice({'from': accounts[0]}).return_value == 2000
    assert newDutchAuctionContract.getDiscountRate({'from': accounts[0]}).return_value == 10
    assert newDutchAuctionContract.getStartAt({'from': accounts[0]}).return_value == time
    assert newDutchAuctionContract.getExpiresAt({'from': accounts[0]}).return_value == time + 100

def test_getPrice(newDutchAuctionContract, accounts):
    #test price change with change in time
    time = chain.time()
    elapsed = chain.time() - time
    assert newDutchAuctionContract.getPrice({'from': accounts[0]}).return_value == (newDutchAuctionContract.getStartingPrice({'from': accounts[0]}).return_value - (newDutchAuctionContract.getDiscountRate({'from': accounts[0]}).return_value * elapsed))
    chain.sleep(10)
    elapsed = chain.time() - time
    assert newDutchAuctionContract.getPrice({'from': accounts[0]}).return_value == (newDutchAuctionContract.getStartingPrice({'from': accounts[0]}).return_value - (newDutchAuctionContract.getDiscountRate({'from': accounts[0]}).return_value * elapsed))

def test_buy(newDutchAuctionContract, accounts):
    nft = newDutchAuctionContract.getNft({'from': accounts[1]}).return_value
    price = newDutchAuctionContract.getPrice({'from': accounts[0]}).return_value
    newDutchAuctionContract.buy({'from': accounts[1]})
    #test correct transfer to new owner
    assert nft.ownerOf(12345).return_value == accounts[1]

    #test correct sum of money is in the buyer's account
    gas = accounts[1].gas_used
    assert accounts[1].balance().return_value == 50000 - price - gas

def test_fail_buy(newDutchAuctionContract, accounts):
    #not enough money sent with the transaction
    with brownie.reverts("Not enough money"):
        newDutchAuctionContract.buy({'from': accounts[2]})

    #too late because over the duration
    chain.sleep(101)
    with brownie.reverts("Too late"):
        newDutchAuctionContract.buy({'from': accounts[1]})