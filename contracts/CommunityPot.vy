# @version ^0.3.7

electedOfficials: dynArray [address, 3]
moneyStored: uint256

@external
def _init_ (initialElectedOfficials:  dynArray [address, 3]):
    moneyStored = 0
    electedOfficials = initialElectedOfficials

@external
def addMoney (amount: uint256):
    moneyStored = moneyStored + amount

@external
def setElectedOfficials (newEleectedOfficials: dynArray [address,3]):
    electedOfficials = newEleectedOfficials