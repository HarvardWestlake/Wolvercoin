#version ^0.3.8

# Henry Ullendorff

import pytest
import brownie
from web3.exceptions import ValidationError

DEFAULT_GAS = 100000

# . This runs before ALL tests
@pytest.fixture

def submithaikuContract (SubmitHaiku, accounts):
    return SubmitHaiku.deploy (accounts[0], {'from': accounts[0]})

haikuSubmission = "An old silent pond\n A frog jumps into the pond—\n Splash! Silence again."

def test_canSubmitHaiku (submithaikuContract, haikuSubmission, accounts):
    submithaikuContract.submitHaiku (accounts[0], haikuSubmission, {'from': accounts[0]})
    assert submithaikuContract.getHaiku (accounts[0], {'from': accounts[0]}).equals ("An old silent pond\n A frog jumps into the pond—\n Splash! Silence again."), "Haiku in HashMap should match with the corresponding submitted haiku"
