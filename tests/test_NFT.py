import pytest
import brownie
from web3.exceptions import ValidationError

DEFAULT_GAS = 100000

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
        {'from': accounts[3]}
    )


def testBurn_BalanceOf_Mint(erc721Contract, accounts):
    mintResult = erc721Contract.mint(accounts[3], "https://example.com?ricepurity", {'from': accounts[3]})
    mintedTokenId = mintResult.events["Transfer"]["tokenId"]
    erc721Contract.burn(mintedTokenId,{'from': accounts[3]})

    assert erc721Contract.balanceOf(accounts[3]) == 0

 


