# @version ^0.3.7
interface ERC20:
    def transferFromNoTax(_from : address, _to : address, _value : uint256) -> bool: view
    def getBalanceOf(_user: address) -> uint256: view
    def approve(_spender : address, _value : uint256) -> bool: nonpayable
TokenContract: ERC20

electedOfficials: public(DynArray [address, 3])
moneyStored: public(uint256)
PotAddress: public(address)

@external
def __init__(thePotAddress: address, ERC20address: address):
    self.moneyStored = 0
    self.electedOfficials = []
    self.PotAddress=thePotAddress
    self.TokenContract=ERC20(ERC20address)


@external
def addMoney (amount: uint256):
    self.moneyStored = self.moneyStored + amount

@internal
def _removeMoney (amount: uint256):
    self.moneyStored = self.moneyStored - amount

@external
def setElectedOfficials (newEleectedOfficials: DynArray [address,3]):
    self.electedOfficials = newEleectedOfficials

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
    assert self._VerifyElectedOfficial(msg.sender)
    assert self.TokenContract.getBalanceOf(self.PotAddress) >= amount
    self.TokenContract.transferFromNoTax(self.PotAddress, destAddress, amount)
    self._removeMoney(amount)

#new method
@view
@external
def getPotAddress() -> address:
    return self.PotAddress

#whether or not an address is in admin array
@view
@internal
def _VerifyElectedOfficial(wolvAddress: address) -> bool:
    for item in self.electedOfficials:
        if item==wolvAddress:
            return True
    return False

