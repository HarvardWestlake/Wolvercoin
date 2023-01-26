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

// Contracts deployed by @ericyoondotcom with account 0xdCafA75DCAED81cba4155706E9d666112950E854 on 2023-01-25 via MyEtherWallet.
// TODO: Add a script to automatically deploy all contracts
export const ACTIVE_CONTRACTS = {
    wolvercoin : {
        BrownieOutput : Wolvercoin,
        address : "0xAfa87B1A40AdC058aAf8D86Ce81A50ed24975E94"
    },
    nft : {
        BrownieOutput : Nft,
        address : "0xaecCbC38Cb9137675e5b4Bd57FFdC0D939ac9735",
        password : "69420"
    },
    activeUser: {
        BrownieOutput : ActiveUser,
        address : "0x9E64ffca8a35446E9b0C015844C8B8235ed51613"
    },
    simpleAuction : {
        BrownieOutput : SimpleAuction,
        address : "0x528eE628E6d0c8BC17021b13b0F17AA1a7bD141D",
    }, 
    dutchAuction : {
        BrownieOutput : DutchAuction,
        address : "0xd1827780098337da3fb8Fe1793405510EFb1cB35"
    },
    publicGoods : {
        BrownieOutput : PublicGoods,
        address : "0x73259A179d49BA2661e172AF827CBb2751f45555"
    },

    chainId: 5,
    network : NETWORKS.goerli
};