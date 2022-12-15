# @version ^0.3.7

interface RandomNumber:
    def getRandomNumber(random:uint256) -> uint256: view


#TODO:
#figy out interface

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

@external
def __init__(_lottery_start:uint256, _lottery_length:uint256):
    self.lotteryStart = _lottery_start
    self.lotteryEnd = self.lotteryStart +_lottery_length
    assert block.timestamp < self.lotteryEnd, "Auction ended"

@external
@payable
def buyTickets():
    
    assert block.timestamp>=self.lotteryStart, "Lottery hasnt even begun..."
    assert block.timestamp<self.lotteryEnd, "Auction ended"
    assert msg.value > 1000000000000000, "Not enough moolah to enter, current entry price set at 0.001 wc"
    self.pot+=msg.value
    self.spentArr[self.ticketTotal] = msg.value
    self.ticketBuys[self.ticketTotal] = msg.sender
    self.ticketTotal = self.ticketTotal +1

  

@external
def endLottery():
    assert block.timestamp>=self.lotteryEnd, "Auction not ended"
    assert not self.ended, "Auction already ended"
    self.ended = True
    #Two important things for editor to keep in mind:
    #1. This lottery is not truly random
    #2. The pot doesnt work as originally intended, and needs to be integrated with 
    #   the other groups using pots and the true random method
    rand : uint256 = 3
    #rand : uint256 = getRandomNumber(ticketTotal)
    for i in self.spentArr:
        rand = rand - self.spentArr[i]
        if (rand <= 0):
                send(self.ticketBuys[i],self.pot*2/3)


