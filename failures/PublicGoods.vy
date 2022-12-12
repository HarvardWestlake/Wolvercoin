# @version ^0.3.7

# vyper.interfaces.ERC20 does not include the mint and burn functions so we make our own interface
interface ERC20WithAdminAccess:
    def mint(_to: address, _value: uint256): nonpayable
    def burnFrom(_to: address, _value: uint256): nonpayable

struct Donation:
    donator: address
    amount: uint256

struct Good:
    name: String[50]
    goal: uint256
    donations: Donation[50] # Up to 50 people can donate to a good
    donationsLen: int8
    totalDonations: uint256
    creator: address

goods: public(HashMap[String[50], Good]) # There can be up to 50 goods collecting donations
erc20: ERC20WithAdminAccess # The main contract we need to interact with
lastIndex: uint256

@external
def __init__(erc20address: address):
    self.erc20 = ERC20WithAdminAccess(erc20address)
    return

@external
def createGood(name: String[50], goal: uint256):
    # Barebones implementation made by @ericyoondotcom so he could test his own method.
    # Please make this method better

    self.goods[name] = Good({
        name: name,
        goal: goal,
        donations: empty(Donation[50]),
        donationsLen: 0,
        totalDonations: 0,
        creator: msg.sender
    })

    # TODO for @exoskeleton-1729
    
    # Note change from tech spec made by @ericyoondotcom 2022-12-08: goods is now a hashmap
    # The key of the hashmap is the name of the good
    return

@external
def contribute(name: String[50], amount1: uint256):
    # Barebones implementation made by @ericyoondotcom so he could test his own method.
    # Please make this method better
    isPreviousDonor: bool = False 
    for i in range(50):
        if (name[i] == name):
            temp: Donation(name, donations[i].amount + amount1)
            self.donations[i] = temp
            isPreviousDonor = True 
    
    if (isPreviousDonor == False):
        temp: Donation(name, amount1)
        self.name[self.lastIndex] = name
        self.donations[self.lastIndex] = temp
        self.lastIndex += 1

    erc20.burnFrom(msg.sender, amount)
    # TODO for @stevenk8819

    # Change from tech spec: donations are stored as an array of Donation objects
    # Loop through the donations array, find the address of the donation associated
    # with the donator, and increment the value. If user has no associated donation
    # object, create one
    return

@external
def retract(name: String[50], amount: uint256):
    # TODO for @monkeymatt2023

    # See comment above
    return

@external
def complete(name: String[50]):
    assert name != ""
    good: Good = self.goods[name]
    assert msg.sender == good.creator
    assert good.name == name # Essentially a test to see if good exists
    if good.totalDonations < good.goal:
        for i in range(50):
            if i >= good.donationsLen:
                break
            donation: Donation = good.donations[i]
            self.erc20.mint(donation.donator, donation.amount) # Return the donator their money
    self.goods[name] = empty(Good)
    return