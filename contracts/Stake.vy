## interface w/ method that determines if someone is an active user
## interface w/ method that removes Wolvercoin from an account
# @version ^0.3.7
interface Wolvercoin:
    def transferFrom(_from : address, _to : address, _value : uint256) -> bool: payable
    def burnFrom(_to: address, _value: uint256): payable

interface ActiveUser:
    def getActiveUser(potentialUser: address) -> bool: view
    def getAdmin(potentialAdmin: address) -> bool: view

bank: address
stakeAmounts: public(HashMap [address, uint256])
stakeDates: HashMap [address, uint256]
wolvercoinContract: Wolvercoin
newAmt: public(uint256)

@external 
def __init__(_bankAddress: address, _wolvercoinContract: Wolvercoin):
    self.bank = _bankAddress
    self.wolvercoinContract = _wolvercoinContract

@external
def unstake (_userAddress: address, amtUnstaked: uint256):
    assert amtUnstaked<self.stakeAmounts[_userAddress]
    newAmt = 0
    changeInTime: uint256 = block.timestamp - self.stakeDates[_userAddress]
    if changeInTime < 1210000:
        newAmt = 2/3*amtUnstaked
        self.wolvercoinContract.transferFrom (self.bank, _userAddress, newAmt)
        self.wolvercoinContract.burnFrom (self.bank, 1/3 * amtUnstaked)
    else:
        days: uint256 = changeInTime/86400
        newAmt = amtUnstaked*((101/100)**days)
        self.wolvercoinContract.transferFrom (self.bank, _userAddress, newAmt)
        self.stakeAmounts[_userAddress] = 0
        self.stakeDates[_userAddress] = 0

@external
def stake (user : address, amountStaked : uint256,_wolvercoinContract: Wolvercoin):
    self.wolvercoinContract = _wolvercoinContract
    assert self.activeUserContract.getActiveUser (user)
    self.stakeAmounts[user] = amountStaked
    self.wolvercoinContract.transferFrom (user, self.bank, amountStaked)

