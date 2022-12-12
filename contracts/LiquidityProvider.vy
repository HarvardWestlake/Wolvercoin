totalOfTransactions: uint256
bank: uint256
tenPercent: uint256
@internal
def takeTenPercent() -> uint256: 
    self.tenPercent = self.totalOfTransactions/10
    self.totalOfTransactions = self.totalOfTransactions - self.tenPercent
    self.bank = self.bank + self.tenPercent
    return self.tenPercent 
