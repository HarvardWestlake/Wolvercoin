# @version ^0.3.3

electedOfficials: public(DynArray [address, 3])
moneyStored: public(uint256)

@external
def __init__ ():
    self.moneyStored = 0
    self.electedOfficials = []

@external
def addMoney (amount: uint256):
    self.moneyStored = self.moneyStored + amount

@external
def setElectedOfficials (newEleectedOfficials: DynArray [address,3]):
    self.electedOfficials = newEleectedOfficials

@external
def getMoney() -> uint256:
    return self.moneyStored

@external
def getElectedOfficials() -> DynArray[address, 3]:
    return self.electedOfficials