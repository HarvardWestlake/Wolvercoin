# @dev Basic testing for the voting system
# @author Evan Stokdyk (@Focus172)

# @version 0.3.7
import pytest
import brownie
from web3.exceptions import ValidationError

DEFAULT_GAS = 100000

# . This runs before ALL tests
@pytest.fixture
def votingContract(VotingAndRep, accounts):
    return VotingAndRep.deploy({'from': accounts[0]})

def _as_wei_value(base, conversion):
    if conversion == "wei":
        return base
    if conversion == "gwei":
        return base * (10 ** 9)
    return base * (10 ** 18)

def test_contractDeployment(votingContract, accounts):
    assert votingContract.voteDuration != 0, "Voting Period Should be initialized"

def test_proposeVote(votingContract, accounts):   
#     assert reimbursementContract.getAdmin(accounts[3]) == False, "User should not be admin before test"
#     reimbursementContract.addAdmin(accounts[3],  {'from': accounts[0]})
#     assert reimbursementContract.getAdmin(accounts[3]) == True, "Contract constructor should add an single admin"

# def test_canSetGradYear(reimbursementContract, accounts):
#     txn1 = reimbursementContract.setCurrentGradYear(2023)
#     assert len(txn1.events) == 1, "Should log when grad year is set"
#     assert reimbursementContract.currentGradYear() == 2023, "Should set grad year"

# def test_canAddUser(reimbursementContract, accounts):
#     reimbursementContract.setCurrentGradYear(2023)
#     reimbursementContract.addUser(accounts[4],  {'from': accounts[1]})
#     assert reimbursementContract.getUserGradYear(accounts[4]) == 2023, "Should set user grad year"

# def test_canDisable(reimbursementContract, accounts):
#     ownerAccount = accounts[0]
#     adminAccount = accounts[1]
#     randomAccount = accounts[5] 

#     with pytest.raises(Exception) as e_info:
#         txn0 = reimbursementContract.setDisableContract(True, {'from':adminAccount})

#     with pytest.raises(Exception) as e_info:
#         txn1 = reimbursementContract.setDisableContract(True, {'from':randomAccount})

#     txn2 = reimbursementContract.setDisableContract(True, {'from':ownerAccount})
#     txn3 = reimbursementContract.setDisableContract(False, {'from':ownerAccount})

# def test_canReceiveMoney(reimbursementContract, accounts):
#     depositAmount = 1
#     accounts[0].transfer(reimbursementContract, depositAmount, gas_price=0)
#     accounts[2].transfer(reimbursementContract, depositAmount, gas_price=0)
#     assert reimbursementContract.balance() == (depositAmount * 2), "Contract should be able to receive money"

# # @Notice Relies on 'canDisabled' 'canAddUser'
# def test_canReimburseMoney(reimbursementContract, accounts):
#     # Add money, set grad year, and an active user
#     targetReimbursementAccount = accounts[4]
#     adminAccount = accounts[1]
#     ownerAccount = accounts[0]
#     # https://vyper.readthedocs.io/en/stable/built-in-functions.html?highlight=send#send
#     # send uses wei value to send to the address
#     txnGasPriceToRepay = _as_wei_value(800577, "gwei")
#     depositAmount = _as_wei_value(0.01, "ether")
#     accounts[0].transfer(reimbursementContract, depositAmount, gas_price=0)
#     assert reimbursementContract.balance() == depositAmount, "Contract should have received eth"

#     reimbursementContract.setCurrentGradYear(2023)
#     reimbursementContract.addUser(targetReimbursementAccount,  {'from': adminAccount})
#     assert reimbursementContract.getUserGradYear(targetReimbursementAccount) == 2023, "Should set user grad year"

#     txn01 = reimbursementContract.setDisableContract(True, {'from':ownerAccount})

#     with pytest.raises(Exception) as e_info:
#         txn02 = reimbursementContract.reimburseGas(targetReimbursementAccount, {'from': targetReimbursementAccount, 'gas_price' : txnGasPriceToRepay, 'gas' : DEFAULT_GAS})
#     assert reimbursementContract.balance() == depositAmount, "Contract should not reimburse when disabled"

#     txn03 = reimbursementContract.setDisableContract(False, {'from':ownerAccount})
#     txn1 = reimbursementContract.reimburseGas(targetReimbursementAccount, {'from': targetReimbursementAccount, 'gas_price' : txnGasPriceToRepay, 'gas' : DEFAULT_GAS})
    
#     # Verify log is correct
#     assert len(txn1.events) == 1, "Contract should log after reimbursement"
#     assert txn1.events[0]['recipient'] == targetReimbursementAccount, "Contract should log user reimbursed"
#     assert txn1.events[0]['amount'] == txnGasPriceToRepay, "Log event should track amount reimbursed"
#     assert reimbursementContract.balance() == (depositAmount - txnGasPriceToRepay), "Contract should pay amount reimbursed"