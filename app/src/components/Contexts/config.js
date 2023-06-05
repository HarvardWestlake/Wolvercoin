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

// Deployed by 0xc718b2fd6f5912511d558b1d6a04a9d2b9be25bb
export const ACTIVE_CONTRACTS = {
    wolvercoin : {
        BrownieOutput : Wolvercoin,
        address : "0xB7577161D22870375d604270aD6fE39f63cCCb1F"
    },
    nft : {
        BrownieOutput : Nft,
        address : "0xBB453Fbee1cdFF8740838E2072eC86B1321f44D4",
        password : "54321",
        uriBase : "https://ipfs.wolvercoin.com/ipfs/"
    },
    activeUser: {
        BrownieOutput : ActiveUser,
        address : "0x2F0941Ddd9505a703529c2f06B20CaF94Cd16C8a"
    },
    simpleAuction : {
        BrownieOutput : SimpleAuction,
        address : "0xDEAD000000000000000000000000000000000000",
    }, 
    dutchAuction : {
        BrownieOutput : DutchAuction,
        address : "0x404439f65Bc959efeA5050ff3ddB105Fd462854a"
    },
    publicGoods : {
        BrownieOutput : PublicGoods,
        address : "0x4F332EDCf2CD82f8A78443987ED0132133C0b197"
    },

    chainId: 5,
    network : NETWORKS.goerli,
};


/*

~~~~ CONTRACTS CREATED ~~~~
ERC20 address: 0xB7577161D22870375d604270aD6fE39f63cCCb1F
ERC721 address: 0xBB453Fbee1cdFF8740838E2072eC86B1321f44D4
ActiveUser address: 0x2F0941Ddd9505a703529c2f06B20CaF94Cd16C8a
DutchAuction address: 0x404439f65Bc959efeA5050ff3ddB105Fd462854a
PublicGoods address: 0x4F332EDCf2CD82f8A78443987ED0132133C0b197
*/
