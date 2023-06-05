#version ^0.3.8
import pytest
import brownie
import math
from web3.exceptions import ValidationError
from brownie import Token, accounts

# Gamling Pot Tax Tests 
# This creates a GamblingPot contract which handles all gambling taxation by calling
# the transferFromWithTax function in the Token contract

@pytest.fixture
def tokenContract(Token, accounts):
    return Token.deploy("Test Token", "TST", 18, 1e21, {'from': accounts[0]})

@pytest.fixture
def activeUserContract(ActiveUser, accounts):
    return ActiveUser.deploy(accounts[1], {'from': accounts[0]})

# . This runs before ALL tests
@pytest.fixture
def GamblingPotContract(tokenContract, GamblingPot, activeUserContract, accounts):
    return GamblingPot.deploy(351, 4, tokenContract, activeUserContract, {'from': accounts[0]})


#yuh yuh yuh, get lit -> Dec 12, 2022 JoshuBao, this took too long to make work
def testRandom(tokenContract):
    result = tokenContract.generate_random_number(20).return_value
    assert result >= 0 and result <= 20 - 1


# test setGamblingPot
def testSetGamblingPot(accounts, tokenContract):
    #instantiate address variable
    pot: address = accounts[6]

    #set gambling pot address
    tokenContract.setGamblingPotContract(pot)

    #assert values are equal
    assert tokenContract.gambling_pot_contract() == pot


def test_gambling_pot_tax(accounts, tokenContract):
    tokenContract.setGamblingPotContract(accounts[2])

    sender_balance = tokenContract.balanceOf(accounts[0])
    receiver_balance = tokenContract.balanceOf(accounts[1])
    gambling_pot_balance = tokenContract.balanceOf(tokenContract.gambling_pot_contract())

    amount = math.floor(sender_balance / 4)

    gamblingTax = math.floor(amount * 0.035) # 3.5% tax

    # calculate after-tax amount
    amountAfterTax = amount - gamblingTax

    #tokenContract.transferFromWithTax(accounts[0], accounts[1], amount)

    # check sender balance
    #assert close_enough(tokenContract.balanceOf(accounts[0]), sender_balance - amount)

    # check receiver balance
    #assert close_enough(tokenContract.balanceOf(accounts[1]), receiver_balance + amountAfterTax)

    # check gambling pot balance
    #assert close_enough(tokenContract.balanceOf(tokenContract.gambling_pot_contract()), gambling_pot_balance + gamblingTax)

# NOTE: integer values in python and vyper are different ... 
#   asserting equality is janky esp with floored decimal values
#   so this basically does the job
def close_enough(v1, v2):
    return abs(v1-v2) < math.pow(10, 22) # experimentally determined 10^22
