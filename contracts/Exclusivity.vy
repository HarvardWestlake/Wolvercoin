# @version 0.3.7
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

@internal
def vote(voter: address):
    isIn: bool = False
    for studentAddress in self.topicsAddress: #find index of address of candidate in topics addresses
            if studentAddress==voter:
                isIn = True
                break
    if isIn == True:
        self.removeNonTopics(voter)
        send(voter,1)
     
    if self.admin[voter]:
        send(voter,(15/100)*self.classSize)

@external
def tallyVotes(voter: address)-> bool:
     if self.percentage >= 50:
        self.removeNonTopics(voter)
        return True
     return False

@external
def addNonTopics(candidate: address):
    self.vote(candidate) #function 1 in tech spec, to be written by someone else
    if self.percentage>=1:#assuming percentage doesnt change immediately after vote method is called
        self.topicsAddress.append(candidate)

@internal
def removeNonTopics(candidate: address):
    #self.vote() #function 1 in tech spec, to be written by someone else
    if self.percentage>=1:#assuming percentage doesnt change immediately after vote method is called
        count: int256=0
        found: bool=False
        for studentAddress in self.topicsAddress: #find index of address of candidate in topics addresses
            count=count+1
            if studentAddress==candidate:
                found=True
                break
        if found: #from google, allegedly removes thing at index
            self.topicsAddress[count] = self.topicsAddress[len(self.topicsAddress) - 1]
            self.topicsAddress.pop()
            





