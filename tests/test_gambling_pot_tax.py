#version ^0.3.8
import pytest
import brownie
import math
from web3.exceptions import ValidationError
from brownie import Token, accounts

DEFAULT_GAS = 100000

# . This runs before ALL tests
@pytest.fixture
def token(Token, accounts):
    # account[2] is our gambling pot address
    return Token.deploy("Test Token", "TST", 18, 1e21, accounts[2], {'from': accounts[0]})

def test_gambling_pot_tax(accounts, token):
    sender_balance = token.balanceOf(accounts[0])
    receiver_balance = token.balanceOf(accounts[1])
    gambling_pot_balance = token.balanceOf(accounts[2])

    amount = math.floor(sender_balance / 4)

    gamblingTax = math.floor(amount * 0.03500000000000000000000000000000000000) # 3.5% tax

    # calculate after-tax amount
    amountAfterTax = amount - gamblingTax

    token.transferFrom(accounts[0], accounts[1], amount)

    # check sender balance
    assert close_enough(token.balanceOf(accounts[0]), sender_balance - amount)

    # check receiver balance
    assert close_enough(token.balanceOf(accounts[1]), receiver_balance + amountAfterTax)

    # check gambling pot balance
    assert close_enough(token.balanceOf(accounts[2]), gambling_pot_balance + gamblingTax)

# NOTE: integer values in python and vyper are different ... 
#   asserting equality is janky esp with floored decimal values
#   so this basically does the job
def close_enough(v1, v2):
    return abs(v1-v2) < math.pow(10, 22) # experimentally determined 10^22