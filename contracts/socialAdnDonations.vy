officialVotingPeriod: bool
alreadyVotedProposal: DynArray [address,100]
proposalVotes: DynArray[uint256, 3]

@external
def voteProposal(proposalNumber : uint256):
    for i in self.alreadyVotedProposal:
        assert i == self
    assert self.officialVotingPeriod == True
    self.alreadyVotedProposal.append(self)


