# @dev Basic testing for the lotto system
# @author Simon W
from brownie.network.state import Chain
import pytest
import brownie
chain = Chain()

LStart = 100
LLength = 1000000000000000

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

def test_advanceTimeExample(erc20Contract, accounts):
    currentChainTime = chain.time()
    chain.sleep(10000)
    assert chain.time() == (currentChainTime + 10000)

def test_setPot(lotteryContract):
    assert lotteryContract.setStartingPot(50)
    assert lotteryContract.pot() == 50
    
def test_initial_state(lotteryContract):
    assert lotteryContract.lotteryStart() == LStart, "Start wrong" 
    assert lotteryContract.lotteryEnd() == LLength+LStart, "End wrong"

def test_lotteryFuncs(lotteryContract,erc20Contract,accounts):
    buyer = accounts[4]
    b1 = accounts[1]
    b2 = accounts[2]
    b3 = accounts[3]
    b4 = accounts[5]
    b5 = accounts[6]
    b6 = accounts[7]
    admin = accounts[0]
    assert erc20Contract.mint(b2, 6, {'from': admin}), "Didnt mint"
    assert erc20Contract.mint(b3, 6, {'from': admin}), "Didnt mint"
    assert erc20Contract.mint(b4, 6, {'from': admin}), "Didnt mint"
    assert erc20Contract.mint(b5, 6, {'from': admin}), "Didnt mint"
    assert erc20Contract.mint(b6, 6, {'from': admin}), "Didnt mint"
    assert erc20Contract.mint(b1, 6, {'from': admin}), "Didnt mint"
    assert erc20Contract.mint(buyer, 69420, {'from': admin}), "Didnt mint"
    assert erc20Contract.getBalanceOf(buyer) == 69420
    
    assert erc20Contract.getBalanceOf(b1) == 6
    assert erc20Contract.getBalanceOf(b2) == 6
    assert erc20Contract.getBalanceOf(b3) == 6
    assert erc20Contract.getBalanceOf(b4) == 6
    assert erc20Contract.getBalanceOf(b5) == 6
    assert erc20Contract.getBalanceOf(b6) == 6


    # Buy funcs
    assert lotteryContract.buyTickets(6, {'from': b1}), "Didnt buy"
    assert lotteryContract.buyTickets(6, {'from': b2}), "Didnt buy"
    assert lotteryContract.buyTickets(6, {'from': b6}), "Didnt buy"
    assert lotteryContract.buyTickets(6, {'from': b5}), "Didnt buy"
    assert lotteryContract.buyTickets(6, {'from': b4}), "Didnt buy"
    assert lotteryContract.buyTickets(6, {'from': b3}), "Didnt buy"
    assert lotteryContract.buyTickets(5, {'from': buyer}), "Didnt buy"
    assert lotteryContract.pot()==41
    assert lotteryContract.ticketTotal()==7
    chain.sleep(5000000000000000)
    assert lotteryContract.endLottery(),"Didnt end"


    # End of Lotto

    # assert str(erc20Contract.getBalanceOf(buyer)) == "69415", "Balance didnt update"
    assert lotteryContract.ended() == True,"end didnt work"
    
def test_lotteryEnd(lotteryContract,erc20Contract,accounts):
    buyer = accounts[8]
    admin = accounts[0]
    assert erc20Contract.mint(buyer, 5, {'from': admin}), "Didnt mint"
    assert erc20Contract.getBalanceOf(buyer) == 5
    assert lotteryContract.buyTickets(5, {'from': buyer}), "Didnt buy" 
    assert erc20Contract.getBalanceOf(buyer)==0
    chain.sleep(5000000000000000)
    assert lotteryContract.endLottery(),"Didnt end"
    assert lotteryContract.ended() == True,"end didnt work"
    assert erc20Contract.getBalanceOf(buyer) == 3


    

    
    