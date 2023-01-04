
#version ^0.3.8 
import pytest
import brownie

@pytest.fixture
def CommunityPotContract(CommunityPot, accounts):
    return CommunityPot.deploy(accounts[1], {'from': accounts[0]})

@pytest.fixture
def WolvercoinContract(Wolvercoin, accounts):
    return Wolvercoin.deploy("Wolvercoin", "WVC", 10, 100000000000, {'from': accounts[0]})


def test_contarct(CommunityPotContract, WolvercoinContract, accounts):
    with pytest.raises(Exception) as e_info:
        CommunityPotContract.VerifyAdmin(accounts[1])