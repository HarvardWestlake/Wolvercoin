# @version ^0.3.3
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
def unstake (_userAddress: address, amtUnstaked: uint256) -> (bool, uint256):
    if amtUnstaked>self.stakeAmounts[_userAddress]:
        return (False, 0)
    else:
        newAmt: uint256 = 0
        changeInTime: uint256 = block.timestamp - self.stakeDates[_userAddress]
        if changeInTime < 1210000:
            newAmt = 2/3*amtUnstaked
            self.wolvercoinContract.transferFrom (self.bank, _userAddress, newAmt)
            self.wolvercoinContract.burnFrom (self.bank, 1/3 * amtUnstaked)
        else:
            days: uint256 = changeInTime/86400
            newAmt = convert (amtUnstaked*((101/100)**days), uint256)
            self.wolvercoinContract.transferFrom (self.bank, _userAddress, newAmt)
            self.stakeAmounts[_userAddress] = 0
            self.stakeDates[_userAddress] = 0
        return (True, newAmt)