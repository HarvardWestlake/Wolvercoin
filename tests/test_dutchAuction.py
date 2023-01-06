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
def erc721Contract(NFT, accounts):
    return NFT.deploy(
        12345, # password
        {'from': accounts[0]}
    )

@pytest.fixture
def dutchAuctionContract(DutchAuction, erc20Contract, erc721Contract, accounts):
    return DutchAuction.deploy(
        erc20Contract,
        erc721Contract,
        {'from': accounts[0]}
    )

def test_create_auction_item(dutchAuctionContract, erc20Contract, erc721Contract, accounts):
    admin = accounts[0]
    creator = accounts[1]

    mintResult = erc721Contract.mint(creator, "https://example.com?doubledate", {'from': admin})
    mintedTokenId = mintResult.events["Transfer"]["tokenId"]
    assert erc721Contract.approve(dutchAuctionContract, mintedTokenId, {'from': creator})
    assert dutchAuctionContract.createAuctionItem(
        "Double Date with Theiss and Sassie", # Name
        25, # Start price
        5, # End price
        chain.time() + 10000, # Start time
        chain.time() + 20000, # End time
        mintedTokenId, # Token ID
        {'from': creator}
    )

def test_create_auction_item(dutchAuctionContract, erc20Contract, erc721Contract, accounts):
    admin = accounts[0]
    creator = accounts[1]

    mintResult = erc721Contract.mint(creator, "https://example.com?doubledate", {'from': admin})
    mintedTokenId = mintResult.events["Transfer"]["tokenId"]
    assert erc721Contract.approve(dutchAuctionContract, mintedTokenId, {'from': creator})
    assert dutchAuctionContract.createAuctionItem(
        "Double Date with Theiss and Sassie", # Name
        25, # Start price
        5, # End price
        chain.time() + 10000, # Start time
        chain.time() + 20000, # End time
        mintedTokenId, # Token ID
        {'from': creator}
    )

def test_getters(dutchAuctionContract, erc20Contract, erc721Contract, accounts):
    admin = accounts[0]
    creator = accounts[1]

    mintResult = erc721Contract.mint(creator, "https://example.com?fieldtrip", {'from': admin})
    mintedTokenId = mintResult.events["Transfer"]["tokenId"]
    assert erc721Contract.approve(dutchAuctionContract, mintedTokenId, {'from': creator})
    startTime = chain.time() + 10000
    endTime = chain.time() + 20000
    assert dutchAuctionContract.createAuctionItem(
        "Field Trip to Bora Bora", # Name
        25, # Start price
        5, # End price
        startTime, # Start time
        endTime, # End time
        mintedTokenId, # Token ID
        {'from': creator}
    )
    assert dutchAuctionContract.getActiveAuctionItems({'from': creator}).return_value == ["Field Trip to Bora Bora"]
    assert dutchAuctionContract.getSeller("Field Trip to Bora Bora", {'from': creator}).return_value == creator
    assert dutchAuctionContract.getStartDate("Field Trip to Bora Bora", {'from': creator}).return_value == startTime
    assert dutchAuctionContract.getEndDate("Field Trip to Bora Bora", {'from': creator}).return_value == endTime
    assert dutchAuctionContract.getStartPrice("Field Trip to Bora Bora", {'from': creator}).return_value == 25
    assert dutchAuctionContract.getEndPrice("Field Trip to Bora Bora", {'from': creator}).return_value == 5
    assert dutchAuctionContract.getNFT("Field Trip to Bora Bora", {'from': creator}).return_value == mintedTokenId

def test_get_price(dutchAuctionContract, erc20Contract, erc721Contract, accounts):
    admin = accounts[0]
    creator = accounts[1]

    mintResult = erc721Contract.mint(creator, "https://example.com?chocolate", {'from': admin})
    mintedTokenId = mintResult.events["Transfer"]["tokenId"]
    assert erc721Contract.approve(dutchAuctionContract, mintedTokenId, {'from': creator})
    assert dutchAuctionContract.createAuctionItem(
        "Chocolate Tasting", # Name
        420, # Start price
        220, # End price
        chain.time() + 10000, # Start time
        chain.time() + 20000, # End time
        mintedTokenId, # Token ID
        {'from': creator}
    )
    chain.sleep(10000)
    assert abs(dutchAuctionContract.getPrice("Chocolate Tasting").return_value - 420) < 2 # Get difference and ABS to account for slow code
    chain.sleep(5000)
    assert abs(dutchAuctionContract.getPrice("Chocolate Tasting").return_value - 320) < 2
    chain.sleep(5000)
    assert abs(dutchAuctionContract.getPrice("Chocolate Tasting").return_value - 220) < 2

def test_buy(dutchAuctionContract, erc20Contract, erc721Contract, accounts):
    admin = accounts[0]
    creator = accounts[1]
    donator = accounts[2]

    mintResult = erc721Contract.mint(creator, "https://example.com?smokesesh", {'from': admin})
    mintedTokenId = mintResult.events["Transfer"]["tokenId"]
    assert erc721Contract.approve(dutchAuctionContract, mintedTokenId, {'from': creator})
    assert dutchAuctionContract.createAuctionItem(
        "Smoke Sesh with Top T", # Name
        420, # Start price
        220, # End price
        chain.time() + 10000, # Start time
        chain.time() + 20000, # End time
        mintedTokenId, # Token ID
        {'from': creator}
    )
    chain.sleep(15000)
    price = dutchAuctionContract.getPrice("Smoke Sesh with Top T").return_value

    assert erc20Contract.mint(donator, 69420, {'from': admin}) # Supply the account with some token
    assert str(erc20Contract.getBalanceOf(donator)) == "69420"
    assert erc20Contract.approve(dutchAuctionContract.address, 69420, {'from': donator}) # Approve expenditure
    assert str(erc20Contract.getApprovedAmountOf(donator, dutchAuctionContract.address).return_value) == "69420"

    assert dutchAuctionContract.buy("Smoke Sesh with Top T", {'from': donator})

    newBalance = int(erc20Contract.getBalanceOf(donator))
    assert abs(69420 - newBalance - price) < 2

    assert erc721Contract.ownerOf(mintedTokenId) == donator
