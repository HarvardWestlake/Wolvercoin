#version ^0.3.8
import pytest
import brownie

@pytest.fixture
def BookstoreNFTContract (BookstoreNFT, accounts):
    return BookstoreNFT.deploy({'from':accounts[0]})

def add_HashMap():
    createBoundNFT(account[1],"pooopie")
    assert hashie.addr == account[1]

def test_redeemProduct(BookstoreNFTContract, accounts):
    assert BookstoreNFTContract.redeemProduct(2).return_value == False, "Should be a null address"
