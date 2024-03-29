# @version ^0.3.7

# vyper.interfaces.ERC20 does not include the mint and burn functions so we make our own interface
interface ERC20WithAdminAccess:
    def getBalanceOf(_address: address) -> uint256: nonpayable
    def transferFrom(_from : address, _to : address, _value : uint256) -> bool: nonpayable
    def transfer(_to : address, _value : uint256) -> bool: nonpayable
    def approve(_spender : address, _value : uint256) -> bool: nonpayable

interface ERC721WithAdminAccess:
    def ownerOf(_tokenId: uint256) -> address: nonpayable
    def transferFrom(_from: address, _to: address, _tokenId: uint256): nonpayable

interface ActiveUser:
    def getIsActiveUser(potentialUser: address) -> bool: view
    def getIsAdmin(potentialAdmin: address) -> bool: view
    def getIsAdminAndActiveUser(potentialAdminAndUser: address) -> bool: view

struct Donation:
    donator: address
    amount: uint256

struct Good:
    goal: uint256
    name: String[50]
    donations: Donation[50] # Up to 50 people can donate to a good
    donationsLen: uint8
    totalDonations: uint256
    creator: address
    nftTokenId: uint256

goods: public(HashMap[uint256, Good]) # There can be up to 50 goods collecting donations
goodsArr: public(DynArray[uint256, 100]) # A list of the nftTokenIds of all the goods currently active

erc20: ERC20WithAdminAccess
erc721: ERC721WithAdminAccess
activeUser: ActiveUser

@external
def __init__(erc20address: address, erc721address: address, activeUserAddress: address):
    self.activeUser = ActiveUser(activeUserAddress)
    self.erc20 = ERC20WithAdminAccess(erc20address)
    self.erc721 = ERC721WithAdminAccess(erc721address)
    return

@internal
def findIndexOfGoodInGoodsArr(nftTokenId: uint256) -> int256:
    for i in range(100):
        if self.goodsArr[i] == nftTokenId:
            return i
    return -1

@external
def createGood(goal: uint256, nftTokenId: uint256, name: String[50]):
    assert self.activeUser.getIsAdminAndActiveUser(msg.sender)
    assert goal > 0
    assert self.erc721.ownerOf(nftTokenId) == self.erc721.address

    # Move the NFT to the property of this contract for safekeeping
    self.erc721.transferFrom(self.erc721.address, self, nftTokenId)

    self.goods[nftTokenId] = Good({
        goal: goal,
        name: name,
        donations: empty(Donation[50]),
        donationsLen: 0,
        totalDonations: 0,
        creator: msg.sender,
        nftTokenId: nftTokenId
    })
    self.goodsArr.append(nftTokenId)

@external
def contribute(nftTokenId: uint256, amount: uint256):
    good: Good = self.goods[nftTokenId]
    assert good.nftTokenId == nftTokenId

    # Fail the function if the user doesn't have enough money
    assert self.erc20.getBalanceOf(msg.sender) >= amount
    self.erc20.transferFrom(msg.sender, self, amount)

    for i in range(50):
        if i >= good.donationsLen:
            break
        if good.donations[i].donator == msg.sender:
            good.donations[i].amount += amount
            good.totalDonations += amount
            self.goods[nftTokenId] = good
            return
    
    good.donations[good.donationsLen] = Donation({
        donator: msg.sender,
        amount: amount
    })
    good.donationsLen += 1
    good.totalDonations += amount
    self.goods[nftTokenId] = good

@external
def retract(nftTokenId: uint256, amount1: uint256):
    good: Good = self.goods[nftTokenId]
    assert good.nftTokenId == nftTokenId

    for i in range(50):
        if i >= good.donationsLen:
            break
        if (good.donations[i].donator == msg.sender):
            if (amount1 <= good.donations[i].amount):
                donation: Donation = good.donations[i]
                self.erc20.approve(self, amount1)
                self.erc20.transferFrom(self, donation.donator, amount1)
                good.donations[i].amount -= amount1
                good.totalDonations -= amount1
                self.goods[nftTokenId] = good
                break
    return

@external
def complete(nftTokenId: uint256):
    good: Good = self.goods[nftTokenId]
    assert msg.sender == good.creator
    assert good.nftTokenId == nftTokenId # Essentially a test to see if good exists

    if good.totalDonations < good.goal:
        # Refund all the donations and transfer the NFT back
        self.erc721.transferFrom(self, self.erc721.address, good.nftTokenId)
        for i in range(50):
            if i >= good.donationsLen:
                break
            donation: Donation = good.donations[i]
            self.erc20.transfer(donation.donator, donation.amount)
    self.goods[nftTokenId] = empty(Good)
    
    # remove the index 
    i: int256 = self.findIndexOfGoodInGoodsArr(nftTokenId)
    if i != -1:
        self.goodsArr[i] = self.goodsArr[len(self.goodsArr) - 1] # Make the last element take the one you want to remove's place...
        self.goodsArr.pop() # ...and then remove the last element

@view
@external
def getActiveGoods() -> DynArray[uint256, 100]:
    return self.goodsArr

#region Trivial getters
@view
@external
def getContributionTotal(nftTokenId: uint256) -> uint256:
    good: Good = self.goods[nftTokenId]
    assert good.nftTokenId == nftTokenId
    return good.totalDonations

@view
@external
def getGoal(nftTokenId: uint256) -> uint256:
    good: Good = self.goods[nftTokenId]
    assert good.nftTokenId == nftTokenId
    return good.goal

@view
@external
def getName(nftTokenId: uint256) -> String[50]:
    good: Good = self.goods[nftTokenId]
    assert good.nftTokenId == nftTokenId
    return good.name

@view
@external
def getNumDonators(nftTokenId: uint256) -> uint8:
    good: Good = self.goods[nftTokenId]
    assert good.nftTokenId == nftTokenId
    return good.donationsLen

@view
@external
def getCreator(nftTokenId: uint256) -> address:
    good: Good = self.goods[nftTokenId]
    assert good.nftTokenId == nftTokenId
    return good.creator
