#version ^0.3.8


import pytest
from brownie import accounts
from web3.exceptions import ValidationError
from brownie.network.state import Chain



@pytest.fixture
# Test the random_number_generator() function
def test_random_number_generator():
    # Generate a random number
    num = random_number_generator()

    # Verify that the number is between 1 and 100
    assert 1 <= num <= 100