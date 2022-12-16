# @version ^0.3.7
# code is dependent on activeUser
from vyper.interfaces import ERC20

interface ActiveUser:
    def getActiveUser(potentialUser: address) -> bool: view
    def getAdmin(potentialAdmin: address) -> bool: view

activeStudents: public(HashMap[address, uint256])
activeYear: public( uint256 )
teachers: public(HashMap[address, bool]) 
electedOfficials: public(address[3])
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
    self.officialVotingPeriod = True
    self.proposalVotes=[0,0,0]



@external
def endVoteOfficial():
    assert self.activeUserContract.getAdmin(block.coinbase)   
    self.officialVotingPeriod = False


@external
def voteProposal(proposalNumber : uint256):
    assert proposalNumber <= 2  
    assert proposalNumber >= 0
    for i in self.alreadyVotedProposal:
        assert i != self
    assert self.officialVotingPeriod == True
    self.proposalVotes [proposalNumber] = self.proposalVotes [proposalNumber] + 1 
    self.alreadyVotedProposal.append(self)

    return self.proposalVotes[num]
def getProposalVotes (num : uint256) -> (uint256):
@external

#def donate(to: Address, value: uint256):
    # Check if the caller has sufficient balance
   # assert self.balanceOf[msg.sender] >= value, "Insufficient balance"
 
    # Transfer the funds
    #self.balanceOf[msg.sender] -= value
    #self.balanceOf[to] += value

@external
def voteOfficial( ballot : address ):
    assert self.activeUserContract.getActiveUser(msg.sender) 
    if (self.officialVotingPeriod):
        assert not self.alreadyVotedOfficials[msg.sender] == True
        value : uint256 =  self.votesForOfficials[ballot] + 1 
        self.votesForOfficials[ballot]=value
        self.alreadyVotedOfficials[msg.sender]= True
        if self.votesForOfficials[ballot] >= self.votesLeaderBoard[0]:
            self.votesLeaderBoard[2]= self.votesLeaderBoard[1]
            self.votesLeaderBoard[1]= self.votesLeaderBoard[0]
            self.votesLeaderBoard[0]= value
            self.electedOfficials[2]= self.electedOfficials[1] 
            self.electedOfficials[1]= self.electedOfficials[0]
            self.electedOfficials[0] = ballot
        elif self.votesForOfficials[ballot] >= self.votesLeaderBoard[1]:
            self.votesLeaderBoard[2]= self.votesLeaderBoard[1]
            self.votesLeaderBoard[1]= value
            self.electedOfficials[2]= self.electedOfficials[1]
            self.electedOfficials[1]= ballot
        elif self.votesForOfficials[ballot] >= self.votesLeaderBoard[2]:
            self.votesLeaderBoard[2]= value
            self.electedOfficials[2] = ballot
        

    # Transfer the funds
    self.balanceOf[msg.sender] -= value
    self.balanceOf[to] += value

>>>>>>> Stashed changes
