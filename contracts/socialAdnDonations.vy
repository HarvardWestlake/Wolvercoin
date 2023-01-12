# @version ^0.3.7
# code is dependent on activeUser
interface Wolvercoin:
    def transferFrom(_from : address, _to : address, _value : uint256) -> bool: payable

wolvercoinContract: public(Wolvercoin)

@external
def __init__ (wolvercoinAdress: address):
    self.wolvercoinContract = Wolvercoin(wolvercoinAdress)
    return

@external
def donate(current: address, to: address, val: uint256):
    self.wolvercoinContract.transferFrom(current,to,val)
