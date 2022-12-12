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
def privateGoodContract(privateGoodDutchAuction, accounts):
    return privateGoodDutchAuction.deploy({'from': accounts[0]})
    

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