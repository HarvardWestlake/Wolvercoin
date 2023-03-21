#version ^0.3.8

# Henry Ullendorff

import pytest
import brownie
from web3.exceptions import ValidationError

DEFAULT_GAS = 100000

haikuSubmission = "An old silent pond\n A frog jumps into the pond—\n Splash! Silence again."
haikuSubmission2 = "An old silent dog\n A cat jumps into a pond—\n Splash! Silence again."
haikuSubmission3 = "Refrigerator\n A cat jumps into a pond—\n Splash! Silence again."

# . This runs before ALL tests
@pytest.fixture


def submithaikuContract (SubmitHaiku, accounts):
    return SubmitHaiku.deploy (accounts[0], {'from': accounts[0]})

# checks that one haiku can be submitted and gotten
def test_canSubmitHaiku (submithaikuContract, accounts):
    submithaikuContract.submitHaiku(accounts[0], haikuSubmission, {'from': accounts[0]})
    assert submithaikuContract.getHaiku (accounts[0], {'from': accounts[0]}) == "An old silent pond\n A frog jumps into the pond—\n Splash! Silence again.", "Haiku in HashMap should match with the corresponding submitted haiku"

# checks that a user can override their previous haiku with a new one
def test_canReplaceHaiku (submithaikuContract, accounts):
    submithaikuContract.submitHaiku(accounts[0], haikuSubmission2, {'from': accounts[0]})
    assert submithaikuContract.getHaiku (accounts[0], {'from': accounts[0]}) == "An old silent dog\n A cat jumps into a pond—\n Splash! Silence again.", "Haiku in HashMap should match with the corresponding submitted haiku"


def submithaikuContract2 (SubmitHaiku, accounts):
    return SubmitHaiku.deploy (accounts[1], {'from': accounts[1]}) 

# checks that two haikus from two different users can coexist
def test_twoHaikus (submithaikuContract, accounts):
    submithaikuContract2.submitHaiku(accounts[1], haikuSubmission3, {'from': accounts[1]})
    assert submithaikuContract2.getHaiku (accounts[1], {'from': accounts[1]}) == "Refrigerator\n A cat jumps into a pond—\n Splash! Silence again.", "second user's haiku was not submitted correctly"
    assert submithaikuContract.getHaiku (accounts[0], {'from': accounts[0]}) == "An old silent dog\n A cat jumps into a pond—\n Splash! Silence again.", "Haiku in HashMap should match with the corresponding submitted haiku"
