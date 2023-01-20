#version ^0.3.8
import pytest
import brownie
from web3.exceptions import ValidationError

DEFAULT_GAS = 100000

# . This runs before ALL tests
@pytest.fixture
def activeUserContract(ActiveUser, accounts):
    return ActiveUser.deploy(accounts[1], {'from': accounts[0]})

def test_contractDeployment(activeUserContract, accounts):
    assert activeUserContract.getIsAdmin(accounts[0]) == True, "Contract creator should be a admin"
    assert activeUserContract.getIsAdmin(accounts[1]) == True, "Contract constructor should enter a single admin"
    assert activeUserContract.getIsAdmin(accounts[2]) == False, "Random accounts should not be admins"

def test_canAddAdmin(activeUserContract, accounts):   
    assert activeUserContract.getIsAdmin(accounts[3]) == False, "User should not be admin before test"
    activeUserContract.addAdmin(accounts[3],  {'from': accounts[0]})
    assert activeUserContract.getIsAdmin(accounts[3]) == True, "Contract constructor should add an single admin"

def test_canRemoveAdmin(activeUserContract, accounts):  
    activeUserContract.addAdmin(accounts[3],  {'from': accounts[0]}) 
    assert activeUserContract.getIsAdmin(accounts[3]) == True, "User should be admin before test"
    activeUserContract.removeAdmin(accounts[3],  {'from': accounts[0]})
    assert activeUserContract.getIsAdmin(accounts[3]) == False, "Contract constructor should remove a single admin"

def test_canSetGradYear(activeUserContract, accounts):
    txn1 = activeUserContract.setCurrentGradYear(2023)
    assert len(txn1.events) == 1, "Should log when grad year is set"
    assert activeUserContract.currentGradYear() == 2023, "Should set grad year"

def test_canGetCurrentGradYear(activeUserContract, accounts):
    txn1 = activeUserContract.setCurrentGradYear(2023)
    assert len(txn1.events) == 1, "Should log when grad year is set"
    assert activeUserContract.getCurrentGradYear() == 2023, "Should set grad year"
    txn1 = activeUserContract.setCurrentGradYear(2024)
    assert activeUserContract.getCurrentGradYear() == 2024, "Should set grad year"

def test_canAddUser(activeUserContract, accounts):
    activeUserContract.setCurrentGradYear(2023)
    activeUserContract.addUser(accounts[4],  {'from': accounts[1]})
    assert activeUserContract.getUserGradYear(accounts[4]) == 2023, "Should set user grad year"

def test_isAlumni(activeUserContract, accounts):
    activeUserContract.setCurrentGradYear(2023)
    activeUserContract.addUser(accounts[4],  {'from': accounts[1]})
    activeUserContract.setCurrentGradYear(2024)
    assert activeUserContract.getIsAlumni(accounts[4], {'from': accounts[1]}), "is alum"
    assert activeUserContract.getIsAlumni(accounts[3], {'from': accounts[1]}) == False, "not alum"

def test_canDisable(activeUserContract, accounts):
    ownerAccount = accounts[0]
    adminAccount = accounts[1]
    randomAccount = accounts[5] 

    with pytest.raises(Exception) as e_info:
        txn0 = activeUserContract.setDisableContract(True, {'from':adminAccount})

    with pytest.raises(Exception) as e_info:
        txn1 = activeUserContract.setDisableContract(True, {'from':randomAccount})

    txn2 = activeUserContract.setDisableContract(True, {'from':ownerAccount})
    txn3 = activeUserContract.setDisableContract(False, {'from':ownerAccount})

def test_whitelistContract(activeUserContract, accounts):
    contract = accounts[6]
    assert activeUserContract.isContractWhitelisted(contract) == False
    activeUserContract.whitelistContract(contract, {'from': accounts[0]})
    assert activeUserContract.isContractWhitelisted(contract) == True
