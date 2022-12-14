# @version ^0.3.7
#Interface:
#   ActiveUser:
#       getActiveUser
#       getAdmin
#To be Interfaced:
#   amountAvailable
#dependent on:
#   transfer (should call incrementAccountVCBal(amount being))
#depends on us:
#   theoretically all contracts, as we can edit the contract via changing the proxy
# @dev An rundementary implementation of a voting system 
# @author Gavin Goldsmith (@Gav-G)

# VotingAndRep.vy

from vyper.interfaces import ERC20
from vyper.interfaces import ERC20Detailed

implements: ERC20
implements: ERC20Detailed

interface ActiveUser:
    def getActiveUser(potentialUser: address) -> bool: view
    def getAdmin(potentialAdmin: address) -> bool: view

activeUserContract: public(ActiveUser)

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

# the balance of voter coin (VC) for each user, drawn from amount of tax payed
balanceOf: public(HashMap[address, uint256])
# total amount in circulation
totalSupply: public(uint256)
# allows people to spend other people money
allowance: public(HashMap[address, HashMap[address, uint256]])
# the address of the contract that prints people VC
minter: address
# amount of VC currently staked
voterCoinStaked: public(uint256)
# the map containing active propositions with total amount invested
activePropositions: public(HashMap[address, uint256])
# a boolean for each function on if it needs a super majority
affectsDao: public(HashMap[address, bool])
# storage for each persons money in a proposition
amountInFavor: public(HashMap[address, HashMap[address, uint256]]) # this maybe should not be public
# list of people in each proposition (to improve efficency in money returns)
peopleInvested: HashMap[address, DynArray[address, 1024]]
# the ending block for each proposition
endBlock: public(HashMap[address, uint256])
# the value sent to contract on sucsessful vote
storedDonation: public(HashMap[address, uint256])

# list of variables that could be changed (via voting) 

returnedWinner: address
# returnedLoser
voteDuration: public(uint256)
# percent needed
# super percent needed
contractMaintainer: public(address)

event VoteStarted:
    subjectContract: address
    creator: address
    amountSent: uint256

disabled: bool


@external
def __init__ (activeUserAddress: address):
    self.voteDuration = 100
    self.contractMaintainer = msg.sender
    self.disabled = False
    self.activeUserContract = ActiveUser(activeUserAddress)

    # more token things
    self.name = "VoterCoin"
    self.symbol = "WvcVc"
    self.decimals = 18
    self.totalSupply = 0
    self.minter = msg.sender

@external
def hasCoin (user: address, proposal: address) -> (uint256):
    assert not self.disabled, "checks if contract is not disabled"
    # assert self.activeUserContract.getActiveUser(user) == True #"checks if user is active" add later when exclusivity is done
    # assert proposal in self.ammountInFavor, "checks if the proposal exists"
    return self.amountInFavor[proposal][user]

@external 
def amountAvailable (user: address) -> (uint256):
    assert not self.disabled, "checks if contract is not disabled"
    # assert self.activeUserContract.getActiveUser(user) == True #"checks if user is active", add later when exclusivity is done
    amount: uint256 = self.balanceOf[user]
    return amount #"gets how much coin they have that is not invested"

# @dev This creates a new proposition for people to vote on
# @param contract address The contract that will be given ran with adminstrator on vote sucsess
# @param payable wei The WvC that will be sent to the executed contract on a sucsess

@payable
@external
def proposeVote (contract: address, explaination: String[255]) -> (bool):
    # there is no current (unhackable) way to check if an address is a contract 
    # https://stackoverflow.com/a/37670490 
    # as such there is no assert that can check the validity of the submitted contract

    # checks that code is ok to run
    assert not self.disabled, "This contract is no longer active"
    assert contract != empty(address), "Cannot add the 0 address as vote subject"
    # NOTE: the below code currently means the same charity cannot recive money twice, this should be fixed
    assert self.endBlock[contract] == 0, "A vote has already been created for that address"

    # Implementation is near impossible
    # curAffectsDAO: bool = True

    # main body of the code
    # self.affectsDao[contract] = curAffectsDAO
    self.endBlock[contract] = block.number + self.voteDuration
    self.storedDonation[contract] = msg.value

    log VoteStarted(contract, msg.sender, msg.value)
    return True

@external
def vote(proposition: address, amount: uint256):
    self.balanceOf[msg.sender] -= amount
    self.voterCoinStaked += amount
    self.activePropositions[proposition] += amount
    self.peopleInvested[proposition].append(msg.sender) # this should not add a new entry for each time someone votes
    self.amountInFavor[proposition][msg.sender] += amount

@external
def mint(_to: address, _value: uint256):
    assert msg.sender == self.minter
    assert _to != empty(address)
    self.totalSupply += _value
    self.balanceOf[_to] += _value
    log Transfer(empty(address), _to, _value)

@external
def burn(_value: uint256):
    self._burn(msg.sender, _value)

@internal
def _burn(_to: address, _value: uint256):
    assert _to != empty(address)
    self.totalSupply -= _value
    self.balanceOf[_to] -= _value
    log Transfer(_to, empty(address), _value)

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

# allows other people to spend your money
@external
def approve(_spender : address, _value : uint256) -> bool:
    self.allowance[msg.sender][_spender] = _value
    log Approval(msg.sender, _spender, _value)
    return True

# burn other peoples money if they let you
@external
def burnFrom(_to: address, _value: uint256):
    self.allowance[_to][msg.sender] -= _value
    self._burn(_to, _value)

@external
def setDisabled(newState: bool):
    assert msg.sender == self.contractMaintainer, "Only the maintainer can change the contract state"

    self.disabled = newState

@external 
def setContractMaintainer(newMaintainer: address):
    assert msg.sender == self.contractMaintainer, "Only the maintainer or DAO can change the maintainer"
    assert newMaintainer != empty(address), "You can't remove the maintainer"

    self.contractMaintainer = newMaintainer