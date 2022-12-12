import pytest
import brownie

@pytest.fixture
def DutchAuctionContract(privateGoodDutchAuction, accounts):
    return privateGoodDutchAuction.deploy(accounts[1], {'from': accounts[0]})

def test_endAuction(DutchAuctionContract, accounts):
    assert DutchAuctionContract.endDate != 0
    assert DutchAuctionContract.startDate != 0
    DutchAuctionContract.endAuction
    assert DutchAuctionContract.startDate == 0
    assert DutchAuctionContract.endDate == 0