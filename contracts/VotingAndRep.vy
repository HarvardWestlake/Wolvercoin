# @version ^0.3.7

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

interface ActiveUser:
    def addAdmin(adminToAdd: address): nonpayable
    def removeAdmin(adminToRemove: address): nonpayable
    def getIsActiveUser(potentialUser: address) -> bool: view
    def getIsAdmin(potentialAdmin: address) -> bool: view

interface WVCvoteableContract:
    def finishVote(): payable

event VoteStarted:
    subjectContract: indexed(address)
    creator: address
    amountSent: uint256

event VoteEnded:
    contract: indexed(address)


activeUserAddress: public(ActiveUser)
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
peopleInvested: public(HashMap[address, DynArray[address, 64]])
# the ending block for each proposition
endBlock: public(HashMap[address, uint256])
# the value sent to contract on sucsessful vote
storedDonation: public(HashMap[address, uint256])

# list of variables that could be changed (via voting) 

# returnedWinner
# returnedLoser
voteDuration: public(uint256)
# percent needed # would be a tuple to multiply by ie (2, 1) for 50% of (4, 3) for 75%
# super percent needed
disabled: bool

# a status temporaryly granted to the contract if the choose to affect the DAO
allowedToAffectDao: address

@external
def __init__ (activeUserAddress: address, voteDuration: uint256):
    self.voteDuration = voteDuration
    self.disabled = False
    self.allowedToAffectDao = empty(address)
    self.activeUserAddress = ActiveUser(activeUserAddress)
    self.minter = msg.sender
   
# @dev This creates a new proposition for people to vote on
# @param contract address The contract that will be given ran with adminstrator on vote sucsess
# @param payable wei The WvC that will be sent to the executed contract on a sucsess

@payable
@external
def proposeVote (contract: address, explaination: String[255]):
    # there is no current (unhackable) way to check if an address is a contract 
    # https://stackoverflow.com/a/37670490 
    # as such there is no assert that can check the validity of the submitted contract

    assert not self.disabled, "This contract is no longer active"
    assert contract != empty(address), "Cannot add the 0 address as vote subject"
    assert self.endBlock[contract] == 0, "A vote has already been created for that address"

    self.endBlock[contract] = block.number + self.voteDuration
    self.storedDonation[contract] = msg.value

    log VoteStarted(contract, msg.sender, msg.value)

@external
def vote(proposition: address, amount: uint256):
    self.balanceOf[msg.sender] -= amount # this stops the whole code on underflow
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
def finishVote(contract: address): 
    assert not self.disabled, "This contract is no longer active"
    assert self.endBlock[contract] != 0 and block.number >= self.endBlock[contract], "this contract either doesn't exist or hasnt ended"

    peopleInvested: DynArray[address,64] = self.peopleInvested[contract]

    # if the vote affects the dao and passes the threshold
    if (self.affectsDao[contract] and self.activePropositions[contract] * 3 > self.totalSupply * 4) :
        for voter in peopleInvested:
            self.burnCoinOnWin(voter, contract)
        self.allowedToAffectDao = contract
        self.runCode(contract)
        self.allowedToAffectDao = empty(address)
    elif(self.activePropositions[contract] * 2 > self.totalSupply and not self.affectsDao[contract]):
        for voter in peopleInvested:
            self.burnCoinOnWin(voter, contract)
        self.runCode(contract)
    else:
        for voter in peopleInvested:
            self.returnCoinOnLose(voter, contract)

    self.resetVotablity(contract)

# will always run the code under the name "finishVote"
# the code is expected to take no parameters, if you want to implement that functionality then you likely need null coalescing
# this can be done is .sol but i dont want to add that as it would force everyone to get tools to compile it
# and i dont want to have deal with that
@internal
def runCode(contract: address):
    self.activeUserAddress.addAdmin(contract)

    # run the code (i love ACE so much)
    votableContract: WVCvoteableContract = WVCvoteableContract(contract)
    # votableContract.finishVote(value=self.storedDonation[contract]) # if this reverts i dont know if they stay an admin
    self.storedDonation[contract] = 0

    self.activeUserAddress.removeAdmin(contract)
    log VoteEnded(contract)


@internal
def resetVotablity(contract: address):
    self.endBlock[contract] = 0
    self.peopleInvested[contract] = []
    self.affectsDao[contract] = False
    self.activePropositions[contract] = 0

# called by finish vote at the end of vote when proposition wins 
@internal
def burnCoinOnWin(voterAddress: address, finishedContract: address):
    # using bit shifts for efficency
    self.balanceOf[voterAddress] += shift(self.amountInFavor[finishedContract][voterAddress], -1)
    self.totalSupply -= shift(self.amountInFavor[finishedContract][voterAddress], -1)
    self.voterCoinStaked -= self.amountInFavor[finishedContract][voterAddress]
    self.amountInFavor[finishedContract][voterAddress] = 0

# called by finish vote at end of vote when a proposition loses
@internal
def returnCoinOnLose(voterAddress: address, finishedContract: address):
    self.balanceOf[voterAddress] += self.amountInFavor[finishedContract][voterAddress]
    self.totalSupply -= self.amountInFavor[finishedContract][voterAddress]
    self.voterCoinStaked -= self.amountInFavor[finishedContract][voterAddress]


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
    self.balanceOf[msg.sender] -= _value
    self.balanceOf[_to] += _value
    log Transfer(msg.sender, _to, _value)
    return True


@external
def transferFrom(_from : address, _to : address, _value : uint256) -> bool:
    self.balanceOf[_from] -= _value
    self.balanceOf[_to] += _value
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
    assert self.activeUserAddress.getIsAdmin(msg.sender) or msg.sender == self.allowedToAffectDao, "Only the maintainer or a contract allowed to affect the Dao can change the contract state"

    self.disabled = newState


# all the setters for this class should assert that the sender is the affectsDao address
# external
# def setActiveUserAddress(newAddress: address):
#     assert not self.disabled
#     assert msg.sender == self.allowedToAffectDao
#     self.activeUserAddress = ActiveUser(newAddress)
