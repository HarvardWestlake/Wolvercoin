# @version ^0.3.3

interface Wolvercoin:
    def transfer(_to : address, _value : uint256) -> bool: view
    def getBalanceOf (_user: address) -> uint256: view

wolvercoinContract: public(Wolvercoin)
theissHighScore: uint256
users: HashMap[address, uint256]

@external
def __init__(wolvercoinAddress: address):
    self.wolvercoinContract = Wolvercoin(wolvercoinAddress)
    self.theissHighScore = 72
    self.users[msg.sender] = 0

# PLEASE READ - this method is reliant on SideQuests getting into main first
# That is a task listed on the project board. ONCE that has occurred please do the following:
# Remove the comment markers on lines 27 and 28. This will make the method actually work.
# Then, delete line 29, which is a placeholder (that still technically does what it needs to)
# The methods are thus placeholders awaiting the finishing of SideQuests.

@external
def compareHighScores (name: address, score: uint256) -> String[100]:
    if self.users[name] == 0:
        if score > self.theissHighScore:
            #self.wolvercoinContract.transfer(name, 2*(self.wolvercoinContract.getBalanceOf(msg.sender)))
            #self.users[name] = 2*(self.wolvercoinContract.getBalanceOf(msg.sender))
            self.users[name] = 42
            return "You beat Mr. Theiss! Epic Gamer Moment!"
        else:
            return "You did not beat Mr. Theiss."
    else:
        return "You cannot beat Mr. Theiss more than once."

@external
def getHighScore() -> uint256:
    return self.theissHighScore
