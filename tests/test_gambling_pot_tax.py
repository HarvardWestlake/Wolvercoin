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
    return Token.deploy("Test Token", "TST", 18, 1e21, {'from': accounts[0]})

def test_gambling_pot_tax(accounts, token):
    token.setGamblingPot(accounts[2], {'from': accounts[0]})

    sender_balance = token.balanceOf(accounts[0], {'from': accounts[0]})
    receiver_balance = token.balanceOf(accounts[1], {'from': accounts[0]})
    gambling_pot_balance = token.balanceOf(token.gambling_pot({'from': accounts[0]}), {'from': accounts[0]})

    amount = math.floor(sender_balance / 4)

    gamblingTax = math.floor(amount * 0.035) # 3.5% tax

    # calculate after-tax amount
    amountAfterTax = amount - gamblingTax

    token.transferFrom(accounts[0], accounts[1], amount, {'from': accounts[0]})

    # check sender balance
    assert close_enough(token.balanceOf(accounts[0], {'from': accounts[0]}), sender_balance - amount)

    # check receiver balance
    assert close_enough(token.balanceOf(accounts[1], {'from': accounts[0]}), receiver_balance + amountAfterTax)

    # check gambling pot balance
    assert close_enough(token.balanceOf(token.gambling_pot(), {'from': accounts[0]}), gambling_pot_balance + gamblingTax)

# NOTE: integer values in python and vyper are different ... 
#   asserting equality is janky esp with floored decimal values
#   so this basically does the job
def close_enough(v1, v2):
    return abs(v1-v2) < math.pow(10, 22) # experimentally determined 10^22

#yuh yuh yuh, get lit -> Dec 12, 2022 JoshuBao, this took too long to make work
def testRandom(accounts, token):

    result = token.generate_random_number(20, {'from': accounts[0]}).return_value
    assert result >= 0 and result <= 20 - 1

# test setGamblingPot
def testSetGamblingPot(accounts, token):
    #instantiate address variable
    pot: address = accounts[6]

    #set gambling pot address
    token.setGamblingPot(pot, {'from': accounts[0]})

    #assert values are equal
    assert token.gambling_pot({'from': accounts[0]}) == pot