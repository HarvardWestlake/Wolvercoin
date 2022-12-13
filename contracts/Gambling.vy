# @version ^0.3.7
justCrashed: public(bool)
crashBets: public(HashMap[address, uint256])
multiplier: public(uint256)
pot: public(address)

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
    log CrashStart(block.timestamp, block.number)

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
    
    # . Need to figure out how to clear the HashMap of all of its entries
    #self.crashBets.clear()

@external
def getMultiplier() -> uint256:
    return self.multiplier

@internal
def crashGamble():
    return