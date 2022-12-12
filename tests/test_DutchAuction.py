import pytest
import brownie

@pytest.fixture
def DutchAuctiontContract(privateGoodDutchAuction, accounts):
    return privateGoodDutchAuction.deploy(accounts[1], {'from': accounts[0]})