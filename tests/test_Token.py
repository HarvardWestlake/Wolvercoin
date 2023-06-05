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

@pytest.fixture
def activeUserContract(ActiveUser, accounts):
    activeUserContract = ActiveUser.deploy(
        accounts[0], # admin
        {'from': accounts[0]}
    )
    activeUserContract.setCurrentGradYear(2021, {'from': accounts[0]})
    return activeUserContract


def test_takeTenPercentNoTransfers(erc20Contract):
    #assert erc20Contract.takeTenPercent().return_value == 0
    #assert str(erc20Contract.totalOfTransactions()) == "0"
    return

def test_takeTenPercent(erc20Contract, accounts):
    senderAccount = accounts[5]
    erc20Contract.mint(accounts[0], 100)
    erc20Contract.approve(senderAccount, 20, {"from": accounts[0]})
    erc20Contract.approve(senderAccount, 20, {"from": accounts[1]})
    erc20Contract.approve(senderAccount, 20, {"from": accounts[2]})
    erc20Contract.transferFrom(accounts[0], accounts[1], 10, {"from": senderAccount})
    erc20Contract.transferFrom(accounts[1], accounts[2], 5, {"from": senderAccount})
    erc20Contract.transferFrom(accounts[2], accounts[3], 5, {"from": senderAccount})
    #assert erc20Contract.takeTenPercent().return_value == 2
    #assert str(erc20Contract.totalOfTransactions()) == "18"

def test_setActiveUserContract(erc20Contract, activeUserContract, accounts):
    erc20Contract.setActiveUserContract(activeUserContract.address, {"from": accounts[0]})
    assert erc20Contract.active_user_contract() == activeUserContract.address
    
 
def test_bulkMintUniqueAmount(erc20Contract, activeUserContract, accounts):
    erc20Contract.setActiveUserContract(activeUserContract.address, {"from": accounts[0]})
    erc20Contract.bulkMintUniqueAmount([accounts[2], accounts[3]], [100, 200], {"from": accounts[0]})
    assert erc20Contract.balanceOf(accounts[2]) == 100
    assert erc20Contract.balanceOf(accounts[3]) == 200

def test_bulkMintFailures(erc20Contract, activeUserContract, accounts):
    erc20Contract.setActiveUserContract(activeUserContract, {"from": accounts[0]})
    with pytest.raises(Exception) as e_info:
        erc20Contract.bulkMintUniqueAmount([accounts[2], accounts[3]], [100, 200, 300], {"from": accounts[1]})
    with pytest.raises(Exception) as e_info:
        erc20Contract.bulkMintUniqueAmount([accounts[2], accounts[3]], [100, 200], {"from": accounts[2]})
