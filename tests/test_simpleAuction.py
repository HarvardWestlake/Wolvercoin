#version ^0.3.7

import pytest
from brownie import accounts
from web3.exceptions import ValidationError
from brownie.network.state import Chain

from datetime import datetime
DEFAULT_GAS = 100000


chain = Chain()

@pytest.fixture
def tokenContract(Token, accounts):
    return Token.deploy(
        "Wolvercoin", # _name
        "WVC", # _symbol
        18, # _decimals
        1000, # _supply
        {'from': accounts[0]}
    )

#@pytest.fixture
#def activeUserContract(ActiveUser, accounts):
#    return ActiveUser.deploy(
#        accounts[0], # admin
#        {'from': accounts[0]}
#    )

@pytest.fixture
def NFTContract(NFT, accounts):
    return NFT.deploy(
        12345, # password
        {'from': accounts[0]}
    )

@pytest.fixture
def simpleAuctionContract(SimpleAuction, tokenContract, NFTContract, accounts):
    return SimpleAuction.deploy(
        tokenContract,
        NFTContract,
        {'from': accounts[0]}
    )    


def test_auctionSimulation(simpleAuctionContract,tokenContract,NFTContract,accounts):
    admin = accounts[0]
    creator = accounts[1]
    ben = accounts[2] #beneficiary
    bidder = accounts[3]
    bidder2 = accounts[4]

    #activeUserContract.addAdmin(creator, {'from': admin})
    #activeUserContract.whitelistContract(simpleAuctionContract, {'from':admin})

    mintResult = NFTContract.mint(creator, "https://example.com?doubledate", {'from': admin})
    mintedTokenId = mintResult.events["Transfer"]["tokenId"]
    assert NFTContract.approve(simpleAuctionContract,mintedTokenId, {'from': creator})
    chain.sleep(15000)

    #Give accounts money; 30 and 40 
    assert tokenContract.mint(bidder, 30, {'from': admin}) 
    assert tokenContract.mint(bidder2, 40, {'from': admin})

    #Check accounts have money
    assert str(tokenContract.getBalanceOf(bidder)) == "30"
    assert str(tokenContract.getBalanceOf(bidder2)) == "40"

    #Approve accounts 
    assert tokenContract.approve(simpleAuctionContract.address, 30, {'from':bidder})
    assert tokenContract.approve(simpleAuctionContract.address, 40, {'from':bidder2})
    assert str(tokenContract.getApprovedAmountOf(bidder, simpleAuctionContract.address).return_value) =="30"
    assert str(tokenContract.getApprovedAmountOf(bidder2, simpleAuctionContract.address).return_value) =="40"

    #Bid #1
    assert simpleAuctionContract.bid(30, mintedTokenId, {'from': bidder})

    chain.sleep(1000)

    #Bid #2
    assert simpleAuctionContract.bid(40, mintedTokenId, {'from': bidder2})

    
    chain.sleep(5001)

    #End Auction
    assert simpleAuctionContract.endItemAuction(mintedTokenId)





