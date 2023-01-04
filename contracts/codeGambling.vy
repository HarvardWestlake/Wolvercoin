# @version ^0.3.7
interface Wolvercoin: 
    def transferFrom(_from : address, _to : address, _value : uint256) -> bool: view
    def getBalanceOf (_user: address) -> uint256: view
wolvercoinContract: public(Wolvercoin)
justCrashed: public(bool)
crashBets: public(HashMap[address, uint256]) 
multiplier: public(uint256)
pot: public(address)

@external 
def __init__(_pot: address, wolvercoinAddress: address):
    self.justCrashed = True
    self.crashBets[msg.sender] = 0
    self.multiplier = 0
    self.pot = _pot
    self.wolvercoinContract = Wolvercoin(wolvercoinAddress)

@external 
def placeBets(gambler: address, amount: uint256):
    assert msg.sender == gambler
    assert self.justCrashed != False
    assert self.wolvercoinContract.getBalanceOf(msg.sender) > amount
    self.crashBets[gambler] = amount
    #self.wolvercoinContract.transferFrom(gambler, self, amount)

@view
@external 
def getHashValue() -> uint256: 
    return self.crashBets[msg.sender] 

