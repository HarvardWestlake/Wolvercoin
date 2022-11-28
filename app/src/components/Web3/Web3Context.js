import React, { createContext, useContext, useEffect, useState } from "react"
import Network from "../Web3/Network.js"
import Config from "./config.json"
import Reimbursement from "../../contracts/Reimbursement.json"

const contracts = { options: [Reimbursement]};
const config = {Config};
const web3Context = createContext();
/**
 * Web3Context needs to alter state after logged in
 * 
 * For logged out:
 *  - Needs to show blank advert for WVC
 * 
 * For logged in:
 *  - Needs to show a whole bunch of options  
 * 
 * Needs to also handle state changes:
 *  - Logging out
 *  - Switching networks
 *  - Checking network?
 *  - Account swtich
 *      - WVC Coin Balance Udpate
 *      - NFT Update
 */

 export function Web3ContextProvider({ children }) {
    async function isCorrectNetwork() {

    }
    return (
        <web3Context.Provider value={{ contracts, Network, config }}> 
            {children}
        </web3Context.Provider>
    );
}

export default function useWeb3Context() {
  return useContext(web3Context);
}