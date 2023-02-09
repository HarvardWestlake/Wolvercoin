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
        address : "0xc6d2f089398bc8BD1Da38d132f6D113D25aE3fcb"
    },
    nft : {
        BrownieOutput : Nft,
        address : "0xA715948275C979150DcF3Ae796244f64c1680e02",
        password : "69420"
    },
    activeUser: {
        BrownieOutput : ActiveUser,
        address : "0x685E58939b431687CC0d8990f0996F18Cd6342bE"
    },
    simpleAuction : {
        BrownieOutput : SimpleAuction,
        address : "0xDEAD000000000000000000000000000000000000",
    }, 
    dutchAuction : {
        BrownieOutput : DutchAuction,
        address : "0xEc7C9a36bbBA83DA66Ae83995E2D9bC90ECC9990"
    },
    publicGoods : {
        BrownieOutput : PublicGoods,
        address : "0x0aD36f3AD05e29e635cc850c342f6319f5A15aa6"
    },

    chainId: 5,
    network : NETWORKS.goerli
};