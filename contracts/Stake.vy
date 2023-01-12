# @version ^0.3.7
## interfaces w/ ActiveUser and Wolvercoin
## anything that requires staking will interface with this class

interface Token:
    def transferFrom(_from : address, _to : address, _value : uint256) -> bool: nonpayable
    def burnFrom(_to: address, _value: uint256): nonpayable

interface ActiveUser:
    def getActiveUser(potentialUser: address) -> bool: view
    def getAdmin(potentialAdmin: address) -> bool: view

stakeAmounts: public(HashMap [address, uint256])
stakeDates: HashMap [address, uint256]
wolvercoinContract: Token
activeUserContract: ActiveUser

@external 
def __init__(_wolvercoinContract: address, _activeUserContract: address):
    self.wolvercoinContract = Token(_wolvercoinContract)
    self.activeUserContract = ActiveUser(_activeUserContract)

@external
def stake (user: address, amountStaked: uint256):
    assert self.activeUserContract.getActiveUser (user)
    self.stakeAmounts[user] += amountStaked
    self.stakeDates[user] = block.timestamp
    self.wolvercoinContract.transferFrom (user, self, amountStaked)

@external
def unstake (_userAddress: address, amtUnstaked: uint256):
    assert amtUnstaked <= self.stakeAmounts[_userAddress]
    changeInTime: uint256 = block.timestamp - self.stakeDates[_userAddress]
    if changeInTime < 1210000:
        decimalAmt: decimal = convert (amtUnstaked, decimal)
        oneThird: decimal = decimalAmt / 3.0
        newAmt: uint256 = 2 * convert(oneThird, uint256)
        self.wolvercoinContract.transferFrom (self, _userAddress, newAmt)
        self.stakeAmounts[_userAddress] -= amtUnstaked
    else:
        days: uint256 = changeInTime/86400
        percent: uint256 = 3800 / 365
        assert percent == 10
        newAmt: uint256 = amtUnstaked * days / percent
        self.wolvercoinContract.transferFrom (self, _userAddress, newAmt)
        self.stakeAmounts[_userAddress] -= amtUnstaked



