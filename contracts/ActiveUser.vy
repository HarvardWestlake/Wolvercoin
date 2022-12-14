# @version ^0.3.7
currentGradYear: public(uint256)
userGraduationYear: HashMap[address, uint256]
admins: public(HashMap[address, bool])

owner: address
disabled: bool

event SetGradYear:
    user: address
    year: uint256

event AdminAdded:
    admin: address
    label: String[10]

@external
def __init__(initialAdmin: address):
    """
        @notice Sets the reimburesement and reimburseGas contract
        @param initialAdmin is a mandatory admin address
    """
    assert initialAdmin != empty(address)
    self.disabled = False
    self.owner = msg.sender

    self.admins[msg.sender] = True
    self.admins[initialAdmin] = True

    log AdminAdded(msg.sender, "init owner")
    log AdminAdded(initialAdmin, "init admin")

@external
def addAdmin(adminToAdd: address):
    """
        @notice addAdmin function adds a new admin
        @param  adminToAdd is the admin to input
        can only be called by existing admin / owner
    """
    assert not self.disabled, "This contract is no longer active"
    assert adminToAdd != empty(address), "Cannot add the 0 address as admin"
    assert self.admins[msg.sender] == True, "You need to be a teacher to add a teacher."
    self.admins[adminToAdd] = True
    log AdminAdded(adminToAdd, "add admin")


@external
def addUser(userToAdd: address):
    assert not self.disabled, "This contract and its features are disabled"
    assert userToAdd != empty(address), "Cannot add the 0 address as a user"
    assert self.admins[msg.sender] == True, "Only admins can add active users"
    self.userGraduationYear[userToAdd] = self.currentGradYear

@view
@external
def getUserGradYear(student: address) -> uint256:
    return self.userGraduationYear[student]

@view
@external
def getAdmin(potentialAdmin: address) -> bool:
    return self.admins[potentialAdmin]

@view
@external
def getActiveUser(potentialUser: address) -> bool:
    return self.userGraduationYear[potentialUser] == self.currentGradYear

@external
def isAlumni(potentialUser: address) -> bool:
    return True

@external
def setDisableContract(disabled: bool):
    assert self.owner == msg.sender
    self.disabled = disabled

@external
def setCurrentGradYear(year: uint256):
    assert not self.disabled, "This contract and its features are disabled"
    assert self.admins[msg.sender] == True, "Only admins can add active students"
    self.currentGradYear = year
    log SetGradYear(msg.sender, year) 

