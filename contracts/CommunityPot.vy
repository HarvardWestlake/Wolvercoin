# @version ^0.3.7

interface ERC20:
    def transfer(_to : address, _value : uint256) -> bool: nonpayable
    def getBalanceOf(_user: address) -> uint256: view

interface ActiveUser:
    def getIsAdmin(potentialAdmin: address) -> bool: view

tokenContractAddress: ERC20
activeUserContract: ActiveUser

# there is a bit of strange logic for an array over a map but here is my best logic
# > for small values arrays can be faster (see vectors in c++)
# > size is always fixed so lookup times are consistant
# > doesn't add space when checking bad input
electedOfficials: public(DynArray[address, 8])

@external
def __init__(tokenContractAddress: address, activeUserContract: address):
    self.electedOfficials = []
    self.tokenContractAddress = ERC20(tokenContractAddress)
    self.activeUserContract = ActiveUser(activeUserContract)

@external
def getMoneyStored() -> uint256:
    return self.tokenContractAddress.getBalanceOf(self)

@external
def transact(amount: uint256, userToSendTo: address):
    assert self.tokenContractAddress.getBalanceOf(self) >= amount
    assert self._isAdmin(msg.sender) or self.activeUserContract.getIsAdmin(msg.sender), "Only qualified users can add an admin"
    self.tokenContractAddress.transfer(userToSendTo, amount)

@external
def isAdmin(addressToCheck: address) -> bool:
    return self._isAdmin(addressToCheck)

@internal
def _isAdmin(addressToCheck: address) -> bool:
    for entry in self.electedOfficials:
        if entry == addressToCheck:
            return True
    return False

@external
def addElectedOfficial(newElectedOfficial: address):
    assert not self._isAdmin(newElectedOfficial), "You can't add an admin twice"
    assert self._isAdmin(msg.sender) or self.activeUserContract.getIsAdmin(msg.sender), "Only qualified users can add an admin"
    self.electedOfficials.append(newElectedOfficial)
