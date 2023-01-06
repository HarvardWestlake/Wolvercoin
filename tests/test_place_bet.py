# @version ^0.3.7

# @dev Basic testing for the voting system
# @author Evan Stokdyk (@Focus172)

import pytest
from brownie import accounts
from web3.exceptions import ValidationError
from brownie.network.state import Chain

chain = Chain()

# @dev basic testing for placeBet 
# @author Ava Weinrot 

@pytest.fixture
def erc20Contract(Token, accounts):
    return Token.deploy("wolvercoin", "wvc", 18, 1000,{'from': accounts[0]})

@pytest.fixture
def gamblingContract(erc20Contract, codeGambling, accounts):
    return codeGambling.deploy(accounts[1], erc20Contract, {'from': accounts[0]})

def test_placeBets(gamblingContract, erc20Contract, accounts):
    assert erc20Contract.approve(gamblingContract.address, 12, {'from': accounts[0]})
    gamblingContract.placeBets(accounts[0], 12,{'from': accounts[0]})
    assert gamblingContract.getHashValue() == 12