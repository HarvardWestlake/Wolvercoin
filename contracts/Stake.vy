
## interface w/ method that determines if someone is an active user
## interface w/ method that removes Wolvercoin from an account

stakeAmounts: public (HashMap[address,uint256])
bank: public (address)


interface ActiveUser:
    def getActiveUser(potentialUser: address) -> bool: view
    def getAdmin(potentialAdmin: address) -> bool: view

activeUserContract: public(ActiveUser)
@external
def __init__(activeUserAddress: address):
    self.activeUserContract = ActiveUser(activeUserAddress)


@external
def stake (user : address, amountStaked : uint256):
    assert self.activeUserContract.getActiveUser (user)
    self.stakeAmounts[user] = amountStaked
    self.wolvercoinContract.transferFrom (user, self.bank)

