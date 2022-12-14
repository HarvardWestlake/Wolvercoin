#version ^0.3.8
import pytest
import brownie
from web3.exceptions import ValidationError

@pytest.fixture
def utilitiesContract (Utilities, accounts): #accounts is bc someone needs to pay for contract
    return Utilities.deploy ({'from':accounts[0]})

def test_redeemProduct(utilitiesContract, accounts):
    assert utilitiesContract.redeemProduct(2).return_value == False, "Should be a null address"

