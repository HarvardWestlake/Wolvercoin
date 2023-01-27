#version ^0.3.8
import pytest
import brownie
from brownie import chain

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
def activeUserContract(ActiveUser, accounts):
    return ActiveUser.deploy(
        accounts[0], # admin
        {'from': accounts[0]}
    )

@pytest.fixture
def erc721Contract(NFT, activeUserContract, accounts):
    return NFT.deploy(
        activeUserContract,
        12345, # password
        {'from': accounts[0]}
    )

@pytest.fixture
def dutchAuctionContract(DutchAuction, erc20Contract, erc721Contract, activeUserContract, accounts):
    return DutchAuction.deploy(
        erc20Contract,
        erc721Contract,
        activeUserContract,
        {'from': accounts[0]}
    )

def test_create_auction_item(dutchAuctionContract, erc20Contract, erc721Contract, activeUserContract, accounts):
    admin = accounts[0]
    creator = accounts[1]

    activeUserContract.addAdmin(creator, {'from': admin})
    activeUserContract.whitelistContract(dutchAuctionContract, {'from': admin})

    mintResult = erc721Contract.mint(erc721Contract, "https://example.com?doubledate", {'from': admin})
    mintedTokenId = mintResult.events["Transfer"]["tokenId"]
    assert dutchAuctionContract.createAuctionItem(
        25, # Start price
        5, # End price
        chain.time() + 10000, # Start time
        chain.time() + 20000, # End time
        mintedTokenId, # Token ID
        "Smoke Sesh with Top T", # Name
        {'from': creator}
    )

def test_create_auction_item(dutchAuctionContract, erc20Contract, erc721Contract, activeUserContract, accounts):
    admin = accounts[0]
    creator = accounts[1]

    activeUserContract.addAdmin(creator, {'from': admin})
    activeUserContract.whitelistContract(dutchAuctionContract, {'from': admin})

    mintResult = erc721Contract.mint(erc721Contract, "https://example.com?doubledate", {'from': admin})
    mintedTokenId = mintResult.events["Transfer"]["tokenId"]
    assert dutchAuctionContract.createAuctionItem(
        25, # Start price
        5, # End price
        chain.time() + 10000, # Start time
        chain.time() + 20000, # End time
        mintedTokenId, # Token ID
        "Smoke Sesh with Top T", # Name
        {'from': creator}
    )

def test_getters(dutchAuctionContract, erc20Contract, erc721Contract, activeUserContract, accounts):
    admin = accounts[0]
    creator = accounts[1]

    activeUserContract.addAdmin(creator, {'from': admin})
    activeUserContract.whitelistContract(dutchAuctionContract, {'from': admin})

    mintResult = erc721Contract.mint(erc721Contract, "https://example.com?fieldtrip", {'from': admin})
    mintedTokenId = mintResult.events["Transfer"]["tokenId"]
    startTime = chain.time() + 10000
    endTime = chain.time() + 20000
    assert dutchAuctionContract.createAuctionItem(
        25, # Start price
        5, # End price
        startTime, # Start time
        endTime, # End time
        mintedTokenId, # Token ID
        "Smoke Sesh with Top T", # Name
        {'from': creator}
    )
    assert dutchAuctionContract.getActiveAuctionItems({'from': creator}) == [mintedTokenId]
    assert dutchAuctionContract.getSeller(mintedTokenId, {'from': creator}) == creator
    assert dutchAuctionContract.getStartDate(mintedTokenId, {'from': creator}) == startTime
    assert dutchAuctionContract.getEndDate(mintedTokenId, {'from': creator}) == endTime
    assert dutchAuctionContract.getStartPrice(mintedTokenId, {'from': creator}) == 25
    assert dutchAuctionContract.getEndPrice(mintedTokenId, {'from': creator}) == 5
    assert dutchAuctionContract.getName(mintedTokenId, {'from': creator}) == "Smoke Sesh with Top T"

def test_get_price(dutchAuctionContract, erc20Contract, erc721Contract, activeUserContract, accounts):
    admin = accounts[0]
    creator = accounts[1]

    activeUserContract.addAdmin(creator, {'from': admin})
    activeUserContract.whitelistContract(dutchAuctionContract, {'from': admin})

    mintResult = erc721Contract.mint(erc721Contract, "https://example.com?chocolate", {'from': admin})
    mintedTokenId = mintResult.events["Transfer"]["tokenId"]
    assert dutchAuctionContract.createAuctionItem(
        420, # Start price
        220, # End price
        chain.time() + 10000, # Start time
        chain.time() + 20000, # End time
        mintedTokenId, # Token ID
        "Smoke Sesh with Top T", # Name
        {'from': creator}
    )
    chain.sleep(10000)
    assert abs(dutchAuctionContract.getPrice(mintedTokenId).return_value - 420) < 2 # Get difference and ABS to account for slow code
    chain.sleep(5000)
    assert abs(dutchAuctionContract.getPrice(mintedTokenId).return_value - 320) < 2
    chain.sleep(5000)
    assert abs(dutchAuctionContract.getPrice(mintedTokenId).return_value - 220) < 2

def test_buy(dutchAuctionContract, erc20Contract, erc721Contract, activeUserContract, accounts):
    admin = accounts[0]
    creator = accounts[1]
    donator = accounts[2]

    activeUserContract.addAdmin(creator, {'from': admin})
    activeUserContract.whitelistContract(dutchAuctionContract, {'from': admin})

    mintResult = erc721Contract.mint(erc721Contract, "https://example.com?smokesesh", {'from': admin})
    mintedTokenId = mintResult.events["Transfer"]["tokenId"]
    assert dutchAuctionContract.createAuctionItem(
        420, # Start price
        220, # End price
        chain.time() + 10000, # Start time
        chain.time() + 20000, # End time
        mintedTokenId, # Token ID
        "Smoke Sesh with Top T", # Name
        {'from': creator}
    )
    chain.sleep(15000)
    price = dutchAuctionContract.getPrice(mintedTokenId).return_value

    assert erc20Contract.mint(donator, 69420, {'from': admin}) # Supply the account with some token
    assert str(erc20Contract.getBalanceOf(donator)) == "69420"
    assert erc20Contract.approve(dutchAuctionContract.address, 69420, {'from': donator}) # Approve expenditure
    assert str(erc20Contract.getApprovedAmountOf(donator, dutchAuctionContract.address).return_value) == "69420"

    assert dutchAuctionContract.buy(mintedTokenId, {'from': donator})

    newBalance = int(erc20Contract.getBalanceOf(donator))
    assert abs(69420 - newBalance - price) < 2

    assert erc721Contract.ownerOf(mintedTokenId) == donator
