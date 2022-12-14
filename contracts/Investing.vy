totalOfTransactions: uint256
tenPercent: uint256
@internal
def takeTenPercent() -> uint256: 
    temp:uint256 = self.totalOfTransactions/10
    self.totalOfTransactions = self.totalOfTransactions - temp
    return temp 