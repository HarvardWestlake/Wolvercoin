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
        address : "0x6D996fC1b1074A5E7F88a4fB789060335866B52e"
    },
    nft : {
        BrownieOutput : Nft,
        address : "0x7Ef07641Bb8Feb194555Fcb4E10a3C7eaa333b6B",
        password : "69420"
    },
    activeUser: {
        BrownieOutput : ActiveUser,
        address : "0x427567F07c7F32637e383eE57B0C3002bAFbA811"
    },
    simpleAuction : {
        BrownieOutput : SimpleAuction,
        address : "0xDEAD000000000000000000000000000000000000",
    }, 
    dutchAuction : {
        BrownieOutput : DutchAuction,
        address : "0xc8F097071232171A1d937D4Ab51D5EAf404846e3"
    },
    publicGoods : {
        BrownieOutput : PublicGoods,
        address : "0x381d896f0980f9516109C74F83B5D489242C60B7"
    },

    chainId: 5,
    network : NETWORKS.goerli
};