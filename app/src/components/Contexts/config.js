import * as Wolvercoin from "../Web3/contracts/contracts/ERC20.json"


export const NETWORKS = {
    GOERLI : {
        name : "goerli",
        chainId : 5,
        chainIdHex : "0x5",
        scanAddress : "https://goerli.etherscan.io/",
        rpc : "https://rpc.goerli.udit.blv",
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
export const CONTRACTS = {
    wolvercoin : {
        ABI : Wolvercoin,
        address : "0x9bced5e272c4d81b55ae092f85f6fee39545686f"
    },
    nft : {

    },
    network : NETWORKS.goerli
};