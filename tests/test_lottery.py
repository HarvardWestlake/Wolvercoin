
# @dev Basic testing for the lotto system
# @author Simon W
import pytest
import brownie
LStart = 100
LLength = 100000000000000

@pytest.fixture
def erc20Contract(Token, accounts):
    return Token.deploy(
        "Wolvercoin", # _name
        "WVC", # _symbol
        18, # _decimals
        1000, # _supply
        {'from': accounts[0]}
    )
    
@pytest.fixture
def lotteryContract(Lottery,erc20Contract,accounts):
    yield Lottery.deploy(LStart,LLength, erc20Contract,{'from':accounts[0]})

def test_setPot(lotteryContract):
    assert lotteryContract.setStartingPot(50)
    assert lotteryContract.pot() == 50
    
def test_initial_state(lotteryContract):
    assert lotteryContract.lotteryStart() == LStart, "Start wrong" 
    assert lotteryContract.lotteryEnd() == LLength+LStart, "End wrong"

# def test_buy(lotteryContract,erc20Contract,accounts):
#     buyer = accounts[4]
#     admin = accounts[0]
#     assert erc20Contract.mint(buyer, 69420, {'from': admin}), "Didnt mint"
#     assert lotteryContract.buyTickets(5,{'from': buyer}), "Didnt buy"
#     assert str(erc20Contract.getBalanceOf(buyer).return_value) == "69415", "Balance didnt update"
    
# def test_end(lotteryContract):
#     assert lotteryContract.hasEnded() == True
    
    