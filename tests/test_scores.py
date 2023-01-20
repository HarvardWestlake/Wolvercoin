# @version ^0.3.7
import pytest
import brownie

@pytest.fixture
def CodeScoreCheck(CodeScoreCheck, accounts):
    return CodeScoreCheck.deploy(accounts[0], {'from': accounts[1]})

def test_returnScore(CodeScoreCheck, accounts):
    assert CodeScoreCheck.getHighScore().return_value == 72
    assert CodeScoreCheck.compareHighScores(accounts[0], 50).return_value == "You did not beat Mr. Theiss."
    assert CodeScoreCheck.compareHighScores(accounts[1], 75).return_value == "You beat Mr. Theiss! Epic Gamer Moment!"
    assert CodeScoreCheck.compareHighScores(accounts[1], 75).return_value == "You cannot beat Mr. Theiss more than once."