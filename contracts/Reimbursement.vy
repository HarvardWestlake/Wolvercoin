# @version ^0.3.7

userIndividualWeiReimbursementCap: public(uint256)
userWeiReimbursed: HashMap[address, uint256]
WEI_REIMBURSEMENT_BUFFER: constant(uint256) = as_wei_value(0.0005, "ether")
disabled: bool
owner: address

interface ActiveUser:
    def getActiveUser(potentialUser: address) -> bool: view
    def getAdmin(potentialAdmin: address) -> bool: view

activeUserAddress: public(ActiveUser)

event GasReimburse:
    recipient: address
    amount: uint256
    maxAllowed: uint256
    totalReimbursed: uint256

event ContractOutOfGas:
    recipient: address
    amountNotReimbursed: uint256

event Payment:
    sender: indexed(address)
    amount: uint256
    bal: uint256

@external
def __init__(activeUserAddress: address):
    """
        @notice Sets the reimburesement and reimburseGas contract
        @param activeUserAddress is a mandatory address of the activeUsers contract
    """
    self.activeUserAddress = ActiveUser(activeUserAddress)
    self.owner = msg.sender
    self.disabled = False
    self.userIndividualWeiReimbursementCap = as_wei_value(0.01, "ether")


@payable
@external
def __default__():
    """
        @notice Default function is executed on a call to the contract if a non-existing function is called
        or if none is supplied at all, such as when someone sends it Eth directly
        Payable functions can receive Ether and read from and write to the contract state
    """
    log Payment(msg.sender, msg.value, self.balance)

@internal
def _reimburseGas(recipient: address, amount: uint256):
    """
        @notice reimburse the user wei
        @param  recipient address to reimburse
          Verifies they are a current user
          Checks contract has enough Wei to reimburse
          Records total per-user reimbursement amount
          Need to grab msg.gas before and msg.gas after to find amount
    """
    assert not self.disabled, "This contract and its features are disabled"

    # Will not reimburse graduates...
    if not self.activeUserAddress.getActiveUser(recipient):
        return
    
    if self.balance < (WEI_REIMBURSEMENT_BUFFER + amount):
        log ContractOutOfGas(recipient, amount)
        return

    if self.userIndividualWeiReimbursementCap >= (self.userWeiReimbursed[recipient] + amount):
        self.userWeiReimbursed[recipient] += amount
        send(recipient, amount)
    
    log GasReimburse(
        recipient, 
        amount,
        self.userIndividualWeiReimbursementCap, 
        self.userWeiReimbursed[recipient]
    )


@external
def reimburseGas(recipient: address):
    self._reimburseGas(recipient, tx.gasprice)


@external
def setDisableContract(disabled: bool):
    assert self._isOwnerOrAdmin() == True, "Only admin or owner can disable the contract"
    self.disabled = disabled

@internal
def _isOwnerOrAdmin() -> bool:
    isOwner: bool = (self.owner == msg.sender)
    isAdmin: bool = self.activeUserAddress.getAdmin(msg.sender)
    return isOwner or isAdmin

@external
def setUserIndividualWeiReimbursementCap(cap: uint256):
    assert not self.disabled, "This contract and its features are disabled"
    assert self._isOwnerOrAdmin() == True, "Only admin or owner can disable the contract"
    self.userIndividualWeiReimbursementCap = cap

@view
@external
def getWeiReimbursed(dummy: bool) -> uint256:
    return self.userWeiReimbursed[msg.sender]

@view
@external
def getUserInidividualWeiReimbursementCap() -> uint256:
    return self.userIndividualWeiReimbursementCap

@view
@external 
def getOwner() -> address:
    return self.owner