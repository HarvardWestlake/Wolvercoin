# @version ^0.3.7
# relies on only Lottery contract as of June 5 2023

interface ActiveUser:
    def getIsActiveUser(potentialUser: address) -> bool: view
    def getIsAdmin(potentialAdmin: address) -> bool: view

interface Lottery:
    def getPot() -> uint256: view
    def setStartingPot(amount: uint256) : nonpayable

activeUserContract: public(ActiveUser)

lotteryContract: public(Lottery)

admin: HashMap[address, bool]
votingAddress: address
rickyCWallet: address
topicsAddress: public(DynArray[address, 1000])
percentage: uint256 
classSize: uint256
activeStudents: HashMap[address, uint256]

@external
def __init__(erc20address: address):
    self.lotteryContract = Lottery(erc20address)
    self._setRickyC()

# Function 1: students can use Wolvercoin to vote for initiatives; Mr. Theiss's vote can be weighted up to 15% of the total vote:

@external
def vote(voter: address):
    if self._isInTopicsList(voter):
        send(voter, 1)
    if self._checkAdmin(voter) == True:
        send(voter, (15/100)*self.classSize)

@external
def tallyVotes(voter: address) -> bool:
    if self.percentage >= 50:
        self._removeTopics(voter)
        return True
    return False

# Function 2: Only Honors topics students can have WolverCoin at full functionality

# me when vyper doesnt allow storage variables to have an initial value
@internal
def _setRickyC():
    self.rickyCWallet = 0xF7Edc8FA1eCc32967F827C9043FcAe6ba73afA5c # placeholder

@internal
def _getRickyC() -> address:
    return self.rickyCWallet

# uncertain if this belongs in this contract - should eventually be integrated into Token
@external
def withdraw(amount: uint256, requester: address) -> (uint256, String[255]):
    isStudent: bool = self._isInTopicsList(requester)

    if (isStudent):
        return (amount, "nice")
    elif (requester == self.rickyCWallet):
        self.lotteryContract.setStartingPot(self.lotteryContract.getPot() + amount*(19/20))
        return ((1/20)*amount, "Enjoy your joyful pursuit of education!")
    else:
        pass # shhh 
    self.lotteryContract.setStartingPot(self.lotteryContract.getPot() + amount*(1/2))
    return ((1/2)*amount, "should've taken topics")

# Function 3: Honors Topics Student can unanimously vote a non Honors Topics Student to be considered an honors topics student by Wolvercoin or excommunicate an Honors Topics Student from being considered one

@external
def addNonTopics(candidate: address):
    #self.vote() #after or within vote is made to remove/add person
    if self.percentage >= 100: #assuming percentage doesnt change immediately after vote method is called
        self.topicsAddress.append(candidate)

@external
def removeTopics(candidate: address) -> bool:
    return self._removeTopics(candidate)

#intern verison
@internal
def _removeTopics(candidate: address) -> bool:
    if self.percentage >= 100: #assuming percentage doesnt change immediately after vote method is called
        newArr: DynArray[address, 1000] = []
        found: bool = False
        for studentAddress in self.topicsAddress:
            if studentAddress == candidate:
                found = True
            else:
                newArr.append(studentAddress)
        self.topicsAddress = newArr
        return found
    return False

@external
def setPercentage(perc: uint256):
    self.percentage = perc

@external
def addToTopicsList(addend: address) -> DynArray[address, 1000]:
    self.topicsAddress.append(addend)
    return self.topicsAddress

@external
def popTopicList():
    self.topicsAddress.pop()

@external
def getTopicsList()->DynArray[address, 1000]:
    return self.topicsAddress

@external
def getVotingAddress()->address:
    return self.votingAddress

@external 
def isInTopicsList(searching: address) -> bool:
    return self._isInTopicsList(searching)

@external
def checkAdmin(adr: address) -> bool:
    return self._checkAdmin(adr)

@internal
def _checkAdmin(adr: address) -> bool:
    return self.admin[adr]

@external
def makeAdmin(adr: address):
    self.admin[adr] = True

@internal
def _isInTopicsList(searching: address) -> bool:
    for studentAddress in self.topicsAddress:
        if studentAddress == searching:
            return True
    return False

