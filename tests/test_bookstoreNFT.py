#version ^0.3.8
import pytest
import brownie

@pytest.fixture
def BookstorenNFTContract (Bookstore, accounts):
    return BookstoreNFT.deploy(accounts[1], {'from': accounts[0]})


def add_HashMap():
    createBoundNFT(account[1],"pooopie")
    assert hashie.addr == account[1]