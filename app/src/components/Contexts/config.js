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
        address : "0x0eD916538F03CD088156a3Bd185422FE54354F71"
    },
    nft : {
        BrownieOutput : Nft,
        address : "0xdAf9441Eb63aa491495D0Ded1d18d95474129d59",
        password : "69420"
    },
    activeUser: {
        BrownieOutput : ActiveUser,
        address : "0x2EfC876e53c9457AafaD0327D03C5B062db71855"
    },
    simpleAuction : {
        BrownieOutput : SimpleAuction,
        address : "0xDEAD000000000000000000000000000000000000",
    }, 
    dutchAuction : {
        BrownieOutput : DutchAuction,
        address : "0xA53518Aa31D1Ab8b9a3C3D11eB6eE6E454BCa130"
    },
    publicGoods : {
        BrownieOutput : PublicGoods,
        address : "0x008Ea48b34eD3c2d8a1a9c05Ac26A0De1043edf4"
    },

    chainId: 5,
    network : NETWORKS.goerli
};