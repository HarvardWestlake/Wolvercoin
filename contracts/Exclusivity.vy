# @version ^0.3.7
# this relies on functional ActiveUser contract/class
# no other contract is interfacing with this code as of 12/12 at 9:00AM
interface ActiveUser:
    def getActiveUser(potentialUser: address) -> bool: view
    def getAdmin(potentialAdmin: address) -> bool: view
    
activeUserContract: public(ActiveUser)

admin: HashMap[address, bool]
topicsAddress: DynArray[address, 1000]
percentage: uint256
classSize: uint256
@external
def vote(voter: address):
    isIn: bool = False
    for studentAddress in self.topicsAddress: #find index of address of candidate in topics addresses
            if studentAddress==voter:    
                isIn = True
                break
    if isIn == True:
        self._removeNonTopics(voter)
        send(voter,1)
    if self.admin[voter]:
     
        send(voter,(15/100)*self.classSize)

@external
     
def tallyVotes(voter: address)-> bool:
    if self.percentage >= 50:
        self._removeNonTopics(voter)
        return True
    return False

@external
def addNonTopics(candidate: address):
    #self.vote() #after or within vote is made to remove/add person
    if self.percentage>=100:#assuming percentage doesnt change immediately after vote method is called
        self.topicsAddress.append(candidate)

@external
def removeNonTopics(candidate: address):
    self._removeNonTopics(candidate)

#intern verison
@internal
def _removeNonTopics(candidate: address):
    #self.vote() #after or within vote is made to remove/add person
    if self.percentage>=100:#assuming percentage doesnt change immediately after vote method is called
        count: int256=-1
        found: bool=False
        for studentAddress in self.topicsAddress: #find index of address of candidate in topics addresses
            count=count+1
            if studentAddress==candidate:
                found=True
                break
        
        if found: #from google, allegedly removes thing at index
            self.topicsAddress[count] = self.topicsAddress[len(self.topicsAddress) - 1]
            self.topicsAddress.pop()


@external
def setPercentage(perc: uint256):
    self.percentage=perc

@external
def addToTopicsList(addend: address):
    self.topicsAddress.append(addend)

@external
def popTopicList():
    self.topicsAddress.pop()

@external
def getTopicsList()->DynArray[address,1000]:
    return self.topicsAddress

@external 
def isInTopicsList(searching:address)->bool:
    added: bool=False
    for studentAddress in self.topicsAddress:
        if studentAddress==searching:
            added=True
            break
    return added

@external
def isNotinTopicsList(searching:address)->bool:
    added: bool=True
    for studentAddress in self.topicsAddress:
        if studentAddress==searching:
            added=False
            break
    return added



