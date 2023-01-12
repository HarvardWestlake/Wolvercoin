# @version 0.3.6

import pytest
from brownie import accounts
from web3.exceptions import ValidationError
from brownie.network.state import Chain

chain = Chain()

@pytest.fixture
#def test_take10Percent()
def test_deposit10Percent(tester,testProvider):
    preBank=tester.balanceOf[tester.bank]
    preProvider=tester.balanceOf[testProvider]
    tester.deposit10Percent(testProvider)    
    postBank=tester.balanceOf[tester.bank]
    postProvider=tester.balanceOf[testProvider]
    assert postBank==preBank-tester.totalOfTransactions*.1 and postProvider==preProvider+tester.totalOfTransactions*.1, "successfully invested 10%"