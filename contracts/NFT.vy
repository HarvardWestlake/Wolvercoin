# @version ^0.3.7
# @dev Implementation of ERC-721 non-fungible token standard.
# @author Ryuya Nakamura (@nrryuya)
# Modified from: https://github.com/vyperlang/vyper/blob/de74722bf2d8718cca46902be165f9fe0e3641dd/examples/tokens/ERC721.vy
# Again from: https://github.com/vykintasmak/vyper-nft-example/blob/main/contracts/ERC721_OpenSea.vy
# https://etherscan.io/address/0xa5ea010a46EaE77bD20EEE754f6D15320358dfD8#code


from vyper.interfaces import ERC20
from vyper.interfaces import ERC165
from vyper.interfaces import ERC721

implements: ERC721
implements: ERC165

# Interface for the contract called by safeTransferFrom()
interface ERC721Receiver:
    def onERC721Received(
            _operator: address,
            _from: address,
            _tokenId: uint256,
            _data: Bytes[1024]
        ) -> bytes4: nonpayable


# @dev Emits when ownership of any NFT changes by any mechanism. This event emits when NFTs are
#      created (`from` == 0) and destroyed (`to` == 0). Exception: during contract creation, any
#      number of NFTs may be created and assigned without emitting Transfer. At the time of any
#      transfer, the approved address for that NFT (if any) is reset to none.
# @param _from Sender of NFT (if address is zero address it indicates token creation).
# @param _to Receiver of NFT (if address is zero address it indicates token destruction).
# @param _tokenId The NFT that got transfered.
event Transfer:
    sender: indexed(address)
    receiver: indexed(address)
    tokenId: indexed(uint256)

# @dev This emits when the approved address for an NFT is changed or reaffirmed. The zero
#      address indicates there is no approved address. When a Transfer event emits, this also
#      indicates that the approved address for that NFT (if any) is reset to none.
# @param _owner Owner of NFT.
# @param _approved Address that we are approving.
# @param _tokenId NFT which we are approving.
event Approval:
    owner: indexed(address)
    approved: indexed(address)
    tokenId: indexed(uint256)

# @dev This emits when an operator is enabled or disabled for an owner. The operator can manage
#      all NFTs of the owner.
# @param _owner Owner of NFT.
# @param _operator Address to which we are setting operator rights.
# @param _approved Status of operator rights(true if operator rights are given and false if
# revoked).
event ApprovalForAll:
    owner: indexed(address)
    operator: indexed(address)
    approved: bool


# @dev Mapping from NFT ID to the address that owns it.
idToOwner: HashMap[uint256, address]

# @dev Mapping from NFT ID to approved address.
idToApprovals: HashMap[uint256, address]

# @dev Mapping from owner address to count of his tokens.
ownerToNFTokenCount: HashMap[address, uint256]

# @dev Mapping from owner address to mapping of operator addresses.
ownerToOperators: HashMap[address, HashMap[address, bool]]

# @dev Address of minter, who can mint a token
minter: address

# @dev Hacky helper convert int to string
IDENTITY_PRECOMPILE: constant(address) = 0x0000000000000000000000000000000000000004

# == Wolvercoin specific NFT fields ==
# == Wolvercoin specific NFT fields ==

# What grad year the nft collection is for
gradYear : uint256

# Check for active user and grad year
interface ActiveUser:
    def getCurrentGradYear() -> uint256: view
    def getIsActiveUser(potentialUser: address) -> bool: view
    def getIsAdmin(potentialAdmin: address) -> bool: view
activeUserContract : public(ActiveUser)


# Creates a unique ID from the hash to make sure there are no two the same
# Maps it to a token ID so UniqueHash => TokenId
uniqueHashesForToken: HashMap[bytes32, uint256]
tokenURIs: HashMap[uint256, String[64]]
password: uint256


# Total NFT minted 
tokenCount: public(uint256)

# ERC721 metadata
name: public(String[64])
symbol: public(String[32])
baseURI: String[32]
contract_uri: String[66]



# @dev Static list of supported ERC165 interface ids
SUPPORTED_INTERFACES: constant(bytes4[5]) = [
    0x01FFC9A7,  # ERC165
    0x80AC58CD,  # ERC721
    0x150B7A02,  # ERC721TokenReceiver
    0x780E9D63,  # ERC721Enumerable
    0x5B5E139F,  # ERC721Metadata
]

# For testing this can manually set the 'auctionContract' who will own all the NFTs after mint
# Eventuall want to update this to automatically mint to the auctionContract or at least approveIt... 
# . Actually should probably only approve the auctionContract
# Need to only allow 'actuveUsers to mint'
# Remove password after ActuveUsers works
# Set password to something basic for start '12345'
@external
def __init__(_password: uint256):  # activeUserContractAddress: address):
    """
    @dev Contract constructor.
    """
    self.name = "Not-So-Fungible Wolvies"
    self.symbol = "NSFW"
    self.minter = msg.sender
    self.baseURI = "http://ipfs.wolvercoin.com/ipfs/"
    self.tokenCount = 0
    self.password = _password
    #self.activeUserContract = ActiveUser(activeUserContractAddress)


@pure
@external
def supportsInterface(interface_id: bytes4) -> bool:
    """
    @notice Query if a contract implements an interface.
    @dev Interface identification is specified in ERC-165.
    @param interface_id Bytes4 representing the interface.
    @return bool True if supported.
    """

    return interface_id in SUPPORTED_INTERFACES


@external
def safeMintToThisContractWithApprovalToExternalContractUsingPassword(_auctionAddress: address, _tokenMetaDataUri: String[64], _password: uint256) -> uint256:

    assert self.password == _password

    # assert token does not exist uniqueHashesForToken
    uniqueHash: bytes32 = keccak256(_abi_encode(_tokenMetaDataUri))
    assert self.uniqueHashesForToken[uniqueHash] == 0, "token is non-unique"

    self._addTokenTo(_auctionAddress, self.tokenCount)
    self._addTokenURI(self.tokenCount, _tokenMetaDataUri)
    log Transfer(empty(address), _auctionAddress, self.tokenCount)
    self.tokenCount += 1
    return self.tokenCount

### VIEW FUNCTIONS ###

@view
@external
def balanceOf(_owner: address) -> uint256:
    """
    @dev Returns the number of NFTs owned by `_owner`.
         Throws if `_owner` is the zero address. NFTs assigned to the zero address are considered invalid.
    @param _owner Address for whom to query the balance.
    """
    assert _owner != empty(address)
    return self.ownerToNFTokenCount[_owner]


@view
@external
def ownerOf(_tokenId: uint256) -> address:
    """
    @dev Returns the address of the owner of the NFT.
         Throws if `_tokenId` is not a valid NFT.
    @param _tokenId The identifier for an NFT.
    """
    owner: address = self.idToOwner[_tokenId]
    # Throws if `_tokenId` is not a valid NFT
    assert owner != empty(address)
    return owner


@view
@external
def getApproved(_tokenId: uint256) -> address:
    """
    @dev Get the approved address for a single NFT.
         Throws if `_tokenId` is not a valid NFT.
    @param _tokenId ID of the NFT to query the approval of.
    """
    # Throws if `_tokenId` is not a valid NFT
    assert self.idToOwner[_tokenId] != empty(address)
    return self.idToApprovals[_tokenId]


@view
@external
def isApprovedForAll(_owner: address, _operator: address) -> bool:
    """
    @dev Checks if `_operator` is an approved operator for `_owner`.
    @param _owner The address that owns the NFTs.
    @param _operator The address that acts on behalf of the owner.
    """
    return (self.ownerToOperators[_owner])[_operator]


### TRANSFER FUNCTION HELPERS ###

@view
@internal
def _isApprovedOrOwner(_spender: address, _tokenId: uint256) -> bool:
    """
    @dev Returns whether the given spender can transfer a given token ID
    @param spender address of the spender to query
    @param tokenId uint256 ID of the token to be transferred
    @return bool whether the msg.sender is approved for the given token ID,
        is an operator of the owner, or is the owner of the token
    """
    owner: address = self.idToOwner[_tokenId]
    spenderIsOwner: bool = owner == _spender
    spenderIsApproved: bool = _spender == self.idToApprovals[_tokenId]
    spenderIsApprovedForAll: bool = (self.ownerToOperators[owner])[_spender]
    return (spenderIsOwner or spenderIsApproved) or spenderIsApprovedForAll


@internal
def _addTokenTo(_to: address, _tokenId: uint256):
    """
    @dev Add a NFT to a given address
         Throws if `_tokenId` is owned by someone.
    """
    # Throws if `_tokenId` is owned by someone
    assert self.idToOwner[_tokenId] == empty(address)
    # Change the owner
    self.idToOwner[_tokenId] = _to
    # Change count tracking
    self.ownerToNFTokenCount[_to] += 1

@external
def _editTokenURI(_tokenId: uint256, _tokenURI: String[64]):
    self.tokenURIs[_tokenId] = _tokenURI

@external
def addTokenURI(_tokenId: uint256, _tokenURI: String[64]):
    self._addTokenURI(_tokenId, _tokenURI)

@view
@external
def getTokenURIByTokenId(_tokenId: uint256) -> String[64]:
    return self.tokenURIs[_tokenId]

@internal
def _addTokenURI(_tokenId: uint256, _tokenURI: String[64]):
    """
    @dev Add a TokenURI for a given tokenId
        Throws if `_tokenId` already has a URI.
    """
    #Throws if `_tokenId` already has a URI
    assert len(self.tokenURIs[_tokenId]) == 0, "Token not 0"
    # Add the token URI
    self.tokenURIs[_tokenId] = _tokenURI
    # Add to uniquie hashes
    uniqueHash: bytes32 = keccak256(_abi_encode(_tokenURI))
    self.uniqueHashesForToken[uniqueHash] = _tokenId


@internal
def _removeTokenFrom(_from: address, _tokenId: uint256):
    """
    @dev Remove a NFT from a given address
         Throws if `_from` is not the current owner.
    """
    # Throws if `_from` is not the current owner
    assert self.idToOwner[_tokenId] == _from
    # Change the owner
    self.idToOwner[_tokenId] = empty(address)
    # Change count tracking
    self.ownerToNFTokenCount[_from] -= 1


@internal
def _clearApproval(_owner: address, _tokenId: uint256):
    """
    @dev Clear an approval of a given address
         Throws if `_owner` is not the current owner.
    """
    # Throws if `_owner` is not the current owner
    assert self.idToOwner[_tokenId] == _owner
    if self.idToApprovals[_tokenId] != empty(address):
        # Reset approvals
        self.idToApprovals[_tokenId] = empty(address)


@internal
def _transferFrom(_from: address, _to: address, _tokenId: uint256, _sender: address):
    """
    @dev Exeute transfer of a NFT.
         Throws unless `msg.sender` is the current owner, an authorized operator, or the approved
         address for this NFT. (NOTE: `msg.sender` not allowed in private function so pass `_sender`.)
         Throws if `_to` is the zero address.
         Throws if `_from` is not the current owner.
         Throws if `_tokenId` is not a valid NFT.
    """
    # Check requirements
    assert self._isApprovedOrOwner(_sender, _tokenId)
    # Throws if `_to` is the zero address
    assert _to != empty(address)
    # Clear approval. Throws if `_from` is not the current owner
    self._clearApproval(_from, _tokenId)
    # Remove NFT. Throws if `_tokenId` is not a valid NFT
    self._removeTokenFrom(_from, _tokenId)
    # Add NFT
    self._addTokenTo(_to, _tokenId)
    # Log the transfer
    log Transfer(_from, _to, _tokenId)


### TRANSFER FUNCTIONS ###

@external
@payable
def transferFrom(_from: address, _to: address, _tokenId: uint256):
    """
    @dev Throws unless `msg.sender` is the current owner, an authorized operator, or the approved
         address for this NFT.
         Throws if `_from` is not the current owner.
         Throws if `_to` is the zero address.
         Throws if `_tokenId` is not a valid NFT.
    @notice The caller is responsible to confirm that `_to` is capable of receiving NFTs or else
            they maybe be permanently lost.
    @param _from The current owner of the NFT.
    @param _to The new owner.
    @param _tokenId The NFT to transfer.
    """
    self._transferFrom(_from, _to, _tokenId, msg.sender)


@external
@payable
def safeTransferFrom(
        _from: address,
        _to: address,
        _tokenId: uint256,
        _data: Bytes[1024]=b""
    ):
    """
    @dev Transfers the ownership of an NFT from one address to another address.
         Throws unless `msg.sender` is the current owner, an authorized operator, or the
         approved address for this NFT.
         Throws if `_from` is not the current owner.
         Throws if `_to` is the zero address.
         Throws if `_tokenId` is not a valid NFT.
         If `_to` is a smart contract, it calls `onERC721Received` on `_to` and throws if
         the return value is not `bytes4(keccak256("onERC721Received(address,address,uint256,bytes)"))`.
    @param _from The current owner of the NFT.
    @param _to The new owner.
    @param _tokenId The NFT to transfer.
    @param _data Additional data with no specified format, sent in call to `_to`.
    """
    self._transferFrom(_from, _to, _tokenId, msg.sender)
    if _to.is_contract: # check if `_to` is a contract address
        returnValue: bytes4 = ERC721Receiver(_to).onERC721Received(msg.sender, _from, _tokenId, _data)
        # Throws if transfer destination is a contract which does not implement 'onERC721Received'
        assert returnValue == method_id("onERC721Received(address,address,uint256,bytes)", output_type=bytes4)


@external
@payable
def approve(_approved: address, _tokenId: uint256):
    """
    @dev Set or reaffirm the approved address for an NFT. The zero address indicates there is no approved address.
         Throws unless `msg.sender` is the current NFT owner, or an authorized operator of the current owner.
         Throws if `_tokenId` is not a valid NFT. (NOTE: This is not written the EIP)
         Throws if `_approved` is the current owner. (NOTE: This is not written the EIP)
    @param _approved Address to be approved for the given NFT ID.
    @param _tokenId ID of the token to be approved.
    """
    owner: address = self.idToOwner[_tokenId]
    # Throws if `_tokenId` is not a valid NFT
    assert owner != empty(address)
    # Throws if `_approved` is the current owner
    assert _approved != owner
    # Check requirements
    senderIsOwner: bool = self.idToOwner[_tokenId] == msg.sender
    senderIsApprovedForAll: bool = (self.ownerToOperators[owner])[msg.sender]
    assert (senderIsOwner or senderIsApprovedForAll)
    # Set the approval
    self.idToApprovals[_tokenId] = _approved
    log Approval(owner, _approved, _tokenId)


@external
def setApprovalForAll(_operator: address, _approved: bool):
    """
    @dev Enables or disables approval for a third party ("operator") to manage all of
         `msg.sender`'s assets. It also emits the ApprovalForAll event.
         Throws if `_operator` is the `msg.sender`. (NOTE: This is not written the EIP)
    @notice This works even if sender doesn't own any tokens at the time.
    @param _operator Address to add to the set of authorized operators.
    @param _approved True if the operators is approved, false to revoke approval.
    """
    # Throws if `_operator` is the `msg.sender`
    assert _operator != msg.sender
    self.ownerToOperators[msg.sender][_operator] = _approved
    log ApprovalForAll(msg.sender, _operator, _approved)


### MINT & BURN FUNCTIONS ###

@external
def mint(_to: address, _tokenURI: String[64]) -> bool:
    """
    @dev Function to mint tokens
         Throws if `msg.sender` is not the minter.
         Throws if `_to` is zero address.
         Throws if `_tokenId` is owned by someone.
    @param _to The address that will receive the minted tokens.
    @param _tokenURI The token uri of next token to mint.
    @return A boolean that indicates if the operation was successful.
    """
    # Throws if `msg.sender` is not the minter
    assert msg.sender == self.minter
    # Throws if `_to` is zero address
    assert _to != empty(address)
    # Add NFT. Throws if `_tokenId` is owned by someone
    # assert token does not exist uniqueHashesForToken
    uniqueHash: bytes32 = keccak256(_abi_encode(_tokenURI))
    assert self.uniqueHashesForToken[uniqueHash] == 0, "token is non-unique"

    self._addTokenTo(_to, self.tokenCount)
    # Writes the tokenURI for the tokenId
    self._addTokenURI(self.tokenCount, _tokenURI)
    log Transfer(empty(address), _to, self.tokenCount)
    # Increase token count
    self.tokenCount += 1
    return True


@external
def burn(_tokenId: uint256):
    """
    @dev Burns a specific ERC721 token.
         Throws unless `msg.sender` is the current owner, an authorized operator, or the approved
         address for this NFT.
         Throws if `_tokenId` is not a valid NFT.
    @param _tokenId uint256 id of the ERC721 token to be burned.
    """
    # Check requirements
    assert self._isApprovedOrOwner(msg.sender, _tokenId)
    owner: address = self.idToOwner[_tokenId]
    # Throws if `_tokenId` is not a valid NFT
    assert owner != empty(address)
    self._clearApproval(owner, _tokenId)
    self._removeTokenFrom(owner, _tokenId)
    log Transfer(owner, empty(address), _tokenId)



@external
def transferMinter(_new_address: address):
    assert msg.sender == self.minter
    self.minter = _new_address


@external
def setBaseURI(_uri: String[32]):
    # Throws if `msg.sender` is not the minter
    assert msg.sender == self.minter
    self.baseURI = _uri


@view
@external
def tokenURI(_tokenId: uint256) -> String[160]:
    return concat(self.baseURI, self.tokenURIs[_tokenId])

@external
@view
def contractURI() -> String[128]:
    """
    @notice URI for contract level metadata
    @return Contract URI
    """
    return self.contract_uri

@external
def set_contract_uri(new_uri: String[66]):
    """
    @notice Admin function to set a new contract URI
    @param new_uri New URI for the contract
    """

   # assert msg.sender in [self.owner, self.minter]  # dev: Only Admin
    assert self.minter == msg.sender
    self.contract_uri = new_uri


@external
def admin_withdraw_erc20(coin: address, target: address, amount: uint256):
    """
    @notice Withdraw ERC20 tokens accidentally sent to contract
    @param coin ERC20 address
    @param target Address to receive
    @param amount Wei
    """
    assert self.minter == msg.sender  # dev: "Admin Only"
    ERC20(coin).transfer(target, amount)



@external
@view
def totalSupply() -> uint256:
    """
    @notice Enumerate valid NFTs
    @dev Throws if `_index` >= `totalSupply()`.
    @return The token identifier for the `_index`th NFT
    """
    return self.tokenCount


@external
@view
def tokenByIndex(_index: uint256) -> uint256:
    """
    @notice Enumerate valid NFTs
    @dev With no burn and direct minting, this is simple
    @param _index A counter less than `totalSupply()`
    @return The token identifier for the `_index`th NFT,
    """
    return _index


@external
@view
def tokenOfOwnerByIndex(owner: address, index: uint256) -> uint256:
    """
    @notice Enumerate NFTs assigned to an owner
    @dev Throws if `index` >= `balanceOf(owner)` or if `owner` is the zero address, representing invalid NFTs.
    @param owner An address where we are interested in NFTs owned by them
    @param index A counter less than `balanceOf(owner)`
    @return The token identifier for the `index`th NFT assigned to `owner`, (sort order not specified)
    """
    assert owner != empty(address)
    return self.ownerToNFTokenCount[owner]
