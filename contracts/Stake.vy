# @version ^0.3.7
## interfaces w/ ActiveUser and Wolvercoin
## anything that requires staking will interface with this class

interface Token:
    def transferFrom(_from : address, _to : address, _value : uint256) -> bool: nonpayable
    def transfer(_to : address, _value : uint256) -> bool: nonpayable
    def burnFrom(_to: address, _value: uint256): nonpayable
    def getBalanceOf (_user: address) -> uint256: nonpayable

interface ActiveUser:
    def getIsActiveUser(potentialUser: address) -> bool: view
    def getIsAdmin(potentialAdmin: address) -> bool: view

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
    assert self.activeUserContract.getIsActiveUser (user)
    assert amountStaked <= self.wolvercoinContract.getBalanceOf (user)
    self.stakeAmounts[user] += amountStaked
    self.stakeDates[user] = block.timestamp
    self.wolvercoinContract.transferFrom(user, self, amountStaked)

@external
def unstake (_userAddress: address, amtUnstaked: uint256):
    assert amtUnstaked <= self.stakeAmounts[_userAddress]

    # Call to calculate proper amount to unstake
    # _newAmount : uint256 = self._calculateUnstakedAmount(_userAddress)
    
    self.stakeAmounts[_userAddress] -= amtUnstaked
    self.stakeDates[_userAddress] = block.timestamp
    
    # Update to calculate the amount unstaked and unstake proper amount
    #self.wolvercoinContract.transferFrom (_userAddress, _newAmount)
    self.wolvercoinContract.transfer(_userAddress, amtUnstaked)

@view
@internal
def _calculateUnstakedAmount(_userAddress : address) -> uint256:
    changeInTime: uint256 = block.timestamp - self.stakeDates[_userAddress]
    if changeInTime < 1210000:
        decimalAmt: decimal = convert (self.stakeAmounts[_userAddress], decimal)
        oneThird: decimal = decimalAmt / 3.0
        newAmt: uint256 = 2 * convert(oneThird, uint256)
        return newAmt
    else:
        days: uint256 = changeInTime/86400
        # the percent value is calculated based on a 1% daily interest rate -- can be changed
        percent: uint256 = 3800 / 365 
        assert percent == 10
        newAmt: uint256 = self.stakeAmounts[_userAddress] * days * percent / 100
        return newAmt

@view
@external
def calculateUnstakedAmount(_userAddress : address) -> uint256:
    return self._calculateUnstakedAmount(_userAddress)