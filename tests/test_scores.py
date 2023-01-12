# @version ^0.3.7
import pytest
import brownie

@pytest.fixture
def CodeScoreCheck(CodeScoreCheck, accounts):
    return CodeScoreCheck.deploy(accounts[0], {'from': accounts[1]})

def test_returnScore(CodeScoreCheck):
    assert CodeScoreCheck.getHighScore().return_value == 72