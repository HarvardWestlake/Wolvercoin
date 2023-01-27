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
        address : "0x6ff6F41C9a3444BE991ffA8E73A8A001839c6f80"
    },
    nft : {
        BrownieOutput : Nft,
        address : "0xCADe7Be2ED689Df4441452Ec2100D867AEA5EcC5",
        password : "69420"
    },
    activeUser: {
        BrownieOutput : ActiveUser,
        address : "0xD68c70F271A776aaB3D270Fca544F50E6Aea91F8"
    },
    simpleAuction : {
        BrownieOutput : SimpleAuction,
        address : "0xb64c719424EaDd901841DB09c6B4d929E644b868",
    }, 
    dutchAuction : {
        BrownieOutput : DutchAuction,
        address : "0xBC25F74c66eb523841BA1E148BE2912FaEea0cDD"
    },
    publicGoods : {
        BrownieOutput : PublicGoods,
        address : "0xDEE68e188d3FE3f235C8f436a018CB7D4b7c2e6e"
    },

    chainId: 5,
    network : NETWORKS.goerli
};