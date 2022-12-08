#version ^0.3.8
import pytest
import brownie

DEFAULT_GAS = 100000

@pytest.fixture
def publicGoodsContract(PublicGoods, accounts):
    return PublicGoods.deploy({})

def test_createGood(publicGoodsContract, accounts):
    # TODO for @exoskeleton-1729
    raise NotImplementedError

def test_contribute(publicGoodsContract, accounts):
    # TODO for @stevenk8819
    raise NotImplementedError

def test_retract(publicGoodsContract, accounts):
    # TODO for @monkeymatt2023
    raise NotImplementedError

def test_complete(publicGoodsContract, accounts):
    # TODO for @ericyoondotcom
    raise NotImplementedError
