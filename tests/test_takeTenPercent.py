# @version ^0.3.7
import pytest
import brownie
from web3.exceptions import ValidationError

@pytest.fixture
def investingContract(Investing, Wolvercoin, accounts):
     wolvercoinContract = Wolvercoin.deploy("Wolvercoin", "WVC", 10, 10000000, {'from': accounts[0]})
     investingContract = Investing.deploy(wolvercoinContract)

def test_takeTenPercent(Investing, Wolvercoin, accounts):
    wolvercoinContract.mint(accounts[0], 100)
    wolvercoinContract.transferFrom(accounts[0], accounts[1], 10)
    wolvercoinContract.transferFrom(accounts[1], accounts[2], 5)
    wolvercoinContract.transferFrom(accounts[2], accounts[3], 5)
    assert investingContract.takeTenPercent() == 2
    assert investingContract.totalOfTransactions == 18

def test_takeTenPercentNoTransfers(Investing, Wolvercoin, accounts):
    assert investingContract.takeTenPercent() == 0
    assert investingContract.totalOfTransactions == 0

