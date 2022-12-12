#version ^0.3.8
import pytest
import brownie
from web3.exceptions import ValidationError

DEFAULT_GAS = 100000

# . This runs before ALL tests
@pytest.fixture
def privateGoodDutchAuctionContract(privateGoodDutchAuction, accounts):
    return Reimbursement.deploy(accounts[1], {'from': accounts[0]})

def test_endAuction(privateGoodDutchAuction, accounts):
    assert privateGoodDutchAuctionContract.endDate != 0
    privateGoodDutchAuctionContract.endAuction()
    assert privateGoodDutchAuctionContract.endDate == 0