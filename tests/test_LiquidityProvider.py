# @version ^0.3.7
import pytest
import brownie
from web3.exceptions import ValidationError

# . This runs before ALL tests
@pytest.fixture
def stakeContract(Stake, accounts):
    return Stake.deploy(accounts[1], {'from': accounts[0]})
    #I'm passing in accounts[1] as the bank address

@pytest.fixture
def WolvercoinContract(Wolvercoin, accounts):
    return Wolvercoin.deploy("Wolvercoin", "WVC", 10, 10000000, {'from': accounts[0]})

def test_takeTenPercent(LiquidityProvider, totalOfTransactions):
    temp: unit256 = totalOfTransactions
    takeTenPercent()
    assert totalOfTransactions = temp/10