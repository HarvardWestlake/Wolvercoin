import * as Wolvercoin from "../Web3/contracts/contracts/Token.json"
import * as Nft from "../Web3/contracts/contracts/NFT.json"
import * as ActiveUser from "../Web3/contracts/contracts/ActiveUser.json"

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
export const ACTIVE_CONTRACTS = {
    wolvercoin : {
        ABI : Wolvercoin,
        address : "0x9bced5e272c4d81b55ae092f85f6fee39545686f"
    },
    nft : {
        ABI : Nft,
        address : "0xe3D135Cc61E2f9391Fe3D678A14Cf8De6F6c9Abf"
    },
    activeUser : {
        ABI : ActiveUser,
        address : "0xbAe2009e5D4fEb1A3884eFf72aD3c5587Aa2A4bD"
    },
    regularAuction : {
        ABI : "",
        address : "",
    }, 
    dutchAction : {
        ABI : "",
        address : ""
    },
    chainId: 5,
    network : NETWORKS.goerli
};