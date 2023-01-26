# @version ^0.3.7
justCrashed: public(bool)
crashBets: public(HashMap[address, uint256])
multiplier: public(uint256)
pot: public(address)
currentBettors: public(DynArray[address, 1024])

interface ActiveUser:
    def getIsActiveUser(potentialUser: address) -> bool: view
    def getIsAdmin(potentialAdmin: address) -> bool: view

interface Token:
    def generate_random_number(maxVal: uint256) -> uint256: view
    def transferFrom(_from : address, _to : address, _value : uint256) -> bool: payable
    def getBalanceOf (_user: address) -> uint256: view
<<<<<<< HEAD
=======

#interface Wolvercoin:
 #   def transferFrom(_from : address, _to : address, _value : uint256) -> bool: payable
  #  def getBalanceOf (_user: address) -> uint256: view
>>>>>>> code_Utilities

wolvercoinContract: public(Token)
activeUserContract: public(ActiveUser)

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
def __init__(activeUserAddress: address, wolvercoinContractAddress: address):
    self.pot = msg.sender
    self.justCrashed = False
    log CrashStart(block.timestamp, block.number)
    self.activeUserContract = ActiveUser(activeUserAddress)
    self.wolvercoinContract = Token(wolvercoinContractAddress)
    self.crashGamble()
<<<<<<< HEAD
    #init of codeGambling
    self.crashBets[msg.sender] = 0
    self.multiplier = 0
=======
    self.crashBets[msg.sender] = 0
    self.multiplier = 0

>>>>>>> code_Utilities

@payable
@external
def withdrawBet(gambler: address):
    #verifies that gambler has placed a bet
    assert self.activeUserContract.getIsActiveUser(gambler) == True
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


@nonpayable
@internal
def crashGamble():
    randomNum: uint256 = self.wolvercoinContract.generate_random_number(1000)
    #self.crashGambleHelper(randomNum)
    return

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
<<<<<<< HEAD
    
#methods from codeGambling.vy
@external 
def placeBets(gambler: address, amount: uint256):
    assert msg.sender == gambler
    assert self.justCrashed != False
    assert self.wolvercoinContract.getBalanceOf(msg.sender) > amount
    self.crashBets[gambler] = amount
=======

@external 
def placeBets(amount: uint256):
    #assert msg.sender == gambler #when would someone even be added in as a gambler? 
    assert self.justCrashed != True #only let this method run if it is true
    assert self.wolvercoinContract.getBalanceOf(msg.sender) > amount 
    self.crashBets[msg.sender] = amount
>>>>>>> code_Utilities
    #self.wolvercoinContract.transferFrom(gambler, self, amount)

@view
@external 
def getHashValue() -> uint256: 
<<<<<<< HEAD
    return self.crashBets[msg.sender] 
=======
    return self.crashBets[msg.sender]
>>>>>>> code_Utilities
