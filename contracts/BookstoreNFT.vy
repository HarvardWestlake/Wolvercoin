# @version ^0.3.7
#Dependent: None 
#Dependent on me: Idalis Mczeal 
num: uint256 
struct Erc20Token:
    addr: address
    decimals: uint256
    symbol: String[16]
    hashImag: String[100]

hashie: public (HashMap[uint256, Erc20Token])

@external
def __init__():
    return 

# hashmap that contains the product sha and the image url 
# method to add to hashmap ()
@external
def createBoundNFT(productOwner: address, uRL: String[100]):
    self.hashie[self.num] = Erc20Token({
        addr: productOwner,
        decimals: 18,
        symbol: "WVC",
        hashImag: uRL
        })
    self.num += 1

@external
def redeemProduct(NFTid : uint256) -> bool:
    if (msg.sender == self.hashie[NFTid].addr):
        return True
    else:
        return False








