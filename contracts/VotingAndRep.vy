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

# list of variables that are only referenced internally

# the balance of voter coin (VC) for each user, drawn from amount of tax payed
voterCoinBalance: public(HashMap[address, uint256])
# total supply of VC
voterCoinSupply: public(uint256)
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


interface ActiveUser:
    def getActiveUser(potentialUser: address) -> bool: view
    def getAdmin(potentialAdmin: address) -> bool: view

activeUserContract: public(ActiveUser)

#setters
@external
def setAccountVCBal (account: address, newAmount: uint256):
    self.voterCoinBalance[account] = newAmount
@external
def incrementAccountVCBal (account: address, increment: uint256):
    self.voterCoinBalance[account] += increment

@external
def setVoterCoinSupply (nVoterCoinSupply: uint256):
    self.voterCoinSupply = nVoterCoinSupply

@external
def setActiveProposition(proposition: address, amount: uint256):
    self.activePropositions[proposition] = amount

@external
def __init__ (activeUserAddress: address):
    self.voteDuration = 100
    self.contractMaintainer = msg.sender
    self.disabled = False
    self.activeUserContract = ActiveUser(activeUserAddress)


@external
def hasCoin (user: address, proposal: address) -> (uint256):
    assert not self.disabled, "checks if contract is not disabled"
    assert self.activeUserContract.getActiveUser(user) == True #"checks if user is active" add later when exclusivity is done
    #assert proposal in self.ammountInFavor, "checks if the proposal exists"
    return self.amountInFavor[proposal][user]

@external 
def amountAvailable (user: address) -> (uint256):
    assert not self.disabled, "checks if contract is not disabled"
    assert self.activeUserContract.getActiveUser(user) == True #"checks if user is active", add later when exclusivity is done
    amount: uint256 = self.voterCoinBalance[user]
    return amount #"gets how much coin they have that is not invested"

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

@external
def finishVote(contract: address): 
    assert not self.disabled, "This contract is no longer active"
    amtStaked: uint256 = self.activePropositions[contract]
    array: DynArray[address,1024] = self.peopleInvested[contract]
    if (self.affectsDao[contract] == False and self.voterCoinStaked < amtStaked * 2 and self.voterCoinSupply < amtStaked * 5) or (self.voterCoinSupply * 3 < amtStaked * 4):
        self.voterCoinSupply -= self.activePropositions[contract] / 2
        for affectedAdr in array:
            self.burnCoin(affectedAdr)
            
    else:
        for affectedAdr in array:
            self.returnCoin(contract, affectedAdr)
    self.voterCoinStaked -= self.activePropositions[contract]
    
#set to internal to make finishVote work, but can be set to external temporarily to run burnCoin test separately
@internal
def burnCoin(voterAddress: address):
    assert not self.disabled, "This contract is no longer active"
    assert voterAddress != empty(address), "Cannot add the 0 address as vote subject"
    assert self.amountInFavor[self.returnedWinner][voterAddress] != empty(uint256)
    self.voterCoinBalance[voterAddress] += self.amountInFavor[self.returnedWinner][voterAddress]/2
    self.voterCoinSupply -= self.amountInFavor[self.returnedWinner][voterAddress]/2

@internal
def returnCoin(proposition: address, voterAddress: address):
    assert not self.disabled, "This contract is no longer active"
    assert voterAddress != empty(address), "Cannot add the 0 address as vote subject"
    self.voterCoinBalance[voterAddress] += self.amountInFavor[proposition][voterAddress]

@external
def vote(voter: address, proposition: address, amount: uint256):
    self.voterCoinBalance[voter] -= amount
    self.voterCoinStaked += amount
    self.activePropositions[proposition] += amount
    self.peopleInvested[proposition].append(voter)
    self.amountInFavor[proposition][voter] = amount
