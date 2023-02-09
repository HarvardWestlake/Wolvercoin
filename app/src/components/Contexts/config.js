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
        address : "0x8b50d300bf47173505975Ca4c10013e9b1fB4679"
    },
    nft : {
        BrownieOutput : Nft,
        address : "0x544100Bb8306Db961d9E81feF02cD61cad1e465e",
        password : "69420"
    },
    activeUser: {
        BrownieOutput : ActiveUser,
        address : "0xCcd6A6Ba3D94d934F52234eB4041e425cB1E9F09"
    },
    simpleAuction : {
        BrownieOutput : SimpleAuction,
        address : "0xDEAD000000000000000000000000000000000000",
    }, 
    dutchAuction : {
        BrownieOutput : DutchAuction,
        address : "0x4718fBb36c2E059E091f6161c6f7D5D597C20fFf"
    },
    publicGoods : {
        BrownieOutput : PublicGoods,
        address : "0xC71924dA1623F6F587b26a49200E2d9eccAeC3A9"
    },

    chainId: 5,
    network : NETWORKS.goerli
};