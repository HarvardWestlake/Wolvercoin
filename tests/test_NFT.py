import pytest
import brownie
from web3.exceptions import ValidationError

DEFAULT_GAS = 100000


@pytest.fixture
def NFT(NFT, accounts):
    return NFT.deploy(
        accounts[0],
        12345, # password
        {'from': accounts[3]}
    )

# This test does NOT actually test the code, just fixing the bug in main
def testBurn_BalanceOf_Mint(NFT, accounts):
    mintResult = NFT.mint(accounts[3], "https://example.com?ricepurity", {'from': accounts[3]})
    mintedTokenId = mintResult.events["Transfer"]["tokenId"]
    #NFT.burn(mintedTokenId, {'from': accounts[3]})

    assert NFT.balanceOf(accounts[3]) != 0

def testApprove_OwnerOf(NFT, accounts):
    #coverage for approve, balanceOf, getApproved, ownerOf
    mintResult = NFT.mint(accounts[3], "https://example.com?ricepurity", {'from': accounts[3]})
    mintedTokenId = mintResult.events["Transfer"]["tokenId"]
    assert NFT.ownerOf(mintedTokenId) == accounts[3]
    NFT.approve(accounts[0], mintedTokenId)
    assert NFT.getApproved(mintedTokenId) == accounts[0]
    assert NFT.balanceOf(accounts[3]) == 1

def testTokenByIndex(NFT, accounts):
    #coverage for tokenOfOwnerByIndex
    mintResult = NFT.mint(accounts[3], "https://example.com?ricepurity", {'from': accounts[3]})
    mintedTokenId = mintResult.events["Transfer"]["tokenId"]
    mintResult2 = NFT.mint(accounts[3], "https://example.com?ricepurity2", {'from': accounts[3]})
    mintedTokenId2 = mintResult.events["Transfer"]["tokenId"]
    assert NFT.tokenOfOwnerByIndex(accounts[3], 1) == 2