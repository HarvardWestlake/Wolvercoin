# @dev An rundementary implementation of a voting system 
# @author Evan Stokdyk (@Focus172)

# @version 0.3.7

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

@external
def __init__ ():
    self.voteDuration = 100

   
# This creates a new proposition for people to vote on
# @param contract - the contract that will be given ran with adminstrator on vote sucsess
# @payable the WvC that will be sent to the executed contract on a sucsess
@payable
@external
def proposeVote (contract: address) -> bool:
    # read the contract to find out what it does

    # there is no current (unhackable) way to check if an address is a contract 
    # https://stackoverflow.com/a/37670490 
    # as such there is no assert that can check the validity of the submitted contract

    # checks that there is not already a proposition for that contract
    assert self.endBlock[contract] == 0

    # checking if it affects the Dao
    # TODO: implement this
    curAffectsDAO: bool = True

    # main body of the code
    self.affectsDao[contract] = curAffectsDAO
    self.endBlock[contract] = block.number + self.voteDuration
    self.storedDonation[contract] = msg.value
    return True
