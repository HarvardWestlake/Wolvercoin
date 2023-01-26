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

// Contracts deployed by @ericyoondotcom with account 0xdCafA75DCAED81cba4155706E9d666112950E854 on 2023-01-25 via deploy script.
export const ACTIVE_CONTRACTS = {
    wolvercoin : {
        BrownieOutput : Wolvercoin,
        address : "0xe9B196B3abdfA098030769794Eb20c9e0237567F"
    },
    nft : {
        BrownieOutput : Nft,
        address : "0x1bC83699dABCc8fd745a0E6Df7B093d956D119Ac",
        password : "69420"
    },
    activeUser: {
        BrownieOutput : ActiveUser,
        address : "0xd8E6E0f5ef1c6620264Cae1E079F11E763D06e69"
    },
    simpleAuction : {
        BrownieOutput : SimpleAuction,
        address : "",
    }, 
    dutchAuction : {
        BrownieOutput : DutchAuction,
        address : ""
    },
    publicGoods : {
        BrownieOutput : PublicGoods,
        address : "0x643443a8fa43f20Cf427594478Db2121238F6CE3"
    },

    chainId: 5,
    network : NETWORKS.goerli
};