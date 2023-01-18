# @version ^0.3.7
## interfaces w/ ActiveUser and Wolvercoin
## anything that requires staking will interface with this class

#interfaces with ActiveUser contract
interface ActiveUser:
    def getIsActiveUser(potentialUser: address) -> bool: view
    def getIsAdmin(potentialAdmin: address) -> bool: view

activeUserAddress: public(ActiveUser)

allHaikus: HashMap[address, String[170]]

event HaikuSubmitted:
    userAddress: address
    submittedHaiku: String[170]

@external
def __init__ (activeUserAddress: address):
    self.activeUserAddress = ActiveUser (activeUserAddress)

# submits haiku to allHaikus
@external
def submitHaiku (activeUserAddress: address, haikuSubmission: String[170]):
    self.activeUserAddress = ActiveUser(activeUserAddress)
    self.allHaikus[activeUserAddress] = haikuSubmission 
    log HaikuSubmitted (activeUserAddress, haikuSubmission)

@view
@external
def getHaiku (activeUserAddress: address) -> String[170]:
    return self.allHaikus[activeUserAddress]
