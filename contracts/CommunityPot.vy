# @version 0.3.7

interface Wolvercoin:
    def transferFrom(address,address,uint256) -> bool: view
    def balanceOf(address) -> uin256: view


#is there an interface admin?? idk
admin: HashMap[address, bool] #bool should always be true
PotAddress: public(address)

@external
def __init__(thePotAddress: address):
    self.PotAddress=thePotAddress

#moves money without tax from pot to an address
@external
def Transact(amount: uint256, destAddress: address, wolvercoinContract: Wolvercoin):
    assert wolvercoinContract.balanceOf[self.PotAddress] >= amount
    wolvercoinContract.transferFrom(self.PotAddress, destAddress, amount)

#whether or not an address is in admin array
@external
def VerifyAdmin(wolvAddress: address) -> bool:
    assert self.admin[wolvAddress]
    return True




