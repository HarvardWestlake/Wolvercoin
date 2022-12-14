# @version ^0.3.7
import pytest
import brownie
from web3.exceptions import ValidationError

@pytest.fixture
def wolvercoinContract(Wolvercoin, accounts):
    return Wolvercoin.deploy(
        "Wolvercoin",
        "WVC",
        8,
        2000,
        {'from': accounts[0]}
    )

def test_takeTenPercentNoTransfers(wolvercoinContract):
    assert wolvercoinContract.takeTenPercent().return_value == 0
    assert str(wolvercoinContract.totalOfTransactions()) == "0"

def test_takeTenPercent(wolvercoinContract, accounts):
    senderAccount = accounts[5]
    wolvercoinContract.mint(accounts[0], 100)
    wolvercoinContract.approve(senderAccount, 20, {"from": accounts[0]})
    wolvercoinContract.approve(senderAccount, 20, {"from": accounts[1]})
    wolvercoinContract.approve(senderAccount, 20, {"from": accounts[2]})
    wolvercoinContract.transferFrom(accounts[0], accounts[1], 10, {"from": senderAccount})
    wolvercoinContract.transferFrom(accounts[1], accounts[2], 5, {"from": senderAccount})
    wolvercoinContract.transferFrom(accounts[2], accounts[3], 5, {"from": senderAccount})
    assert wolvercoinContract.takeTenPercent().return_value == 2
    assert str(wolvercoinContract.totalOfTransactions()) == "18"


