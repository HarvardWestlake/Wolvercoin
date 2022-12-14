# @version 0.3.7


percentage: uint256
topicsAddress: public(DynArray[address, 1000])

@internal
def vote():
    pass

@external
def addNonTopics(candidate: address):
    self.vote() #function 1 in tech spec, to be written by someone else
    if self.percentage>=1:#assuming percentage doesnt change immediately after vote method is called
        self.topicsAddress.append(candidate)

@external
def removeNonTopics(candidate: address):
    self.vote() #function 1 in tech spec, to be written by someone else
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

@external
def addToTopicsList(addend: address):
    self.topicsAddress.append(addend)

@external
def getTopicsList()->DynArray[address,1000]:
    return self.topicsAddress





