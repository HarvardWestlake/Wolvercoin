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

def test_cantRemoveNonAdmin(activeUserContract, accounts):  
    assert activeUserContract.getIsAdmin(accounts[3]) == False, "User should not be admin before test"
    with pytest.raises(Exception) as e_info:
        activeUserContract.removeAdmin(accounts[3],  {'from': accounts[0]})

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
    assert activeUserContract.getIsActiveUser(accounts[4]) == True, "Should be active user"

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

def test_addBulkUsers(activeUserContract, accounts):
    activeUserContract.setCurrentGradYear(2023)
    activeUserContract.addBulkUsers([accounts[7], accounts[8], accounts[9]],  {'from': accounts[1]})
    assert activeUserContract.getUserGradYear(accounts[7]) == 2023, "Should get user grad year"
    assert activeUserContract.getUserGradYear(accounts[8]) == 2023, "Should get user grad year"
    assert activeUserContract.getUserGradYear(accounts[9]) == 2023, "Should get user grad year"

def test_getIsAdminAndActiveUser(activeUserContract, accounts):
    assert activeUserContract.getIsAdminAndActiveUser(accounts[0]) == True, "Should be admin and active user"
    assert activeUserContract.getIsAdminAndActiveUser(accounts[1]) == True, "Should be admin and active user"
    assert activeUserContract.getIsAdminAndActiveUser(accounts[2]) == False, "Should not be admin and active user"

def test_isContractWhitelisted(activeUserContract, accounts):
    contract = accounts[6]
    assert activeUserContract.isContractWhitelisted(contract) == False
    activeUserContract.whitelistContract(contract, {'from': accounts[0]})
    assert activeUserContract.isContractWhitelisted(contract) == True

def test_getIsActiveUser(activeUserContract, accounts):
    assert activeUserContract.getIsActiveUser(accounts[0]) == False, "Should be active user"
    assert activeUserContract.getIsActiveUser(accounts[1]) == False, "Should be active user"
    assert activeUserContract.getIsAdmin(accounts[1]) == True, "Should be admin"
    assert activeUserContract.getIsActiveUser(accounts[2]) == False, "Should not be active user"

def test_getIsActiveUserWithNonActiveUser(activeUserContract, accounts):
    assert activeUserContract.getIsActiveUser(accounts[9]) == False, "Should not be active user"

def test_getIsActiveUserDoesntExist(activeUserContract, accounts):
    assert activeUserContract.getIsActiveUser(accounts[3]) == False, "Should not be active user"

def test_getIsAdminAndActiveUser(activeUserContract, accounts):
    assert activeUserContract.getIsAdminAndActiveUser(accounts[0]) == False, "Should be admin and active user"
    assert activeUserContract.getIsAdmin(accounts[1]) == True, "Should be admin"
    assert activeUserContract.getIsAdminAndActiveUser(accounts[1]) == False, "Should be admin and active user"
    assert activeUserContract.getIsAdminAndActiveUser(accounts[2]) == False, "Should not be admin and active user"


def test_setOwner(activeUserContract, accounts):
    ownerAccount = accounts[0]
    adminAccount = accounts[1]
    randomAccount = accounts[5] 

    with pytest.raises(Exception) as e_info:
        activeUserContract.setOwner(randomAccount, {'from':adminAccount})

    activeUserContract.setOwner(randomAccount, {'from':ownerAccount})
    assert activeUserContract.getOwner() == randomAccount

def test_contractDisabled(activeUserContract, accounts):
    ownerAccount = accounts[0]
    randomAccount = accounts[5] 

    activeUserContract.setDisableContract(True, {'from':ownerAccount})
    with pytest.raises(Exception) as e_info:
        activeUserContract.addUser(randomAccount,  {'from': accounts[1]})
    with pytest.raises(Exception) as e_info:
        activeUserContract.addAdmin(randomAccount,  {'from': accounts[1]})
    with pytest.raises(Exception) as e_info:
        activeUserContract.removeAdmin(randomAccount,  {'from': accounts[1]})
    with pytest.raises(Exception) as e_info:
        activeUserContract.whilteListContract(activeUserContract,  {'from': accounts[1]})
    with pytest.raises(Exception) as e_info:
        activeUserContract.setCurrentGradYear(42069,  {'from': accounts[1]})
    with pytest.raises(Exception) as e_info:
        activeUserContract.addBulkUsers([randomAccount],  {'from': accounts[1]})
    with pytest.raises(Exception) as e_info:
        activeUserContract.whitelistContract(randomAccount,  {'from': accounts[1]})

def test_allEmptyAddresses(activeUserContract, accounts):
    with pytest.raises(Exception) as e_info:
        activeUserContract.addAdmin("0x0000000000000000000000000000000000000000",  {'from': accounts[1]})
    with pytest.raises(Exception) as e_info:
        activeUserContract.addUser("0x0000000000000000000000000000000000000000",  {'from': accounts[1]})
    with pytest.raises(Exception) as e_info:
        activeUserContract.removeAdmin("0x0000000000000000000000000000000000000000",  {'from': accounts[1]})
    with pytest.raises(Exception) as e_info:
        activeUserContract.whitelistContract("0x0000000000000000000000000000000000000000",  {'from': accounts[1]})

def test_allNotAsAdmin(activeUserContract, accounts):
    assert activeUserContract.getIsAdminAndActiveUser(accounts[3]) == False, "User should not be admin before test"
    with pytest.raises(Exception) as e_info:
        activeUserContract.addAdmin(accounts[1],  {'from': accounts[3]})
    with pytest.raises(Exception) as e_info:
        activeUserContract.addUser(accounts[1],  {'from': accounts[3]})
    with pytest.raises(Exception) as e_info:
        activeUserContract.removeAdmin(accounts[1],  {'from': accounts[3]})
    with pytest.raises(Exception) as e_info:
        activeUserContract.whitelistContract(accounts[1],  {'from': accounts[3]})

def test_addIsNotAdminOrOwner(activeUserContract, accounts):
    assert activeUserContract.getIsAdmin(accounts[3]) == False, "User should not be admin before test"
    with pytest.raises(Exception) as e_info:
        activeUserContract.setCurrentGradYear(2000,  {'from': accounts[3]})
    with pytest.raises(Exception) as e_info:
        activeUserContract.addBulkUsers([accounts[3]],  {'from': accounts[3]})

def test_getContractWhitelisted(activeUserContract, accounts):
    contract = accounts[6]
    assert activeUserContract.getContractWhitelisted(contract) == False
    activeUserContract.whitelistContract(contract, {'from': accounts[0]})
    assert activeUserContract.getContractWhitelisted(contract) == True
