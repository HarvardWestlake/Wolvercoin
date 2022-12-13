# @version ^0.3.7
justCrashed: public(bool)
crashBets: public(HashMap[address, uint256])
multiplier: public(uint256)
pot: public(address)
currentBettors: public(DynArray[address, 1024])

interface ActiveUser:
    def getActiveUser(potentialUser: address) -> bool: view
    def getAdmin(potentialAdmin: address) -> bool: view

activeUserAddress: public(ActiveUser)

event Crash:
    multiple: uint256

event CrashStart:
    time: uint256
    blockNumber: uint256

@external
def __init__():
    self.pot = msg.sender
    self.justCrashed = False
    log CrashStart(block.timestamp, block.number)
    self.crashGamble()

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