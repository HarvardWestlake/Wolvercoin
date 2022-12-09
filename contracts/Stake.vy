interface Wolvercoin:
    def transferFrom(_from : address, _to : address, _value : uint256) -> bool: payable
    def burnFrom(_to: address, _value: uint256): payable

bank: address
stakeAmounts: HashMap [address, uint256]
stakeDates: HashMap [address, uint256]
wolvercoinContract: Wolvercoin

@external 
def __init__(_bankAddress: address, _wolvercoinContract: Wolvercoin):
    self.bank = _bankAddress
    self.wolvercoinContract = _wolvercoinContract


@external
def unstake (_userAddress: address, amtUnstaked: decimal) -> (bool, uint256):
    if amtUnstaked>self.stakeAmounts[_userAddress]:
        return (False, 0)
    else:
        newAmt: decimal = 0.0
        changeInTime: uint256 = block.timestamp - self.stakeDates[_userAddress]
        if changeInTime < 1210000:
            newAmt = (decimal) 0.67*amtUnstaked
            self.wolvercoinContract.transferFrom (self.bank, _userAddress, newAmt)
            self.wolvercoinContract.burnFrom (self.bank, 1/3 * amtUnstaked)
        else:
            days: decimal = changeInTime/86400
            percentChange: decimal = 1.01
            newAmt = amtUnstaked * (1.01**days)
            transferFrom (bank, _userAddress, newAmt)
            stakeAmounts.remove (_userAddress)
            stakeDates.remove (_userAddress)
        return (True, newAmt)