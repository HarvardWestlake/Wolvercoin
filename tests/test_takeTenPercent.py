#version ^0.3.7
import pytest
import brownie
from web3.exceptions import ValidationError

@pytest.fixture
def wolvercoinContract(Wolvercoin, takeTenPercent, accounts):
    wolvercoinContract = Wolvercoin.deploy("Wolvercoin", "WVC", 10, 10000000, {'from': accounts[0]})
    takeTenPercentContract = takeTenPercent.deploy(wolvercoinContract, {'from': accounts[0]})
@pytest.fixture
def takeTenPercentContract(wolvercoinContract, takeTenPercent, accounts):
    takeTenPercentContract = takeTenPercent.deploy(wolvercoinContract, {'from': accounts[0]})

def test_takeTenPercentNoTransfers(wolvercoinContract):
    assert  takeTenPercentContract.takeTenPercent() == 0
    assert  takeTenPercentContract.totalOfTransactions == 0

def test_takeTenPercent(wolvercoinContract, accounts):
    wolvercoinContract.mint(accounts[0], 100)
    wolvercoinContract.transferFrom(accounts[0], accounts[1], 10)
    wolvercoinContract.transferFrom(accounts[1], accounts[2], 5)
    wolvercoinContract.transferFrom(accounts[2], accounts[3], 5)
    assert  takeTenPercentContract.takeTenPercent() == 2
    assert  takeTenPercentContract.totalOfTransactions == 18


