#version ^0.3.7

import pytest
from brownie import accounts
from web3.exceptions import ValidationError
from brownie.network.state import Chain

chain = Chain()

# . This runs before ALL tests
@pytest.fixture
def votingContract(SimpleAuction, accounts):
    return SimpleAuction.deploy({'from': accounts[0]})
