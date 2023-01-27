import * as Wolvercoin from "../Web3/contracts/Token.json"
import * as Nft from "../Web3/contracts/NFT.json"
import * as ActiveUser from "../Web3/contracts/ActiveUser.json"
import * as SimpleAuction from "../Web3/contracts/SimpleAuction.json"
import * as DutchAuction from "../Web3/contracts/DutchAuction.json"
import * as PublicGoods from "../Web3/contracts/PublicGoods.json"

export const NETWORKS = {
    GOERLI : {
        name : "goerli",
        chainId : 5,
        chainIdHex : "0x5",
        scanAddress : "https://goerli.etherscan.io/",
        nativeCurrency: {
            "name": "Goerli ETH",
            "symbol": "gorETH",
            "decimals": 18
        },
    },
    ARBITRUM : {
        name : "Arbitrum One",
        chainId : 42161
    }
}

// Contracts deployed by @ericyoondotcom with account 0xdCafA75DCAED81cba4155706E9d666112950E854 on 2023-01-26 via deploy script.
export const ACTIVE_CONTRACTS = {
    wolvercoin : {
        BrownieOutput : Wolvercoin,
        address : "0x7047cEaE38984F8c9b1fDAD307CDE442ee59Ab3E"
    },
    nft : {
        BrownieOutput : Nft,
        address : "0x323827C16b9a8239A7cD766746985e0eDa2B8646",
        password : "69420"
    },
    activeUser: {
        BrownieOutput : ActiveUser,
        address : "0x58bE02b5629FF4B1E4968727C1f132d23A884647"
    },
    simpleAuction : {
        BrownieOutput : SimpleAuction,
        address : "0x722A39F16eBAd642c258A8BebE04B6ecfF0D1AD6",
    }, 
    dutchAuction : {
        BrownieOutput : DutchAuction,
        address : "0xfC9394426e0750237A7559e01dE0456eb2aC4c4F"
    },
    publicGoods : {
        BrownieOutput : PublicGoods,
        address : "0x7e253Bdd2a0c18827830eF703c4478F54475fBf3"
    },

    chainId: 5,
    network : NETWORKS.goerli
};