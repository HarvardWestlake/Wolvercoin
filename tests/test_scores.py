# @version ^0.3.7
import pytest
import brownie

@pytest.fixture
def compareContract(CodeScoreCheck, accounts):
    return CodeScoreCheck.deploy(2700, accounts[0], {'from': accounts[1]})

def returnScore(compareContract, accounts):
    assert compareContract.getHighScore()