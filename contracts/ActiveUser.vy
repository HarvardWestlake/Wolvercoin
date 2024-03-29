# @version ^0.3.7
currentGradYear: public(uint256)
userGraduationYear: HashMap[address, uint256]
admins: public(HashMap[address, bool])
isContractWhitelisted: public(HashMap[address, bool])

owner: address
disabled: bool

event SetGradYear:
    user: address
    year: uint256

event AdminAdded:
    admin: address
    label: String[10]

event AdminRemoved:
    admin: address
    label: String[10]

event ContractWhitelisted:
    contract: address

@external
def __init__(_initialAdmin: address):
    """
        @notice Sets the reimburesement and reimburseGas contract
        @param _initialAdmin is a mandatory admin address
    """
    assert _initialAdmin != empty(address)
    self.disabled = False
    self.owner = msg.sender

    self.admins[msg.sender] = True
    self.admins[_initialAdmin] = True

    log AdminAdded(msg.sender, "init owner")
    log AdminAdded(_initialAdmin, "init admin")

@external
def addAdmin(_adminToAdd: address):
    """
        @notice addAdmin function adds a new admin
        @param  _adminToAdd is the admin to input
        can only be called by existing admin / owner
    """
    assert not self.disabled, "This contract is no longer active"
    assert _adminToAdd != empty(address), "Cannot add the 0 address as admin"
    assert self.admins[msg.sender] == True, "You need to be a teacher to add a teacher."
    self.admins[_adminToAdd] = True
    log AdminAdded(_adminToAdd, "add admin")

@external
def addUser(_userToAdd: address):
    self._addUser(_userToAdd)

@internal
def _addUser(_userToAdd: address):
    assert not self.disabled, "This contract and its features are disabled"
    assert _userToAdd != empty(address), "Cannot add the 0 address as a user"
    assert self.admins[msg.sender] == True, "Only admins can add active users"
    self.userGraduationYear[_userToAdd] = self.currentGradYear

@external
def removeAdmin(_adminToRemove: address):
    """
        @notice removeAdmin function adds a new admin
        @param  _adminToRemove is the admin to remove
        can only be called by existing admin / owner
    """
    assert not self.disabled, "This contract is no longer active"
    assert _adminToRemove != empty(address), "Cannot add the 0 address as admin"
    assert self._isAdminOrOwner(msg.sender), "You need to be an admin or owner to add an admin."
    assert self.admins[_adminToRemove] == True, "The person is already not an admin"
    self.admins[_adminToRemove] = False
    log AdminRemoved(_adminToRemove, "remove adm")

@external
def whitelistContract(_contractAddress: address):
    assert not self.disabled, "This contract is no longer active"
    assert _contractAddress != empty(address), "Cannot add the 0 address as a contract"
    assert self._isAdminOrOwner(msg.sender), "You need to be an admin or owner to add a contract."
    self.isContractWhitelisted[_contractAddress] = True
    log ContractWhitelisted(_contractAddress)

@view
@internal
def _isAdminOrOwner(_address : address) -> bool:
    return self.admins[_address] or self.owner == _address

@view
@internal
def _getIsActiveUser(_potentialUser: address) -> bool:
    if (self.userGraduationYear[_potentialUser] <= 0):
        return False
    return self.userGraduationYear[_potentialUser] == self.currentGradYear
  
@view
@internal
def _getIsAdminAndActiveUser(potentialAdminAndActiveUser: address) -> bool:
    isActive: bool = self._getIsActiveUser(potentialAdminAndActiveUser)
    isAdmin: bool = self._isAdminOrOwner(potentialAdminAndActiveUser)
    return isActive and isAdmin
    
@view
@external
def getContractWhitelisted(_contractAddress: address) -> bool:
    return self.isContractWhitelisted[_contractAddress]

@view
@external
def getUserGradYear(_student: address) -> uint256:
    return self.userGraduationYear[_student]

@view
@external
def getIsAdmin(_potentialAdmin: address) -> bool:
    return self._isAdminOrOwner(_potentialAdmin)

@view
@external
def getIsActiveUser(_potentialUser: address) -> bool:
    return self._getIsActiveUser(_potentialUser)
    
@view
@external
def getIsAdminAndActiveUser(potentialAdminAndActiveUser: address) -> bool:
    return self._getIsAdminAndActiveUser(potentialAdminAndActiveUser)

@view 
@external
def getCurrentGradYear() -> uint256:
    return self.currentGradYear

@view
@external
def getIsAlumni(_potentialUser: address) -> bool:
    return self.userGraduationYear[_potentialUser] != self.currentGradYear and self.userGraduationYear[_potentialUser] > 0

@external
def setDisableContract(disabled: bool):
    assert self.owner == msg.sender
    self.disabled = disabled

@external
def setCurrentGradYear(_year: uint256):
    assert not self.disabled, "This contract and its features are currently disabled"
    assert self._isAdminOrOwner(msg.sender), "Only admins can add active students"
    self.currentGradYear = _year
    log SetGradYear(msg.sender, _year) 

@external
def setOwner(_owner : address):
    assert msg.sender == self.owner
    self.owner = _owner

@external
def addBulkUsers(_usersToAdd: DynArray[address, 25]):
    assert not self.disabled, "This contract and its features are currently disabled"
    assert self._isAdminOrOwner(msg.sender), "Only admins can add active students"
    for user in _usersToAdd:
        self._addUser(user)

@view
@external
def getOwner() -> address:
    return self.owner