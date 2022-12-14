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

event CrashGambled:
    currentMultiple: uint256
    currentjustCrashed: bool

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
    #verifies that gambler has placed a bet
    assert self.activeUserContract.getActiveUser(gambler) == True
    found: bool = False
    for bettor in self.currentBettors:
        if (bettor == gambler):
            found = True
    assert (found == True)
    
    #calculates their return
    paid: uint256 = (self.crashBets[gambler] * (self.multiplier / 10))

    #transfers return from pot to gambler's address
    self.wolvercoinContract.transferFrom (self.pot, gambler, paid)

    log BetWithdrawn(self.multiplier, paid, gambler)

@nonpayable
@external
def crashGamble():
    self.crashGambleHelper(self.tokenContract.generate_random_number(1000))

#does all the work for crashGamble()
#did it this way so it could be tested easily
@nonpayable
@internal
def crashGambleHelper(random: uint256):
    crashed: bool = self.crashFromRandomNumber(random)
    if (crashed == True):
        self.justCrashed = True
    else:
        self.multiplier = self.multiplier + 1

    log CrashGambled(self.multiplier, self.justCrashed)

#takes number (between 0-1000) and returns true if its above 900 and false if <= 900
#this effectively generates true 10% of the time
@nonpayable
@internal
def crashFromRandomNumber(randomNumber: uint256) -> bool:
    if (randomNumber > 900):
        return True
    else:
        return False

@external
def getMultiplier() -> uint256:
    return self.multiplier

@external
def getJustCrashed() -> bool:
    return self.justCrashed

@external
def getCrashFromRandomNumber(useRandomNumber: uint256) -> bool:
    return self.crashFromRandomNumber(useRandomNumber)

@external
def getCrashGambleHelper(useRandomNumber: uint256):
    self.crashGambleHelper(useRandomNumber)
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