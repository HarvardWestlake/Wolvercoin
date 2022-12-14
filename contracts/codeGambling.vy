# @version ^0.3.7
interface Wolvercoin: 
    def transfer(_to : address, _value : uint256) -> bool: view
    def balanceOf (account: address) -> uint256: view
wolvercoinContract: public(Wolvercoin)
justCrashed: public(bool)
crashBets: public(HashMap[address, uint256]) 
multiplier: public(uint256)
pot: public(address)

@external 
def __init__(_pot: address, wolvercoinAddress: address):
    self.justCrashed = False
    self.crashBets[msg.sender] = 0
    self.multiplier = 0
    self.pot = _pot
    self.wolvercoinContract = Wolvercoin(wolvercoinAddress)
@external 
def placeBets(gambler: address, amount: uint256):
    assert msg.sender == gambler
    assert self.justCrashed != False
    assert self.wolvercoinContract.balanceOf(msg.sender) > amount
    self.crashBets.set_Val(gambler, amount)
    gambler.transfer(self.pot, amount)
@external 
def getHashValue() -> uint256: 
    return self.crashBets[msg.sender]
