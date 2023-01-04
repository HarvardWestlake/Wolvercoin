# @version ^0.3.7

interface ERC20:
    def transferFrom(_from : address, _to : address, _value : uint256) -> bool: view
    def getBalanceOf(_user: address) -> uint256: view
ERC20Contract: public(ERC20)

interface ActiveUser:
    def getAdmin(potentialAdmin: address) -> bool: view

ActiveUserContract: public(ActiveUser)

#variables not related to interface
PotAddress: public(address)

@external
def __init__(thePotAddress: address, ERC20address: address, ActiveUserContractAddress: address):
    self.PotAddress=thePotAddress
    self.ERC20Contract=ERC20(ERC20address)
    self.ActiveUserContract=ActiveUser(ActiveUserContractAddress)

#moves money without tax from pot to an address
@external
def Transact(amount: uint256, destAddress: address):
    assert self.ERC20Contract.getBalanceOf(self.PotAddress) >= amount
    self.ERC20Contract.transferFrom(self.PotAddress, destAddress, amount)

#whether or not an address is in admin array
@external
def VerifyAdmin(wolvAddress: address) -> bool:
    return self.ActiveUserContract.getAdmin(wolvAddress)
    




