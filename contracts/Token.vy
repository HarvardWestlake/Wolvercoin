# @version ^0.3.7
# @dev Implementation of ERC-20 token standard.
# @author Takayuki Jimba (@yudetamago)
# https://github.com/ethereum/EIPs/blob/master/EIPS/eip-20.md

from vyper.interfaces import ERC20
from vyper.interfaces import ERC20Detailed

implements: ERC20
implements: ERC20Detailed



event Transfer:
    sender: indexed(address)
    receiver: indexed(address)
    value: uint256

event Approval:
    owner: indexed(address)
    spender: indexed(address)
    value: uint256

name: public(String[32])
symbol: public(String[32])
decimals: public(uint8)

# NOTE: By declaring `balanceOf` as public, vyper automatically generates a 'balanceOf()' getter
#       method to allow access to account balances.
#       The _KeyType will become a required parameter for the getter and it will return _ValueType.
#       See: https://vyper.readthedocs.io/en/v0.1.0-beta.8/types.html?highlight=getter#mappings
balanceOf: public(HashMap[address, uint256])
# By declaring `allowance` as public, vyper automatically generates the `allowance()` getter
allowance: public(HashMap[address, HashMap[address, uint256]])
# By declaring `totalSupply` as public, we automatically create the `totalSupply()` getter
totalSupply: public(uint256)
minter: address


contract_bitmask: uint256
contract_hex: uint256

gambling_pot: public(address)


@external
def __init__(_name: String[32], _symbol: String[32], _decimals: uint8, _supply: uint256):
    init_supply: uint256 = _supply * 10 ** convert(_decimals, uint256)
    self.name = _name
    self.symbol = _symbol
    self.decimals = _decimals
    self.balanceOf[msg.sender] = init_supply
    self.totalSupply = init_supply
    self.minter = msg.sender
    self.contract_bitmask = convert(0xFFFFF00000000000000000000000000000000000, uint256)
    self.contract_hex = convert(0xAB66600000000000000000000000000000000000, uint256)
    log Transfer(empty(address), msg.sender, init_supply)


@external
def getAllowanceOf(_from: address) -> uint256:
    return self.allowance[_from][msg.sender]

@view
@external
def getBalanceOf(_user: address) -> uint256:
    return self.balanceOf[_user]

@external
def getApprovedAmountOf(_user: address, _spender: address) -> uint256:
    return self.allowance[_user][_spender]

@external
def transfer(_to : address, _value : uint256) -> bool:
    """
    @dev Transfer token for a specified address
    @param _to The address to transfer to.
    @param _value The amount to be transferred.
    """
    # NOTE: vyper does not allow underflows
    #       so the following subtraction would revert on insufficient balance
    self.balanceOf[msg.sender] -= _value
    self.balanceOf[_to] += _value
    log Transfer(msg.sender, _to, _value)
    return True


# @external
# def transferFrom(_from : address, _to : address, _value : uint256) -> bool:
#     """
#      @dev Transfer tokens from one address to another.
#      @param _from address The address which you want to send tokens from
#      @param _to address The address which you want to transfer to
#      @param _value uint256 the amount of tokens to be transferred
#     """
#     # NOTE: vyper does not allow underflows
#     #       so the following subtraction would revert on insufficient balance

#     # TODO: WHOEVER WROTE GAMBLING POT TAX BROKE, LIKE, ALL THE TESTS THAT USED TOKEN.VY!!!!

#     # calculate the 3.5% tax for the gambling pot, and floor the value
#     # gamblingPotTax: uint256 = convert(
#     #     floor(
#     #         convert(_value, decimal) * 0.035
#     #         ),
#     #     uint256
#     #     )

#     # calculate the real transaction amount
#     transactionAmount: uint256 = _value - gamblingPotTax

#     # add tax to gambling pot
#     self.balanceOf[self.gambling_pot] += gamblingPotTax

#     assert self.balanceOf[_from] > _value
#     self.balanceOf[_from] -= _value

#     # log gambling tax
#     log Transfer(_from, self.gambling_pot, gamblingPotTax)

#     self.balanceOf[_to] += transactionAmount
#     log Transfer(_from, _to, transactionAmount)

#     return True

@external
def transferFrom(_from : address, _to : address, _value : uint256) -> bool:
    """
    @dev Transfer tokens from one address to another.
    @param _from address The address which you want to send tokens from
    @param _to address The address which you want to transfer to
    @param _value uint256 the amount of tokens to be transferred
    """
    # NOTE: vyper does not allow underflows
    #       so the following subtraction would revert on insufficient balance
    self.balanceOf[_from] -= _value
    self.balanceOf[_to] += _value
    # NOTE: vyper does not allow underflows
    #      so the following subtraction would revert on insufficient allowance
    self.allowance[_from][msg.sender] -= _value
    log Transfer(_from, _to, _value)
    return True

@external
def approve(_spender : address, _value : uint256) -> bool:
    """
    @dev Approve the passed address to spend the specified amount of tokens on behalf of msg.sender.
         Beware that changing an allowance with this method brings the risk that someone may use both the old
         and the new allowance by unfortunate transaction ordering. One possible solution to mitigate this
         race condition is to first reduce the spender's allowance to 0 and set the desired value afterwards:
         https://github.com/ethereum/EIPs/issues/20#issuecomment-263524729
    @param _spender The address which will spend the funds.
    @param _value The amount of tokens to be spent.
    """
    self.allowance[msg.sender][_spender] = _value
    log Approval(msg.sender, _spender, _value)
    return True


@external
def mint(_to: address, _value: uint256):
    """
    @dev Mint an amount of the token and assigns it to an account.
         This encapsulates the modification of balances such that the
         proper events are emitted.
    @param _to The account that will receive the created tokens.
    @param _value The amount that will be created.
    """
    isCalledFromContract: bool = ((convert(msg.sender, uint256) & self.contract_bitmask) ^ self.contract_hex) == self.contract_bitmask
    assert msg.sender == self.minter or isCalledFromContract
    assert _to != empty(address)
    self.totalSupply += _value
    self.balanceOf[_to] += _value
    log Transfer(empty(address), _to, _value)


@internal
def _burn(_to: address, _value: uint256):
    """
    @dev Internal function that burns an amount of the token of a given
    account.
    @param _to The account whose tokens will be burned.
    @param _value The amount that will be burned.
    """
    assert _to != empty(address)
    self.totalSupply -= _value
    self.balanceOf[_to] -= _value
    log Transfer(_to, empty(address), _value)
    return


@external
def burn(_value: uint256):
    """
    @dev Burn an amount of the token of msg.sender.
    @param _value The amount that will be burned.
    """
    self._burn(msg.sender, _value)

@external
def burnFrom(_to: address, _value: uint256):
    """
    @dev Burn an amount of the token from a given account.
    @param _to The account whose tokens will be burned.
    @param _value The amount that will be burned.
    """
    self.allowance[_to][msg.sender] -= _value
    self._burn(_to, _value)
@external
def generate_random_number(maxVal: uint256) -> uint256:
    return block.timestamp % maxVal

@external
def setGamblingPot(gp: address):
    self.gambling_pot = gp
