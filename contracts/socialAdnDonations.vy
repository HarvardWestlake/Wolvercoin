# @version ^0.3.7
# code is dependent on activeUser
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



@external
def endVoteOfficial():
    assert self.activeUserContract.getAdmin(block.coinbase)   
    self.officialVotingPeriod = False


@external
def voteProposal(proposalNumber : uint256):
   def voteProposal(proposalNumber : uint256):
    assert proposalNumber <= 2  
    assert proposalNumber >= 0
    for i in self.alreadyVotedProposal:
        assert i != self
    assert self.officialVotingPeriod == True
    self.proposalVotes [proposalNumber] = self.proposalVotes [proposalNumber] + 1 
    self.alreadyVotedProposal.append(self)



# doesn't work- commenting out for now
# external
# def donate(_from : address, _to : address, _value : uint256) -> bool:
   # """
   #  @dev Transfer tokens from one address to another.
   #  @param _from address The address which you want to send tokens from
   #  @param _to address The address which you want to transfer to
   #  @param _value uint256 the amount of tokens to be transferred
   # """
    # NOTE: vyper does not allow underflows
    #       so the following subtraction would revert on insufficient balance
    # self.balanceOf[_from] -= _value
    # self.balanceOf[_to] += _value
    # NOTE: vyper does not allow underflows
    #      so the following subtraction would revert on insufficient allowance
    # self.allowance[_from][msg.sender] -= _value
    # log Transfer(_from, _to, _value)
    # return True

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
        
