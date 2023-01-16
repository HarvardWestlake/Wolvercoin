#version ^0.3.8
import pytest
from brownie import accounts

@pytest.fixture
def contractAddresses(CommunityPot, ActiveUser, Token, accounts):
    activeUserContract = ActiveUser.deploy(accounts[1], {'from': accounts[0]})
    tokenContract = Token.deploy("Wolvercoin", "WVC", 18, 2000, {'from': accounts[0]})
    communityPotContract = CommunityPot.deploy(tokenContract, activeUserContract, {'from': accounts[0]})
    return [communityPotContract, tokenContract, activeUserContract]

def test_getMoneyStored(contractAddresses, accounts):
    communityPotContract = contractAddresses[0]
    tokenContract = contractAddresses[1]
    _ = contractAddresses[2]

    assert communityPotContract.getMoneyStored().return_value == 0, "Initialize money to zero"

    # accounts[0] is the minter of the token address
    tokenContract.transfer(communityPotContract, 10, {'from': accounts[0]})
    assert communityPotContract.getMoneyStored().return_value == 10, "Donated money should be reflected in pot"

def test_addElectedOfficial(contractAddresses, accounts):
    communityPotContract = contractAddresses[0]
    tokenContract = contractAddresses[1]
    _ = contractAddresses[2]

    # current officials: []
    assert communityPotContract.isAdmin(accounts[8]).return_value == False, "Admins should not contain every user"

    # owner of active user contract is accounts[0]
    communityPotContract.addElectedOfficial(accounts[7], {'from': accounts[0]})
    assert communityPotContract.isAdmin(accounts[7]).return_value == True, "Should be able to add admin"
    assert communityPotContract.isAdmin(accounts[8]).return_value == False, "Adding an admin shouldn't change others status"

def test_transact(contractAddresses, accounts):
    communityPotContract = contractAddresses[0]
    tokenContract = contractAddresses[1]
    _ = contractAddresses[2]

    initalAccountBalence = tokenContract.getBalanceOf(accounts[3])

    tokenContract.transfer(communityPotContract, 10, {'from': accounts[0]})
    communityPotContract.addElectedOfficial(accounts[5], {'from': accounts[0]})

    communityPotContract.transact(2, accounts[3], {'from': accounts[5]})
    assert tokenContract.getBalanceOf(accounts[3]) == initalAccountBalence + 2

    try:
        stopBadtransfer = False
        communityPotContract.transfer(4, accounts[0], {'from': accounts[9]})
    except:
        stopBadtransfer = True
    assert stopBadtransfer, "contract should stop non admins from transacting"
