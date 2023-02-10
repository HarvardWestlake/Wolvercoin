from brownie import network, accounts, ActiveUser, DutchAuction, NFT, PublicGoods, SimpleAuction, Token

def main():
    account = accounts.load('my_account')

    activeUserContract = ActiveUser.deploy(
        account, # admin
        {'from': account}
    );
    erc20Contract = Token.deploy(
        "Wolvercoin", # name
        "WVC", # symbol
        0, # decimals
        42069420, # supply
        {'from': account}
    );
    erc721Contract = NFT.deploy(
        activeUserContract, #activeUser
        12345, #password
        {'from': account}
    );
    # simpleAuctionContract = SimpleAuction.deploy(
    #     erc20Contract, #wolvercoinAddress
    #     erc721Contract, #nftAddress
    #     activeUserContract, #activeUserAddress
    #     {'from': account}
    # );
    dutchAuctionContract = DutchAuction.deploy(
        erc20Contract, #erc20Address
        erc721Contract, #erc721Address
        activeUserContract, #activeUserAddress
        {'from': account}
    );
    publicGoodsContract = PublicGoods.deploy(
        erc20Contract, #erc20Address
        erc721Contract, #erc721Address
        activeUserContract, #activeUserAddress
        {'from': account}
    );

    # Whitelist contracts in ActiveUser
    # activeUserContract.whitelistContract(simpleAuctionContract, {'from': account})
    activeUserContract.whitelistContract(dutchAuctionContract, {'from': account})
    activeUserContract.whitelistContract(publicGoodsContract, {'from': account})

    # print("SimpleAuction has been whitelisted: " + str(activeUserContract.getContractWhitelisted(simpleAuctionContract, {'from': account})))
    print("DutchAuction has been whitelisted: " + str(activeUserContract.getContractWhitelisted(dutchAuctionContract, {'from': account})))
    print("PublicGoods has been whitelisted: " + str(activeUserContract.getContractWhitelisted(publicGoodsContract, {'from': account})))

    print("\n\n~~~~ CONTRACTS CREATED ~~~~")
    print("ERC20 address: " + erc20Contract.address)
    print("ERC721 address: " + erc721Contract.address)
    print("ActiveUser address: " + activeUserContract.address)
    # print("SimpleAuction address: " + simpleAuctionContract.address)
    print("DutchAuction address: " + dutchAuctionContract.address)
    print("PublicGoods address: " + publicGoodsContract.address)
    print("\nNow, copy and paste these addresses into app/src/components/Contexts/config.js.")
