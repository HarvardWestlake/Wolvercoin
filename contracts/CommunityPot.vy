# @version ^0.3.7
interface Token:
    def transferFrom(_from : address, _to : address, _value : uint256) -> bool: view
    def getBalanceOf(_user: address) -> uint256: view
TokenContract: public(Token)


electedOfficials: public(DynArray [address, 3])
moneyStored: public(uint256)
PotAddress: public(address)

@external
def __init__(thePotAddress: address, ERC20address: address):
    self.moneyStored = 0
    self.electedOfficials = []
    self.PotAddress=thePotAddress
    self.TokenContract=Token(ERC20address)


@external
def AddMoney(amount: uint256):
    assert amount>0
    self.moneyStored = self.moneyStored + amount

@internal
def removeMoney(amount: uint256):
    self.moneyStored = self.moneyStored - amount

@external
def SetElectedOfficials(newElectedOfficials: DynArray [address,3]):
    self.electedOfficials = newElectedOfficials
    

@view
@external
def getMoney() -> uint256: 
    return self.moneyStored

@view
@external
def getElectedOfficials() -> DynArray[address, 3]:
    return self.electedOfficials

@external
def Transact(amount: uint256, destAddress: address):
    assert self.TokenContract.getBalanceOf(self.PotAddress) >= amount
    self.TokenContract.transferFrom(self.PotAddress, destAddress, amount)
    self.removeMoney(amount)

#whether or not an address is in admin array
@view
@external
def VerifyElectedOfficial(wolvAddress: address) -> bool:
    for item in self.electedOfficials:
        if item==wolvAddress:
            return True
    return False

