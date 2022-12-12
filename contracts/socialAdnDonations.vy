# @version ^0.3.7
interface ActiveUser:
    def getActiveUser(potentialUser: address) -> bool: view
    def getAdmin(potentialAdmin: address) -> bool: view

activeStudents: public(Hashmap[address, uint256])
activeYear: public( uint256 )
teachers: public(HashMap[address, boolean]) # hashmap?
electedOfficials: public(DynArray[address, 3])
alreadyVotedOfficials: public(HashMap [address, bool])
votesForOfficials: public(HashMap [address, uint256])
officialVotingPeriod: public(bool)
alreadyVotedProposal: DynArray [address,100]
proposalVotes: DynArray[uint256, 3]
activeUserContract: public(ActiveUser)



@external
def __init__ (activeUserAddress: address):
    self.activeYear = 2023
    self.activeUserContract = ActiveUser(activeUserAddress)


@external
def endVoteOfficial():
    assert self.activeUserContract.getAdmin(block.coinbase)   # what is the contains function for dynarrays
    # how would I get the top three votes for officials
    electedOfficials[0]=
    electedOfficials[1]=
    electedOfficials[2]=
    officialVotingPeriod=false


@external
def voteProposal(proposalNumber : uint256):
    for i in self.alreadyVotedProposal:
        assert i != self
    assert self.officialVotingPeriod == True
    self.alreadyVotedProposal.append(self)

@external
def voteOfficial(ballot : address):
    assert wvcVariable.isInActiveStudents(msg.sender) 
    if (officialVotingPeriod):
        assert not self.alreadyVotedOfficials.get_val(msg.sender) == true
        value : unit265
        value = self.votesForOfficials.get_val(ballot) + 1
        self.votesForOfficials.set_val(ballot,value)
        self.alreadyVotedOfficials.set_val(msg.sender,true)