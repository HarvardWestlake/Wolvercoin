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
# number of students
numStudents: public(uint256)

@external
def __init__():
    self.officialVotingPeriod = True
    self.potentialElectedOfficials = []
    self.electedOfficials = []

@external
def getVotes(account : address) -> uint256:
    return self.votesForOfficials[account]

@external
def determineResult() -> address:

    largest : uint256 = 0

    voteCounts : DynArray[uint256, 10] = []

    # NOTE: community pot should NEVER win. this is just a placeholder
    bestCandidate : address = self.communityPot

    if len(self.potentialElectedOfficials) > 0:
        largest = self.votesForOfficials[self.potentialElectedOfficials[0]]
        bestCandidate = self.potentialElectedOfficials[0]

    for candidate in self.potentialElectedOfficials:
        votes : uint256 = self.votesForOfficials[candidate]
        voteCounts.append(votes)
        if votes >= largest:
            largest = votes
            bestCandidate = candidate

    self.electedOfficials.append(bestCandidate)
    return bestCandidate

## BEYOND THIS POINT, ALL METHODS ARE SOLELY FOR TESTING PURPOSES AND ARE NOT THE OFFICIAL METHODS
## AGAIN, THESE ARE PROTOTYPES

@external
def getElectedOfficials() -> DynArray[address, 1024]:
    return self.electedOfficials

@external
def getLengthOfPotential() -> uint256:
    return len(self.potentialElectedOfficials)

@external
def addPotentialOfficial(account : address):
    if(self.activeStudents[account] != 0):
        self.potentialElectedOfficials.append(account)
        self.votesForOfficials[account] = 0

@external
def addStudent(wallet: address, gradYear: uint256):
    self.activeStudents[wallet] = gradYear
    self.numStudents = self.numStudents + 1

@external
def getLengthOfStudents() -> uint256:
    return self.numStudents

@external
def checkIfActive (wallet: address) -> bool:
    return (self.activeStudents[wallet] != 0)

@external
def vote(account : address):
    self.votesForOfficials[account] += 1

@external
def beginVoteOfficial(user: address) -> (bool):
    isTeacher: bool = False
    for i in self.teachers:
        if (i == user):
            isTeacher = True
            assert self.officialVotingPeriod == True  
        else:
            isTeacher = False
    return isTeacher
            
@external
def getOfficalVotingPeriod() -> (bool):
    return self.officialVotingPeriod
@external
def getTeachers() -> (address):
    return self.teachers[0]
@external 
def getElectedOffical() -> (address):
    return self.electedOfficials[0]



####################################################################################################
