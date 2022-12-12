# @version ^0.3.7

interface ActiveUser:
    def getActiveUser(potentialUser: address) -> bool: view

interface Token:
    generate_random_number(maxVal: uint256) -> uint256:
    transferFrom(_from : address, _to : address, _value : uint256) -> bool: payable

justCrashed: public(bool)
crashBets: public(HashMap[address, uint256])
multiplier: public(uint256)
pot: public(address)
tokenContract: Token(_name: String[32], _symbol: String[32], _decimals: uint8, _supply: uint256, _gamblingPot: address):
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
    self.activeUserContract = ActiveUser(activeUserAddress)
    self.tokenContract = Token("Wolvercoin", "WVC", 10, 10000000)

@payable
@external
def withdrawBet(gambler: address):
    assert(self.activeUserAddress.getActiveUser(gambling) == true)
    
    paid: uint256 = (self.crashBets[gambler] * (self.multiplier / 10))

    self.tokenContract.transferFrom (self.pot, gambler, paid)

    log BetWithdrawn(self.multiplier, paid, gambler)