interfaceWolvercoin: 
    def isInActiveStudents()

activeStudents: public(Hashmap[address, uint256])
activeYear: public( uint256 )
teachers: public(HashMap[address, boolean]) # hashmap?
electedOfficials: public(DynArray[address, 3])
alreadyVotedOfficials: public(HashMap [address, boolean])
votesForOfficials: public(HashMap [address, uint256])
officialVotingPeriod: public(boolean)
wvcVariable: Wolvercoin


@external
def __init__ ():
    self.activeYear = 2023


@external
def endVoteOfficial():
    assert wvcVariable.isTeacher(block.coinbase)   # what is the contains function for dynarrays
    # how would I get the top three votes for officials
    electedOfficials[0]=
    electedOfficials[1]=
    electedOfficials[2]=
    officialVotingPeriod=false



