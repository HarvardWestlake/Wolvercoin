import pytest
import brownie
from web3.exceptions import ValidationError

# . This runs before ALL tests
@pytest.fixture
def crashContract(crash, accounts):
    return Crash.deploy()

@external
def test_placeBet(gambler: address, amount: uint256)

@external
def test_withdrawBet(gambler: address)
