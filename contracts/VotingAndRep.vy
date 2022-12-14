# @version 0.3.7

interface ActiveUser:
    def getAdmin(a: address) -> bool: view

activeUserAddress: public(ActiveUser)

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
# contractMaintainer: public(address)
disabled: bool

# temporary storage
# a status temporaryly granted to the contract if the choose to affect the DAO
allowedToAffectDao: address

event VoteStarted:
    subjectContract: address
    creator: address
    amountSent: uint256

@external
def __init__ (activeUserAddress: address):
    self.voteDuration = 100
    self.disabled = False
    self.allowedToAffectDao = empty(address)
    self.activeUserAddress = ActiveUser(activeUserAddress)
   
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

    # main body of the code
    self.endBlock[contract] = block.number + self.voteDuration
    self.storedDonation[contract] = msg.value

    log VoteStarted(contract, msg.sender, msg.value)


@external
def setDisabled(newState: bool):
    assert self.activeUserAddress.getAdmin(msg.sender) or msg.sender == self.allowedToAffectDao, "Only the maintainer or a contract allowed to affect the Dao can change the contract state"

    self.disabled = newState