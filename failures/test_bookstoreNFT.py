#version ^0.3.8
import pytest
import brownie

@pytest.fixture
def BookstorenNFTContract (Bookstore, accounts):
    return BookstoreNFT.deploy(accounts[1], {'from': accounts[0]})


def add_HashMap():
    createBoundNFT(account[1],"pooopie")
    assert hashie.addr == account[1]

@pytest.fixture
def utilitiesContract (Utilities, accounts): #accounts is bc someone needs to pay for contract
    return Utilities.deploy ({'from':accounts[0]})

def test_redeemProduct(utilitiesContract, accounts):
    assert utilitiesContract.redeemProduct(2).return_value == False, "Should be a null address"
