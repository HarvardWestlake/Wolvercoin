

#the amount of time that the auction will be active
duration public(uint256)
#the seller of the auction item
seller public(address)
#the starting price of the auction item
startPrice public(uint256)
#the minimum price that the auction item can reach
endPrice public(uint256)
#the time that the auction item was created & active
startDate public(uint256)
#the final date when the auction will end no matter what
endDate public(uint256)
#the address for the auction item NFT
NFT public(address)

@external
def __init__():
    

@external
def _buy(buyer: address):


@external
def _getPrice() -> (uint256):
