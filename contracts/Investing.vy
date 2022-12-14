#version ^0.3.7
##Interfaces with method that monitors totalOfTransactions
interface Wolvercoin:
    def totalOfTransactions() -> uint256: view

totalOfTransactions: uint256
tenPercent: uint256
wolvercoinContract: Wolvercoin

@external
def __init__(wolvercoinContract: Wolvercoin):
    self.wolvercoinContract = wolvercoinContract

@external
def takeTenPercent() -> uint256: 
    self.totalOfTransactions = self.wolvercoinContract.totalOfTransactions()
    temp:uint256 = self.totalOfTransactions/10
    if self.totalOfTransactions != 0:
        self.totalOfTransactions = self.totalOfTransactions - temp
    return temp 