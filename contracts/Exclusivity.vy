# @version 0.3.7


percentage: uint256
topicsAddress: public(DynArray[address, 1000])

@internal
def vote():
    pass

@external
def addNonTopics(candidate: address):
    self.vote() #function 1 in tech spec, to be written by someone else
    if self.percentage>=100:#assuming percentage doesnt change immediately after vote method is called
        self.topicsAddress.append(candidate)

@external
def removeNonTopics(candidate: address):
    self.vote() #function 1 in tech spec, to be written by someone else
    if self.percentage>=100:#assuming percentage doesnt change immediately after vote method is called
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