#version ^0.3.8
import pytest
import brownie

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
def publicGoodsContract(PublicGoods, erc20Contract, erc721Contract, accounts):
    return PublicGoods.deploy(
        erc20Contract,
        erc721Contract,
        accounts[1]
        {'from': accounts[0]}
    )


def test_createGood(publicGoodsContract, erc20Contract, erc721Contract, accounts):
    creatorOfGood = accounts[5]
    donator = accounts[4]
    admin = accounts[0]

    mintResult = erc721Contract.mint(creatorOfGood, "https://example.com?ricepurity", {'from': admin})
    mintedTokenId = mintResult.events["Transfer"]["tokenId"]
    assert erc721Contract.approve(publicGoodsContract, mintedTokenId, {'from': creatorOfGood})

    assert publicGoodsContract.createGood(10, mintedTokenId, {'from': creatorOfGood}), "createGood failed"
    assert erc721Contract.ownerOf(mintedTokenId) == publicGoodsContract
    returnVal = publicGoodsContract.getGoal(mintedTokenId, {'from': creatorOfGood}).return_value
    assert str(returnVal) == "10", "getGoal returned wrong value"

def test_contribute(publicGoodsContract, erc20Contract, erc721Contract, accounts):
    creatorOfGood = accounts[5]
    donator = accounts[4]
    admin = accounts[0]

    mintResult = erc721Contract.mint(creatorOfGood, "https://example.com?ricepurity", {'from': admin})
    mintedTokenId = mintResult.events["Transfer"]["tokenId"]
    assert erc721Contract.approve(publicGoodsContract, mintedTokenId, {'from': creatorOfGood})

    # User starts with lots of eth in their account so no need to mint
    assert publicGoodsContract.createGood(10, mintedTokenId, {'from': creatorOfGood}), "createGood failed"

    assert erc20Contract.mint(donator, 69420, {'from': admin}) # Supply the account with some token
    assert str(erc20Contract.getBalanceOf(donator)) == "69420"
    
    assert erc20Contract.approve(publicGoodsContract.address, 69420, {'from': donator}) # Approve expenditure
    assert str(erc20Contract.getApprovedAmountOf(donator, publicGoodsContract.address).return_value) == "69420"
    
    assert publicGoodsContract.contribute(mintedTokenId, 3, {'from': donator}), "contribute failed"
    returnVal = publicGoodsContract.getContributionTotal(mintedTokenId, {'from': accounts[0]}).return_value
    assert str(returnVal) == "3", "getContributionTotal returned wrong value"
    assert str(erc20Contract.getBalanceOf(donator)) == str(69420 - 3)

    # 2nd contribution: make sure it adds, not creates a new entry
    assert publicGoodsContract.contribute(mintedTokenId, 5, {'from': donator}), "contribute failed"    
    returnVal = publicGoodsContract.getContributionTotal(mintedTokenId, {'from': accounts[0]}).return_value
    assert str(returnVal) == "8", "getContributionTotal returned wrong value"
    assert str(erc20Contract.getBalanceOf(donator)) == str(69420 - 8)

def test_retract(publicGoodsContract, erc20Contract, erc721Contract, accounts):
    creatorOfGood = accounts[5]
    donator = accounts[4]
    admin = accounts[0]

    mintResult = erc721Contract.mint(creatorOfGood, "https://example.com?ricepurity", {'from': admin})
    mintedTokenId = mintResult.events["Transfer"]["tokenId"]
    assert erc721Contract.approve(publicGoodsContract, mintedTokenId, {'from': creatorOfGood})

    assert publicGoodsContract.createGood(10, mintedTokenId, {'from': creatorOfGood}), "createGood failed"

    assert publicGoodsContract.retract(mintedTokenId, 1, {'from': donator}), "retract failed"

    assert erc20Contract.mint(donator, 69420, {'from': admin}) # Supply the account with some token
    assert str(erc20Contract.getBalanceOf(donator)) == "69420"

    assert erc20Contract.approve(publicGoodsContract.address, 69420, {'from': donator}) # Approve expenditure
    assert str(erc20Contract.getApprovedAmountOf(donator, publicGoodsContract.address).return_value) == "69420"

    assert publicGoodsContract.contribute(mintedTokenId, 3, {'from': donator}), "contribute failed"
    assert publicGoodsContract.retract(mintedTokenId, 1, {'from': donator}), "retract failed"

    #retract doesn't subtract from donator amount or total contributions
    assert str(erc20Contract.getBalanceOf(donator)) == str(69420 - 2)
    returnVal = publicGoodsContract.getContributionTotal(mintedTokenId, {'from': accounts[0]}).return_value
    assert str(returnVal) == "2", "getContributionTotal returned wrong value"

def test_complete_goal_achieved(publicGoodsContract, erc20Contract, erc721Contract, accounts):
    creatorOfGood = accounts[6]
    donator = accounts[7]
    admin = accounts[0]

    mintResult = erc721Contract.mint(creatorOfGood, "https://example.com?ricepurity", {'from': admin})
    mintedTokenId = mintResult.events["Transfer"]["tokenId"]
    assert erc721Contract.approve(publicGoodsContract, mintedTokenId, {'from': creatorOfGood})

    assert publicGoodsContract.createGood(10, mintedTokenId, {'from': creatorOfGood}), "createGood failed"

    assert erc20Contract.mint(donator, 69420, {'from': admin})
    assert str(erc20Contract.getBalanceOf(donator)) == "69420"
    
    assert erc20Contract.approve(publicGoodsContract.address, 69420, {'from': donator})
    assert str(erc20Contract.getApprovedAmountOf(donator, publicGoodsContract.address).return_value) == "69420"
    
    assert publicGoodsContract.contribute(mintedTokenId, 10, {'from': donator}), "contribute failed"
    
    returnVal = publicGoodsContract.getContributionTotal(mintedTokenId, {'from': accounts[0]}).return_value
    assert str(returnVal) == "10", "getContributionTotal returned wrong value"
    assert str(erc20Contract.getBalanceOf(donator)) == str(69420 - 10)

    assert publicGoodsContract.complete(mintedTokenId, {'from': creatorOfGood})
    assert str(erc20Contract.getBalanceOf(donator)) == str(69420 - 10)

def test_complete_goal_not_achieved(publicGoodsContract, erc20Contract, erc721Contract, accounts):
    creatorOfGood = accounts[6]
    donator = accounts[7]
    admin = accounts[0]

    mintResult = erc721Contract.mint(creatorOfGood, "https://example.com?ricepurity", {'from': admin})
    mintedTokenId = mintResult.events["Transfer"]["tokenId"]
    assert erc721Contract.approve(publicGoodsContract, mintedTokenId, {'from': creatorOfGood})

    assert publicGoodsContract.createGood(10, mintedTokenId, {'from': creatorOfGood}), "createGood failed"

    assert erc20Contract.mint(donator, 69420, {'from': admin})
    assert str(erc20Contract.getBalanceOf(donator)) == "69420"
    
    assert erc20Contract.approve(publicGoodsContract.address, 69420, {'from': donator})
    assert str(erc20Contract.getApprovedAmountOf(donator, publicGoodsContract.address).return_value) == "69420"
    
    assert publicGoodsContract.contribute(mintedTokenId, 3, {'from': donator}), "contribute failed"
    assert str(erc20Contract.getBalanceOf(donator)) == str(69420 - 3)
    
    returnVal = publicGoodsContract.getContributionTotal(mintedTokenId, {'from': accounts[0]}).return_value
    assert str(returnVal) == "3", "getContributionTotal returned wrong value"
    assert str(erc20Contract.getBalanceOf(donator)) == str(69420 - 3)

    assert publicGoodsContract.complete(mintedTokenId, {'from': creatorOfGood})
    assert str(erc20Contract.getBalanceOf(donator)) == "69420" # Make sure user got their money back
    assert erc721Contract.ownerOf(mintedTokenId) == creatorOfGood # Make sure creator got their NFT back

def test_getters(publicGoodsContract, erc20Contract, erc721Contract, accounts):
    creatorOfGood = accounts[6]
    donator = accounts[7]
    admin = accounts[0]

    mintResult = erc721Contract.mint(creatorOfGood, "https://example.com?ricepurity", {'from': admin})
    mintedTokenId = mintResult.events["Transfer"]["tokenId"]
    assert erc721Contract.approve(publicGoodsContract, mintedTokenId, {'from': creatorOfGood})

    assert publicGoodsContract.createGood(10, mintedTokenId, {'from': creatorOfGood}), "createGood failed"

    returnVal = publicGoodsContract.getActiveGoods({'from': accounts[0]}).return_value
    assert returnVal == [mintedTokenId], "getActiveGoods returned wrong value"

    assert publicGoodsContract.getContributionTotal(mintedTokenId, {'from': accounts[0]}).return_value == 0, "getContributionTotal returned wrong value"
    assert publicGoodsContract.getGoal(mintedTokenId, {'from': accounts[0]}).return_value == 10, "getContributionTotal returned wrong value"
    assert publicGoodsContract.getNumDonators(mintedTokenId, {'from': accounts[0]}).return_value == 0, "getContributionTotal returned wrong value"
    assert publicGoodsContract.getCreator(mintedTokenId, {'from': accounts[0]}).return_value == creatorOfGood, "getContributionTotal returned wrong value"
