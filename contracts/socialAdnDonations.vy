# @version ^0.3.7
# code is dependent on activeUser
interface ActiveUser:
    def getActiveUser(potentialUser: address) -> bool: view
    def getAdmin(potentialAdmin: address) -> bool: view

activeStudents: public(HashMap[address, uint256])
activeYear: public( uint256 )
teachers: public(HashMap[address, bool]) 
electedOfficials: public(HashMap[address, uint256])
votesLeaderBoard: public(uint256[3])
alreadyVotedOfficials: public(HashMap [address, bool])
votesForOfficials: public(HashMap [address, uint256])
officialVotingPeriod: public(bool)
alreadyVotedProposal: public(DynArray [address,100])
proposalVotes: public(DynArray[uint256, 3])
activeUserContract: public(ActiveUser)



@external
def __init__ (activeUserAddress: address):
    self.activeYear = 2023
    self.activeUserContract = ActiveUser(activeUserAddress)



@external
def endVoteOfficial():
    assert self.activeUserContract.getAdmin(block.coinbase)   
    self.officialVotingPeriod = False


@external
def voteProposal(proposalNumber : uint256):
    for i in self.alreadyVotedProposal:
        assert i == self
    assert self.officialVotingPeriod == True
    self.alreadyVotedProposal.append(self)

@external
def voteOfficial( ballot : address ):
    assert self.activeUserContract.getActiveUser(msg.sender) 
    if (self.officialVotingPeriod):
        assert not self.alreadyVotedOfficials[msg.sender] == True
        value : uint256 =  self.votesForOfficials[ballot] + 1 
        self.votesForOfficials[ballot]=value
        self.alreadyVotedOfficials[msg.sender]= True
        if self.votesForOfficials[ballot] >= self.votesLeaderBoard[0]:
            self.votesLeaderBoard[2]= votesLeaderBoard[1]
            self.votesLeaderBoard[1]= votesLeaderBoard[0]
            self.votesLeaderBoard[0]= value
            # we need to change these bottom ones to change the addresses 
            self.electedOfficials[2]= electedOfficials[1] 
            self.electedOfficials[1]= electedOfficials[0]
            self.electedOfficials[0] = ballot
        elif self.votesForOfficials[ballot] >= electedOfficials[1]:
            self.electedOfficials[2]=electedOfficials[1]
            self.electedOfficials[1]= ballot
        elif self.votesForOfficials[ballot] >= electedOfficials[2]:
            self.electedOfficials[2] = ballot
        
