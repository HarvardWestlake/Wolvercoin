#version ^0.3.7

import pytest
from brownie import accounts
from web3.exceptions import ValidationError
from brownie.network.state import Chain

from datetime import datetime


chain = Chain()

@pytest.fixture
def tokenContract(Token, accounts):
    return Token.deploy(
        "Wolvercoin",
        "WVC",
        8,
        2000,
        {'from': accounts[0]}
    )

@pytest.fixture
def simpleAuctionContract(SimpleAuction, tokenContract, accounts):
    date= datetime.utcnow() - datetime(1970, 1, 1)
    seconds =(date.total_seconds())
    milliseconds = round(seconds*1000)
    return SimpleAuction.deploy(accounts[0], milliseconds, milliseconds+10000, tokenContract, 150, {'from': accounts[0]})

def _as_wei_value(base, conversion):
    if conversion == "wei":
        return base
    if conversion == "gwei":
        return base * (10 ** 9)
    return base * (10 ** 18)

def test_bid(simpleAuctionContract):
    simpleAuctionContract.bid(200)
    #assert simpleAuctionContract.highestBid> 100
    simpleAuctionContract.bid(300)
    #assert simpleAuctionContract.highestBid> 200
    
