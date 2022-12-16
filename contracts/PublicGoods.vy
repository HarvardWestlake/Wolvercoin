# @version ^0.3.7

# vyper.interfaces.ERC20 does not include the mint and burn functions so we make our own interface
interface ERC20WithAdminAccess:
    def getBalanceOf(_address: address) -> uint256: nonpayable
    def transferFrom(_from : address, _to : address, _value : uint256) -> bool: nonpayable
    def approve(_spender : address, _value : uint256) -> bool: nonpayable

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
    assert name != ""
    assert goal > 0
    assert self.goods[name].name != name # Make sure good with same name doesn't already exist
    self.goods[name] = Good({
        name: name,
        goal: goal,
        donations: empty(Donation[50]),
        donationsLen: 0,
        totalDonations: 0,
        creator: msg.sender
    })

@external
def contribute(name: String[50], amount: uint256):
    good: Good = self.goods[name]
    assert good.name == name

    # Fail the function if the user doesn't have enough money
    assert self.erc20.getBalanceOf(msg.sender) >= amount
    self.erc20.transferFrom(msg.sender, self, amount)

    for i in range(50):
        if i >= good.donationsLen:
            break
        if good.donations[i].donator == msg.sender:
            good.donations[i].amount += amount
            good.totalDonations += amount
            return
    
    good.donations[good.donationsLen] = Donation({
        donator: msg.sender,
        amount: amount
    })
    good.donationsLen += 1
    good.totalDonations += amount
    self.goods[name] = good

@external
def retract(name: String[50], amount: uint256):
    # TODO for @monkeymatt2023

    # See comment above
    return

@external
def getContributionTotal(name: String[50]) -> uint256:
    assert name != ""
    good: Good = self.goods[name]
    assert good.name == name
    return good.totalDonations

@external
def getGoal(name: String[50]) -> uint256:
    assert name != ""
    good: Good = self.goods[name]
    assert good.name == name
    return good.goal

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
            self.erc20.approve(self, donation.amount)
            self.erc20.transferFrom(self, donation.donator, donation.amount)
    self.goods[name] = empty(Good)
    return
