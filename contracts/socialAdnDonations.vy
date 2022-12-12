officialVotingPeriod: bool
alreadyVotedProposal: DynArray [address,100]
proposalVotes: DynArray[uint256, 3]

@external
def voteProposal(proposalNumber : uint256):
    for i in self.alreadyVotedProposal:
        assert i == self
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