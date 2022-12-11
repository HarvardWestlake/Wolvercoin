#write variable names
#hashmap public instance var right here
#in vyper example there is an example of this
#erc20token is the struct name

hashie : public (HashMap[uint256,Erc20Token])

@external
def __init__ ()

@external
def redeemProduct(NFTid : uint256) -> bool
    nftStr : struct = self.hashie.get_val(NFTid)
    if (msg.sender == nftStr.addr):
        return true
    else:
        return false


#when you want to buy an item make a new nft, whoever buys gets that item, in order to buy nft 
#we dont need to alert wolvercoin that this person is buying an nft, 
#nft has address of the person who bought it and hash of the url
#redeemproduct is a boolean and returns true if the person calling this method is the same as the nft id (parameter)'s address owner person
#returns false if the person is not the same