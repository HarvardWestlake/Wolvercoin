import Web3 from 'web3';

class Network {
    
    // Variables
    DEFAULT_CHAIN_SEARCH = "etherscan.io";

    async formatCurrentAccount(currentAccount, showFront = 5, showEnd = 4) {
        if (currentAccount.length < (showFront + showEnd)) {
            return "Not Connected";
        }
        return currentAccount.substring(0, showFront) + "..." + currentAccount.substring(currentAccount.length - showEnd);
    }
    
    async getChainSearchByChainId(chainId) {
        let chainSearch = this.DEFAULT_CHAIN_SEARCH;
        switch (chainId) {
            case "0x1" :
            chainSearch = "etherscan.io";
            break;
            case "0x3" :
            chainSearch = "ropsten." + chainSearch;
            break;
            case "0x4" :
            chainSearch = "rinkeby." + chainSearch;
            break;
            case "0x5" :
            chainSearch = "goerli." + chainSearch;
            break;
            case "0x2a" :
            chainSearch = "kovan." + chainSearch;
            break;
            case "0x89" :
            chainSearch = "polygonscan.com";
            break;
            case "0x13881" :
            chainSearch = "mumbai.polygonscan.com";
            break;
            default:
            break;
        }
        return chainSearch;
    }

}

export default Network;