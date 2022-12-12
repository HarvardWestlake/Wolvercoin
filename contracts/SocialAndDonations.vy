# @version 0.3.7

# Tech Spec Variables:
# Community Pot -> Address
# Active Students -> HashMap(wallet -> grade year) ## by "wallet" does the spec mean "address"? I assume so...
# activeYear -> uint256
# teachers -> dynarray (of addresses? not specified but I assume...)
# creator -> address

# electedOfficials -> dynarray (of addresses)
# alreadyVotedOfficials -> dynarray (of addresses)
# ARE THESE TWO NOT THE SAME!? 
# for this reason, I am rewriting:
# potentialElectedOfficials -> dynarray (of addresses)
# electedOfficials -> dynarray (of addresses)

# votesForOfficials -> hashMap(address -> unit256)
# officialVotingPeriod -> boolean

# Address for community pot
communityPot: public(address)
# hashmap of active students
activeStudents: public(HashMap[address, uint256])
# year of current students
activeYear: public(uint256)
# list of teachers
teachers: public(DynArray[address, 1024])
# creator address
creator: public(address)
# list of candidates
potentialElectedOfficials: public(DynArray[address, 1024])
# list of admin
electedOfficials: public(DynArray[address, 1024])
# hash map keeping track of vote tally
votesForOfficials: public(HashMap[address, uint256])
# boolean for whether or not it is the voting period
officialVotingPeriod: public(bool)

def determineResult():
    uint256 max = votesForOfficials[potentialElectedOfficials[0]]
    address bestCandidate = potentialElectedOfficials[0]

    for candidate in potentialElectedOfficials:
        uint256 votes = votesForOfficials[candidate]
        if votes > max:
            max = votes
            bestCandidate = candidate
    
    electedOfficials.add(bestCandidate)
        

