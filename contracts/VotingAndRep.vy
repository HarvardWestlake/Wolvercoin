# @version 0.3.7

# @dev An rundementary implementation of a voting system 
# @author Evan Stokdyk (@Focus172)

# VotingAndRep.vy

# list of variables that are only referenced internally

# the balence of voter coin (VC) for each user, drawn from amount of tax payed
voterCoinBalance: public(HashMap[address, uint256])
# total supply of VC
voterCoinSupply: public(uint256)
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
# returnedWinner
# returnedLoser
voteDuration: public(uint256)
# percent needed
# super percent needed
contractMaintainer: public(address)


disabled: bool

event VoteStarted:
    subjectContract: address
    creator: address
    amountSent: uint256

@external
def __init__ ():
    self.voteDuration = 100
    self.contractMaintainer = msg.sender
    self.disabled = False

   
# @dev This creates a new proposition for people to vote on
# @param contract address The contract that will be given ran with adminstrator on vote sucsess
# @param payable wei The WvC that will be sent to the executed contract on a sucsess
@payable
@external
def proposeVote (contract: address, explaination: String[255]):
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


@external
def setDisabled(newState: bool):
    assert msg.sender == self.contractMaintainer, "Only the maintainer can change the contract state"

    self.disabled = newState

@external 
def setContractMaintainer(newMaintainer: address):
    assert msg.sender == self.contractMaintainer, "Only the maintainer or DAO can change the maintainer"
    assert newMaintainer != empty(address), "You can't remove the maintainer"

    self.contractMaintainer = newMaintainer