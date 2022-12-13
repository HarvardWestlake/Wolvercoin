# @version ^0.3.7
justCrashed: public(bool)
crashBets: public(HashMap[address, uint256])
multiplier: public(uint256)
pot: public(address)
currentBettors: public(DynArray[address, 1024])

interface ActiveUser:
    def getActiveUser(potentialUser: address) -> bool: view
    def getAdmin(potentialAdmin: address) -> bool: view

interface Token:
    def generate_random_number(maxVal: uint256) -> uint256: view

interface Wolvercoin:
    def transferFrom(_from : address, _to : address, _value : uint256) -> bool: payable

activeUserAddress: public(ActiveUser)
tokenContract: public(Token)
wolvercoinContract: public(Wolvercoin)

event CrashStart:
    time: uint256
    blockNumber: uint256

event BetWithdrawn:
    multiplied: uint256
    amountPaid: uint256
    recipient: address

event CrashUpdated:
    currentMultiple: uint256

event Crash:
    multiple: uint256

@external
def __init__(activeUserAddress: address, tokenContractAddress: address, wolvercoinContractAddress: address):
    self.pot = msg.sender
    self.justCrashed = False
    log CrashStart(block.timestamp, block.number)
    self.activeUserAddress = ActiveUser(activeUserAddress)
    self.tokenContract = Token(tokenContractAddress)
    self.wolvercoinContract = Wolvercoin(wolvercoinContractAddress)
    self.crashGamble()

@payable
@external
def withdrawBet(gambler: address):
    assert self.activeUserAddress.getActiveUser(gambler) == True
    
    paid: uint256 = (self.crashBets[gambler] * (self.multiplier / 10))

    self.wolvercoinContract.transferFrom (self.pot, gambler, paid)

    log BetWithdrawn(self.multiplier, paid, gambler)

@external
def updateCrash():
    if (self.justCrashed):
        self.resetCrash()
    else:
        self.crashGamble()

@internal
def resetCrash():
    self.justCrashed = False
    log Crash(self.multiplier)
    self.multiplier = 0

    #sets all the remaining bettors in the HashMap's bets to 0
    for i in self.currentBettors:
        self.crashBets[i] = 0

@external
def getMultiplier() -> uint256:
    return self.multiplier

#--DELETE THIS LATER--
#Dummy method - Will is coding this
@internal
def crashGamble():
    self.multiplier = self.multiplier+1
    #Will, log CrashUpdating in crashGamble