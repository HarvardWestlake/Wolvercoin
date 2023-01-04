# THIS CODE DOES NOT WORK
"""
# @external
def finishVote(contract: address): 
    assert not self.disabled, "This contract is no longer active"
    assert self.endBlock[contract] != 0 and block.number >= self.endBlock[contract]

    amtStaked: uint256 = self.activePropositions[contract]
    array: DynArray[address,1024] = self.peopleInvested[contract]
    if (self.affectsDao[contract] == False and self.voterCoinStaked < amtStaked * 2 and self.totalSupply < amtStaked * 5) or (self.totalSupply * 3 < amtStaked * 4):
        self.totalSupply -= self.activePropositions[contract] / 2
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
    self.balanceOf[voterAddress] += self.amountInFavor[self.returnedWinner][voterAddress]/2
    self.totalSupply -= self.amountInFavor[self.returnedWinner][voterAddress]/2

@internal
def returnCoin(proposition: address, voterAddress: address):
    assert not self.disabled, "This contract is no longer active"
    assert voterAddress != empty(address), "Cannot add the 0 address as vote subject"
    self.balanceOf[voterAddress] += self.amountInFavor[proposition][voterAddress]
"""