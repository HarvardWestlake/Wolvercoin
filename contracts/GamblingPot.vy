# @version ^0.3.7
## Gambling Pot ##
# This is the gambling pot, where the players' tax gets deposited

TAX_RATE : public(uint256)
TAX_DECIMALS : public(uint256)


# vyper.interfaces.ERC20 does not include the mint and burn functions so we make our own interface
interface ERC20WithAdminAccess:
    def getBalanceOf(_address: address) -> uint256: nonpayable
    def transferFrom(_from : address, _to : address, _value : uint256) -> bool: nonpayable
    def transfer(_to : address, _value : uint256) -> bool: nonpayable
    def approve(_spender : address, _value : uint256) -> bool: nonpayable

interface ActiveUser:
    def getIsActiveUser(potentialUser: address) -> bool: view
    def getIsAdmin(potentialAdmin: address) -> bool: view
    def getIsAdminAndActiveUser(potentialAdmin: address) -> bool: view
    
erc20: ERC20WithAdminAccess
activeUser: ActiveUser

# Token with a tax rate of 0.0354 would be a tax_rate of 354 and a decimal value of 4
@external
def __init__ ( _tax_rate : uint256 , _tax_decimals : uint256, erc20address: address, activeUserAddress: address):
    self.TAX_RATE = _tax_rate
    self.TAX_DECIMALS = _tax_decimals
    self.activeUser = ActiveUser(activeUserAddress)
    self.erc20 = ERC20WithAdminAccess(erc20address)
    return

@external
def payOut( _amount : uint256, winner: address):
    assert self.activeUser.getIsAdminAndActiveUser(msg.sender)
    self.erc20.transfer(winner, _amount)

@external
@view
def getBalance() -> uint256:
    return self.balance

@external
@view
def getAmountToTax(originalAmount : uint256) -> uint256:
    return originalAmount * self.TAX_RATE / (10 ** self.TAX_DECIMALS)

