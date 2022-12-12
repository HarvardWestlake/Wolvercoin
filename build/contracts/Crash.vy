interface ActiveUser:
    def getActiveUser(potentialUser: address) -> bool: view

interface CFlip:
    def randomPrime() -> uint256: random

interface Wolvercoin:
    def transferFrom(_from : address, _to : address, _value : uint256) -> bool: payable

justCrashed: public(bool)
crashBets: public(HashMap[address, uint256])
multiplier: public(uint256)
pot: public(address)
CFLIP: immutable(CFlip)
wolvercoinContract: Wolvercoin
activeUserAddress: public(ActiveUser)

event BetWithdrawn:
    multiplied: uint256
    amountPaid: uint256
    recipient: address

event CrashUpdated:
    currentMultiple: uint256

event CrashStart:
    time: uint256
    blockNumber: uint256

@external
def __init__():
    self.pot = msg.sender
    log CrashStart(block.timestamp, block.number)

@payable
@external
def withdrawBet(gambler: address):
    assert(self.activeUserAddress.getActiveUser(gambling) == true)
    
    paid: uint256 = (self.crashBets[gambler] * (self.multiplier / 10))

    self.wolvercoinContract.transferFrom (self.pot, gambler, paid)

    log BetWithdrawn(self.multiplier, paid, gambler)