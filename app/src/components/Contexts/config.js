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
        address : "0xd74cAe406dBcCEDAcF4700f8B9CB79f6b2593815"
    },
    nft : {
        BrownieOutput : Nft,
        address : "0x0e52E9dbB8F1Fd540990C620671DF982958eb0D9",
        password : "54321"
    },
    activeUser: {
        BrownieOutput : ActiveUser,
        address : "0x38901938590dD927192a51aEDD957AFa294d146c"
    },
    simpleAuction : {
        BrownieOutput : SimpleAuction,
        address : "0xDEAD000000000000000000000000000000000000",
    }, 
    dutchAuction : {
        BrownieOutput : DutchAuction,
        address : "0xAF0Ba98bE3ae36c8919835e9eA9504E2344E0561"
    },
    publicGoods : {
        BrownieOutput : PublicGoods,
        address : "0xcDe7aD355e6bb4571FEC5B4AC4BE7A4ea57376db"
    },

    chainId: 5,
    network : NETWORKS.goerli
};
