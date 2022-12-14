#version ^0.3.8
import pytest
import brownie
from web3.exceptions import ValidationError

DEFAULT_GAS = 100000

# . This runs before ALL tests
@pytest.fixture
def reimbursementContract(Reimbursement, ActiveUser, accounts):
    activeUserContract = ActiveUser.deploy(accounts[0], {'from':accounts[1]})
    activeUserContract.setCurrentGradYear(2022)
    activeUserContract.addUser(accounts[2])
    activeUserContract.setCurrentGradYear(2023)
    activeUserContract.addUser(accounts[3])
    return Reimbursement.deploy(activeUserContract, {'from': accounts[1]})


def _as_wei_value(base, conversion):
    if conversion == "wei":
        return base
    if conversion == "gwei":
        return base * (10 ** 9)
    return base * (10 ** 18)

def test_contractDeployment(reimbursementContract, accounts):
    assert reimbursementContract.getOwner() == accounts[1], "Contract creator should be owner"

def test_canDisable(reimbursementContract, accounts):
    ownerAccount = accounts[0]
    adminAccount = accounts[1]
    randomAccount = accounts[5] 

    with pytest.raises(Exception) as e_info:
        txn0 = reimbursementContract.setDisableContract(True, {'from':randomAccount})

    txn1 = reimbursementContract.setDisableContract(True, {'from':adminAccount})
    txn2 = reimbursementContract.setDisableContract(False, {'from':adminAccount})

    txn3 = reimbursementContract.setDisableContract(True, {'from':ownerAccount})
    txn4 = reimbursementContract.setDisableContract(False, {'from':ownerAccount})

def test_canReceiveMoney(reimbursementContract, accounts):
    depositAmount = 1
    accounts[0].transfer(reimbursementContract, depositAmount, gas_price=0)
    accounts[2].transfer(reimbursementContract, depositAmount, gas_price=0)
    assert reimbursementContract.balance() == (depositAmount * 2), "Contract should be able to receive money"

# @Notice Relies on 'canDisabled' 'canAddUser'
def test_canReimburseMoney(reimbursementContract, accounts):

    #non active user 2022 year
    nonActiveUser = accounts[2]

    #active user 2023 year
    targetReimbursementAccount = accounts[3]

    adminAccount = accounts[1]
    ownerAccount = accounts[0]

    # https://vyper.readthedocs.io/en/stable/built-in-functions.html?highlight=send#send
    # send uses wei value to send to the address
    txnGasPriceToRepay = _as_wei_value(800577, "gwei")
    depositAmount = _as_wei_value(0.01, "ether")
    accounts[0].transfer(reimbursementContract, depositAmount, gas_price=0)
    assert reimbursementContract.balance() == depositAmount, "Contract should have received eth"

    txn01 = reimbursementContract.setDisableContract(True, {'from':ownerAccount})

    with pytest.raises(Exception) as e_info:
        txn02 = reimbursementContract.reimburseGas(targetReimbursementAccount, {'from': targetReimbursementAccount, 'gas_price' : txnGasPriceToRepay, 'gas' : DEFAULT_GAS})
    assert reimbursementContract.balance() == depositAmount, "Contract should not reimburse when disabled"

    txn03 = reimbursementContract.setDisableContract(False, {'from':ownerAccount})
    txn1 = reimbursementContract.reimburseGas(targetReimbursementAccount, {'from': targetReimbursementAccount, 'gas_price' : txnGasPriceToRepay, 'gas' : DEFAULT_GAS})
    
    # Verify log is correct
    assert len(txn1.events) == 1, "Contract should log after reimbursement"
    assert txn1.events[0]['recipient'] == targetReimbursementAccount, "Contract should log user reimbursed"
    assert txn1.events[0]['amount'] == txnGasPriceToRepay, "Log event should track amount reimbursed"
    assert reimbursementContract.balance() == (depositAmount - txnGasPriceToRepay), "Contract should pay amount reimbursed"

# @Notice Relies on 'canAddUser', and 'canReimburseMoney'
def test_userHitMaxReimbursement(reimbursementContract, accounts):
    adminAccount = accounts[1]
    targetReimbursementAccount = accounts[3]

    # Test needs to make sure we can reimburse a 3 times and leaves buffer
    # 0.004 each txn + 0.0005 buffer
    WEI_REIMBURSEMENT_BUFFER_FROM_CONTRACT = _as_wei_value(0.0005, "ether")
    depositAmount = _as_wei_value(0.0125, "ether")
    txnGasPrice = _as_wei_value(4, "gwei")
    totalReimbursementAllowed = _as_wei_value(12, "gwei")

    # Add money, set grad year, and an active user
    accounts[0].transfer(reimbursementContract, depositAmount, gas_price=0)
    assert reimbursementContract.balance() == depositAmount, "Contract should have received eth"

    # Set how much wei we each user can be reimbursed
    setCapTxn = reimbursementContract.setUserIndividualWeiReimbursementCap(totalReimbursementAllowed, {'from': adminAccount, 'gas_price' : 0, 'gas' : DEFAULT_GAS})
    assert reimbursementContract.getUserInidividualWeiReimbursementCap() == totalReimbursementAllowed, "Should set per-user reimbursement cap"
    
    # Reimburse gas once of 'txnGasPrice' amount
    accountEth = targetReimbursementAccount.balance()
    txnReimb1 = reimbursementContract.reimburseGas(targetReimbursementAccount, {'from': targetReimbursementAccount, 'gas_price' : txnGasPrice, 'gas' : DEFAULT_GAS})
    assert reimbursementContract.balance() == (depositAmount - txnGasPrice), "Contract should have sent 1 txn of eth"
    assert txnReimb1.events[0]['amount'] == txnGasPrice, "Log event should track amount"
    assert reimbursementContract.balance() == (depositAmount - txnGasPrice), "Contract should have sent 1 txn of eth"
    
    # Reimburse gas one more time of 'txnGasPrice' amount
    txnReimb2 = reimbursementContract.reimburseGas(targetReimbursementAccount, {'from': targetReimbursementAccount, 'gas_price' : txnGasPrice, 'gas' : DEFAULT_GAS})
    assert reimbursementContract.balance() == (depositAmount - 2*txnGasPrice), "Contract should have sent 2 txns of eth"
    assert txnReimb2.events[0]['totalReimbursed'] == (txnGasPrice * 2), "Log event should track 2 reimburement amount"

    txnReimb3 = reimbursementContract.reimburseGas(targetReimbursementAccount, {'from': targetReimbursementAccount, 'gas_price' : txnGasPrice, 'gas' : DEFAULT_GAS})
    assert reimbursementContract.balance() == (depositAmount - (3*txnGasPrice)), "Contract should have sent eth"
    
    txnTooMuch = reimbursementContract.reimburseGas(targetReimbursementAccount, {'from': targetReimbursementAccount, 'gas_price' : txnGasPrice, 'gas' : DEFAULT_GAS})
    assert reimbursementContract.balance() == (depositAmount - (3*txnGasPrice)), "Contract should not reimburse any more"

def test_contractOutOfEth(reimbursementContract, accounts):
    adminAccount = accounts[1]
    targetReimbursementAccount = accounts[3]

    # Test needs to make sure we can reimburse a 3 times and leaves buffer
    # 0.004 each txn + 0.0005 buffer
    WEI_REIMBURSEMENT_BUFFER_FROM_CONTRACT = _as_wei_value(0.0005, "ether")
    depositAmount = WEI_REIMBURSEMENT_BUFFER_FROM_CONTRACT + _as_wei_value(8, "gwei")
    txnGasPrice = _as_wei_value(4, "gwei")
    totalReimbursementAllowed = _as_wei_value(12, "gwei")

    # Add money, set grad year, and an active user
    accounts[0].transfer(reimbursementContract, depositAmount, gas_price=0)
    assert reimbursementContract.balance() == depositAmount, "Contract should have received eth"

    # Set how much wei we each user can be reimbursed
    setCapTxn = reimbursementContract.setUserIndividualWeiReimbursementCap(totalReimbursementAllowed, {'from': adminAccount, 'gas_price' : 0, 'gas' : DEFAULT_GAS})
    assert reimbursementContract.getUserInidividualWeiReimbursementCap() == totalReimbursementAllowed, "Should set per-user reimbursement cap"
    
    # Reimburse gas once of 'txnGasPrice' amount
    accountEth = targetReimbursementAccount.balance()
    txnReimb1 = reimbursementContract.reimburseGas(targetReimbursementAccount, {'from': targetReimbursementAccount, 'gas_price' : txnGasPrice, 'gas' : DEFAULT_GAS})
    assert reimbursementContract.balance() == (depositAmount - txnGasPrice), "Contract should have sent 1 txn of eth"
    assert txnReimb1.events[0]['amount'] == txnGasPrice, "Log event should track amount"
    assert reimbursementContract.balance() == (depositAmount - txnGasPrice), "Contract should have sent 1 txn of eth"
    
    # Reimburse gas one more time of 'txnGasPrice' amount
    txnReimb2 = reimbursementContract.reimburseGas(targetReimbursementAccount, {'from': targetReimbursementAccount, 'gas_price' : txnGasPrice, 'gas' : DEFAULT_GAS})
    assert reimbursementContract.balance() == (depositAmount - 2*txnGasPrice), "Contract should have sent 2 txns of eth"
    assert txnReimb2.events[0]['totalReimbursed'] == (txnGasPrice * 2), "Log event should track 2 reimburement amount"

    txnTooMuch = reimbursementContract.reimburseGas(targetReimbursementAccount, {'from': targetReimbursementAccount, 'gas_price' : txnGasPrice, 'gas' : DEFAULT_GAS})
    assert txnTooMuch.events[0]['amountNotReimbursed'] == txnGasPrice, "Log event should track amount failed to send"
    assert reimbursementContract.balance() == WEI_REIMBURSEMENT_BUFFER_FROM_CONTRACT, "Contract should not reimburse any more"

# This test works and fails...
def test_willOnlyReimburseStudents(reimbursementContract, accounts):
    adminAccount = accounts[1]
    targetReimbursementAccount = accounts[4]

    # Test needs to make sure we can reimburse a 3 times and leaves buffer
    # 0.004 each txn + 0.0005 buffer
    WEI_REIMBURSEMENT_BUFFER_FROM_CONTRACT = _as_wei_value(0.0005, "ether")
    depositAmount = WEI_REIMBURSEMENT_BUFFER_FROM_CONTRACT + _as_wei_value(8, "gwei")
    txnGasPrice = _as_wei_value(4, "gwei")
    totalReimbursementAllowed = _as_wei_value(12, "gwei")

    # Add money, set grad year, and an active user
    accounts[0].transfer(reimbursementContract, depositAmount, gas_price=0)
    assert reimbursementContract.balance() == depositAmount, "Contract should have received eth"

    # Set how much wei we each user can be reimbursed
    setCapTxn = reimbursementContract.setUserIndividualWeiReimbursementCap(totalReimbursementAllowed, {'from': adminAccount, 'gas_price' : 0, 'gas' : DEFAULT_GAS})
    assert reimbursementContract.getUserInidividualWeiReimbursementCap() == totalReimbursementAllowed, "Should set per-user reimbursement cap"
    
    # Reimburse no gas to non-user
    accountEth = targetReimbursementAccount.balance()
    txnReimb1 = reimbursementContract.reimburseGas(adminAccount, {'from': targetReimbursementAccount, 'gas_price' : txnGasPrice, 'gas' : DEFAULT_GAS})
    assert reimbursementContract.balance() == (depositAmount), "Contract should have sent 1 txn of eth"
    assert len(txnReimb1.events) == 0, "Contract should not log when not reimbursing"

