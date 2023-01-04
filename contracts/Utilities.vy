# @version 0.3.7

#Dependent: None 
#Dependent on me: None

struct Erc20Token:
    addr: address
    decimals: uint256
    symbol: String[16]
    hashImag: String[100]




hashie : public (HashMap[uint256,Erc20Token])

@external
def __init__ ():
    return

@external
def redeemProduct(NFTid : uint256) -> bool:
    if (msg.sender == self.hashie[NFTid].addr):
        return True
    else:
        return False


#when you want to buy an item make a new nft, whoever buys gets that item, in order to buy nft 
#we dont need to alert wolvercoin that this person is buying an nft, 
#nft has address of the person who bought it and hash of the url
#redeemproduct is a boolean and returns true if the person calling this method is the same as the nft id (parameter)'s address owner person
#returns false if the person is not the same