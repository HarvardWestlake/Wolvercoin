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
bank: (address)
totalOfTransactions: uint256


@external
def __init__ (activeUserAddress: address):
    self.activeYear = 2023
    self.activeUserContract = ActiveUser(activeUserAddress)
    self.officialVotingPeriod = True
    self.proposalVotes=[0,0,0]

#NO TEST
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
@external
def getProposalVotes (num : uint256) -> (uint256):
    return self.proposalVotes[num]

#def donate(to: Address, value: uint256):
    # Check if the caller has sufficient balance
   # assert self.balanceOf[msg.sender] >= value, "Insufficient balance"
 
    # Transfer the funds
    #self.balanceOf[msg.sender] -= value
    #self.balanceOf[to] += value

#NO TEST
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
            # we need to change these bottom ones to change the addresses 
            self.electedOfficials[2]= electedOfficials[1] 
            self.electedOfficials[1]= electedOfficials[0]
            self.electedOfficials[0] = ballot
        elif self.votesForOfficials[ballot] >= electedOfficials[1]:
            self.electedOfficials[2]=electedOfficials[1]
            self.electedOfficials[1]= ballot
        elif self.votesForOfficials[ballot] >= electedOfficials[2]:
            self.electedOfficials[2] = ballot

#NO TEST AND WRONG     
#UNISWAP: constant(address) = 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D
#SUSD: constant(address) = 0x970C963166351B901c642B8CB49920536C3127e6
#@internal 
#def take10percent() -> uint256:
#    return 100
#investment: address
#@external
#def deposit10Percent(_provider: address)->bool:
#    self.investment=_provider
#    amount: uint256 =self.take10percent()
#    self.balanceOf[self.bank] -= amount
#    self.balanceOf[_provider] += amount
# NOTE: vyper does not allow underflows
# so the following subtraction would revert on insufficient allowance
#    self.allowance[self.bank][msg.sender] -= amount
#    log Transfer(self.bank, _provider, amount)
#    return True

