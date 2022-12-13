# @version ^0.3.7

interface ActiveUser:
    def getActiveUser(potentialUser: address) -> bool: view

interface Token:
    def generate_random_number(maxVal: uint256) -> uint256: view

interface Wolvercoin:
    def transferFrom(_from : address, _to : address, _value : uint256) -> bool: payable

justCrashed: public(bool)
crashBets: public(HashMap[address, uint256])
multiplier: public(uint256)
pot: public(address)

tokenContract: public(Token)
activeUserContract: public(ActiveUser)
wolvercoinContract: public(Wolvercoin)

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
def __init__(activeUserAddress: address, tokenContractAddress: address, wolvercoinContractAddress: address):
    self.pot = msg.sender
    log CrashStart(block.timestamp, block.number)
    self.activeUserContract = ActiveUser(activeUserAddress)
    self.tokenContract = Token(tokenContractAddress)
    self.wolvercoinContract = Wolvercoin(wolvercoinContractAddress)

@payable
@external
def withdrawBet(gambler: address):
    assert self.activeUserContract.getActiveUser(gambler) == True
    
    paid: uint256 = (self.crashBets[gambler] * (self.multiplier / 10))

    self.wolvercoinContract.transferFrom (self.pot, gambler, paid)

    log BetWithdrawn(self.multiplier, paid, gambler)