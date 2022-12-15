# @version ^0.3.7
## interfaces w/ ActiveUser and Wolvercoin
## anything that requires staking will interface with this class

interface Token:
    def transferFrom(_from : address, _to : address, _value : uint256) -> bool: payable
    def burnFrom(_to: address, _value: uint256): payable

interface ActiveUser:
    def getActiveUser(potentialUser: address) -> bool: view
    def getAdmin(potentialAdmin: address) -> bool: view

bank: address
stakeAmounts: public(HashMap [address, uint256])
stakeDates: HashMap [address, uint256]
wolvercoinContract: Token
newAmt: public(uint256)
activeUserContract: ActiveUser

@external
def stake (user : address, amountStaked : uint256):
    assert self.activeUserContract.getActiveUser (user)
    self.stakeAmounts[user] += amountStaked
    self.stakeDates[user] = block.timestamp
    self.wolvercoinContract.transferFrom (user, self.bank, amountStaked)
    
@external 
def __init__(_bankAddress: address, _wolvercoinContract: Token, _activeUserContract: ActiveUser):
    self.bank = _bankAddress
    self.wolvercoinContract = _wolvercoinContract
    self.activeUserContract = _activeUserContract

@external
def unstake (_userAddress: address, amtUnstaked: uint256):
    #the type conversions are really janky -- if anyone knows a better way of doing this, pls fix it!
    assert amtUnstaked<self.stakeAmounts[_userAddress]
    self.newAmt = 0
    changeInTime: uint256 = block.timestamp - self.stakeDates[_userAddress]
    if changeInTime < 1210000:
        decimalAmt:decimal = convert (amtUnstaked, decimal)
        oneThird:decimal = decimalAmt/3.0
        self.newAmt = 2* convert(oneThird,uint256)
        self.wolvercoinContract.transferFrom (self.bank, _userAddress, self.newAmt)
        self.wolvercoinContract.burnFrom (self.bank, convert (oneThird, uint256))
        self.stakeAmounts[_userAddress] -= amtUnstaked
    else:
        days: uint256 = changeInTime/86400
        percent: decimal = (convert(101**days, decimal) / convert(100**days, decimal))
        self.newAmt = amtUnstaked * (convert((percent),uint256))
        self.wolvercoinContract.transferFrom (self.bank, _userAddress, self.newAmt)
        self.stakeAmounts[_userAddress] = 0
        self.stakeDates[_userAddress] = 0

