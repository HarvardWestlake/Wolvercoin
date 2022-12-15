
# @dev Basic testing for the lotto system
# @author Simon W
import pytest
import brownie
LStart = 100
LLength = 100000000000000

@pytest.fixture
def lottery_contract(Lottery,accounts):
    yield Lottery.deploy(LStart,LLength,{'from':accounts[0]})
def test_initial_state(lottery_contract):
    assert lottery_contract.lotteryStart() == LStart
    assert lottery_contract.lotteryLength() == LLength
def test_buy(lottery_contract,accounts):
    lottery_contract.buyTickets(50, {'from':accounts[0]})
    assert lottery_contract.pot >0
    assert lottery_contract.holders==1
def test_end(lottery_contract):
    assert lottery_contract.ended == True
    
    