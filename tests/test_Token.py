#version ^0.3.7
import pytest
import brownie
from web3.exceptions import ValidationError

@pytest.fixture
def erc20Contract(Token, accounts):
    return Token.deploy(
        "Wolvercoin",
        "WVC",
        8,
        2000,
        {'from': accounts[0]}
    )

def test_mint(erc20Contract, accounts):
    initBalance: uint256 = erc20Contract.balanceOf(accounts[1])
    erc20Contract.mint(accounts[1], 100)
    assert erc20Contract.balanceOf(accounts[0]) == initBalance + 100

def test_burn(accounts, erc20Contract):
    initBalance: uint256 = erc20Contract.balanceOf(accounts[2])
    erc20Contract.mint(accounts[2], 100)
    senderAccount = accounts[2]
    erc20Contract.burn(50)
    assert erc20Contract.balanceOf(accounts[2]) == initBalance + 50

# def test_takeTenPercentNoTransfers(erc20Contract):
#     #assert erc20Contract.takeTenPercent().return_value == 0
#     #assert str(erc20Contract.totalOfTransactions()) == "0"
#     return

# def test_takeTenPercent(erc20Contract, accounts):
#     senderAccount = accounts[5]
#     erc20Contract.mint(accounts[0], 100)
#     erc20Contract.approve(senderAccount, 20, {"from": accounts[0]})
#     erc20Contract.approve(senderAccount, 20, {"from": accounts[1]})
#     erc20Contract.approve(senderAccount, 20, {"from": accounts[2]})
#     erc20Contract.transferFrom(accounts[0], accounts[1], 10, {"from": senderAccount})
#     erc20Contract.transferFrom(accounts[1], accounts[2], 5, {"from": senderAccount})
#     erc20Contract.transferFrom(accounts[2], accounts[3], 5, {"from": senderAccount})
#     #assert erc20Contract.takeTenPercent().return_value == 2
#     #assert str(erc20Contract.totalOfTransactions()) == "18"


