#version ^0.3.8

# @dev Basic testing for the voting system
# @author Evan Stokdyk (@Focus172)

import pytest
from brownie import accounts
from web3.exceptions import ValidationError
from brownie.network.state import Chain

chain = Chain()

# . This runs before ALL tests
@pytest.fixture
def privateGoodContract(privateGoodDutchAuction, ERC20, accounts):
    ERC20Contract = ERC20.deploy("str", "string", 8, 12, {'from':accounts[0]})
    return privateGoodDutchAuction.deploy(100, 100, 200, 0xb5E89dc549B070CdD51fc18F1072aE9eC6e7A7C2, ERC20Contract, {'from': accounts[0]})
    

def _as_wei_value(base, conversion):
    if conversion == "wei":
        return base
    if conversion == "gwei":
        return base * (10 ** 9)
    return base * (10 ** 18)

def test_endAuction(privateGoodContract, accounts):
    assert privateGoodContract.endDate != 0
    privateGoodContract.endAuction
    assert privateGoodContract.endDate == 0
