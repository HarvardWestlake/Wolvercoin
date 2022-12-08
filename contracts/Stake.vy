bank: address
totalTransactions: HashMap [uint256, uint256]
stakeAmounts: HashMap [address, uint256]
stakeDates: HashMap [address, uint256]

@external 
def __init__(_bankAddress: address):
    bank = _bankAddress

@external
def unstake (_userAddress: address, amtUnstaked: uint256):
    assert amtUnstaked < stakeAmounts[_userAddress]
    if stakeDates[_userAddress] - block.timestamp < 14:
        transferFrom (bank, _userAddress, 2/3 * amtUnstaked)
        burnFrom (bank, 1/3 * amtUnstaked)
    else:
        percentChange: uint256
        percentChange = (totalTransactions [1]/totalTransactions[0])
        newAmt: uint256
        newAmt = amtUnstaked * percentChange
        transferFrom (bank, _userAddress, newAmt)
        stakeAmounts.remove (_userAddress)
        stakeDates.remove (_userAddress)
        





