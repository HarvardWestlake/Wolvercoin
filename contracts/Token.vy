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

# GamblingPot is a contract that holds the tax for the gambling pot
interface GamblingPotContract:
    def getAmountToTax(preTaxAmount: uint256) -> uint256: nonpayable
gambling_pot_contract: public(GamblingPotContract)

interface ActiveUserContract:
    def getIsAdmin(_potentialAdmin: address) -> bool: view
active_user_contract: public(ActiveUserContract)


@external
def __init__(_name: String[32], _symbol: String[32], _decimals: uint8, _supply: uint256):
    init_supply: uint256 = _supply * 10 ** convert(_decimals, uint256)
    self.name = _name
    self.symbol = _symbol
    self.decimals = _decimals
    self.balanceOf[msg.sender] = init_supply
    self.totalSupply = init_supply
    self.minter = msg.sender
    log Transfer(empty(address), msg.sender, init_supply)

@view
@external
def getAllowanceOf(_from: address) -> uint256:
    return self.allowance[_from][msg.sender]

@view
@external
def getBalanceOf(_user: address) -> uint256:
    return self.balanceOf[_user]

@view
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

@external
def transferFromWithTax(_from : address, _to : address, _value: uint256) -> bool:
    """
     @dev Transfer tokens from one address to another including a tax for the gambling pot.
     @param _from address The address which you want to send tokens from
     @param _to address The address which you want to transfer to
     @param _value uint256 the amount of tokens to be transferred
    """
    # Gambling Pot Tax 
    #  should be a POT located in a GamblingPot contract and not related to the actual token itself
    #  when transactions outside are made, they should be able to include
    #  GamblingPot.tax(gamblingPotTaxPercentage) before calling transferFrom

    ## Note: Calling a tax on transferFrom applies even transactions from a single student to another
    #   or when someone bids 1 WVC on an item, the tax is applied to the 1 WVC as well, including when the 
    #   pot of money is then transfered back out.  Basically the tax is on EVERY transaction, not just specific ones...

    assert self.gambling_pot_contract.address != empty(address)
    assert self.balanceOf[_from] >= _value

    # Get gamblingPotTax
    _gamblingPotTaxAmount: uint256 = self.gambling_pot_contract.getAmountToTax(_value)
    _nonTaxedAmount: uint256 = _value - _gamblingPotTaxAmount

    # NOTE: vyper does not allow underflows
    #       so the following subtraction would revert on insufficient balance
    self.balanceOf[_from] -= _value
    self.balanceOf[self.gambling_pot_contract.address] += _gamblingPotTaxAmount
    self.balanceOf[_to] += _nonTaxedAmount

    # NOTE: vyper does not allow underflows
    #      so the following subtraction would revert on insufficient allowance
    self.allowance[_from][msg.sender] -= _value
    log Transfer(_from, self.gambling_pot_contract.address, _gamblingPotTaxAmount)
    log Transfer(_from, _to, _nonTaxedAmount)
    return True


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
    self._mint(_to, _value)

@internal
def _mint(_to: address, _value: uint256):
    """
    @dev Mint an amount of the token and assigns it to an account.
         This encapsulates the modification of balances such that the
         proper events are emitted.
    @param _to The account that will receive the created tokens.
    @param _value The amount that will be created.
    """
    assert msg.sender == self.minter
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
def setGamblingPotContract(_gamblingPotContract: address):
    assert msg.sender == self.minter
    self.gambling_pot_contract = GamblingPotContract(_gamblingPotContract)

@external
def setActiveUserContract(_activeUserContract: address):
    assert msg.sender == self.minter
    self.active_user_contract = ActiveUserContract(_activeUserContract)

@external
def bulkMintUniqueAmount(_to: DynArray[address,100], _value: DynArray[uint256,100]):
    assert len(_to) == len(_value), "Array lengths must match"
    assert self.active_user_contract.address != empty(address)
    assert self.active_user_contract.getIsAdmin(msg.sender)
    counter: uint256 = 0
    value: uint256 = _value[counter]
    for i in _to:
        value = _value[counter]
        counter += 1
        self._mint(i, value)

