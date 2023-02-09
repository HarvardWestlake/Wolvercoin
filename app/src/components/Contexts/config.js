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
        address : "0xF44d986adF710FF306bAFf87E80a14e06D643C7e"
    },
    nft : {
        BrownieOutput : Nft,
        address : "0x021E940c3685ecb0A5d16eBd3b937DFF8C55c079",
        password : "69420"
    },
    activeUser: {
        BrownieOutput : ActiveUser,
        address : "0xdBb27a7A91b9A9317557abC73699f31a72CD67B3"
    },
    simpleAuction : {
        BrownieOutput : SimpleAuction,
        address : "0xDEAD000000000000000000000000000000000000",
    }, 
    dutchAuction : {
        BrownieOutput : DutchAuction,
        address : "0x605Fac131eFD323C6964f0593b6B41A07bd87332"
    },
    publicGoods : {
        BrownieOutput : PublicGoods,
        address : "0xfBc88d4c672F42CD6d1588A268F256C9938CdbC5"
    },

    chainId: 5,
    network : NETWORKS.goerli
};