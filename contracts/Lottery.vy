# @version ^0.3.7



# vyper.interfaces.ERC20 does not include the mint and burn functions so we make our own interface
interface Token:
    def getBalanceOf(_address: address) -> uint256: nonpayable
    def transferFrom(_from : address, _to : address, _value : uint256) -> bool: nonpayable
    def approve(_spender : address, _value : uint256) -> bool: nonpayable

#TODO:
#figy out interface/randomness

lotteryStart:public(uint256)
lotteryEnd:public(uint256)

#keep track of the order of bid purchases
ticketBuys: public(DynArray[address, 1])

#keep track of how much is spent by each
spentArr: public(DynArray[uint256, 1])

#send an email to swacziarg@gmail.com please I will respond
ticketTotal:public(uint256)
pot: public(uint256)

ended:public(bool)

erc20: Token # The main contract we need to interact with

@external
def __init__(_lottery_start:uint256, _lottery_length:uint256,erc20address: address):
    self.erc20 = Token(erc20address)
    self.lotteryStart = _lottery_start
    self.lotteryEnd = self.lotteryStart +_lottery_length
    assert block.timestamp < self.lotteryEnd, "Auction ended"

@external
@payable
def buyTickets(amount:uint256):
    # h: uint256 = amount +1
    assert block.timestamp>=self.lotteryStart, "Lottery hasnt even begun..."
    assert block.timestamp<self.lotteryEnd, "Auction ended"
    assert amount > 0, "Not enough WC, current entry price set at 1 WC"
    assert self.erc20.getBalanceOf(msg.sender) >= amount, "Not enough money in account"
    assert self.erc20.transferFrom(msg.sender, self, amount), "Transfer failed"

    self.pot+=amount
    self.spentArr.append(amount) 
    self.ticketBuys.append(msg.sender)
    self.ticketTotal = self.ticketTotal +1
    if (amount == 5):
        self.endLotto()

@external
def getLotteryStart()->uint256:
    return self.lotteryStart

@external
def getLotteryLen()->uint256:
    return self.lotteryEnd - self.lotteryStart

@external
def hasEnded()->bool:
    return self.ended

@external
def setStartingPot(amount:uint256):
    self.pot = amount

@external
def getPot()->uint256:
    return self.pot
    
@internal
def endLotto():
    self.ended = True
    rand : uint256 = 0
    bol : bool = False
    rand = block.timestamp*block.difficulty%self.pot
    #rand : uint256 = getRandomNumber(ticketTotal)
    for i in self.spentArr:
        rand-=1
        if (rand <= 0 and bol == False):
            bol = True
            assert self.erc20.transferFrom(self, self.ticketBuys[i], self.pot*2/3), "Transfer failed"

@external
def endLottery():
    assert block.timestamp>=self.lotteryEnd, "Auction not ended"
    assert not self.ended, "Auction already ended"
    self.ended = True
    rand : uint256 = 0
    bol : bool = False
    rand = block.timestamp*block.difficulty%self.pot
    #rand : uint256 = getRandomNumber(ticketTotal)
    for i in self.spentArr:
        rand-=1
        if (rand <= 0 and bol == False):
            bol = True
            assert self.erc20.transferFrom(self, self.ticketBuys.pop(), self.pot*2/3), "Transfer failed"
            



