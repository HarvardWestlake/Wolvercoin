#version ^0.3.8
import brownie
import pytest

implements Wolvercoin:
def transfer(_to : address, _value : uint256) -> bool:

theissHighScore: uint256
users: HashMap[address, String[300]]

def __init__()
    return true


@external
def compareHighScores (unit256: newScore, address: name) -> String[100]:
    if users[name, newScore] == 0:
        if newScore > theissHighScore:
            transfer(name, 2.14*self.balanceOf[msg.sender])
            return "You beat Mr. Theiss! Epic Gamer Moment!"
        else:
            return "You did not beat Mr. Theiss."
    else
        return "You cannot beat Mr. Theiss more than once."

@external
def getHighScore() -> uint256:
    return theissHighScore

