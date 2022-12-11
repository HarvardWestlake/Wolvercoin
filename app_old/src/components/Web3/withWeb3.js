import React, { createContext, useContext, useEffect, useState } from "react";
import Network from "./Network.js";
import Config from "./config.json";
import Web3 from "web3";
import Web3Context from "./context";

import Contracts from "./Contracts";

const contracts = { Contracts };
const config = { Config };
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

const withWeb3 = (Component) => {
  class WithWeb3 extends React.Component {
    constructor(props) {
      super(props);

      this.state = {
        contracts: Contracts,
        user: {
          admin: false,
          connected: false,
        },
        web3: false
      };
    }

    // Check the user is logged on
    async componentDidMount() {
      if (!this.state.web3) {
        let web3 = new Web3(
          Web3.givenProvider ||
            new Web3.providers.HttpProvider("http://localhost:8545")
        );
        console.log(web3);
        let provider = this.getNetworkProvider(web3);
        let accounts = this.getAccounts(web3);
        await this.setState({ web3 });

      }

    }

    async getAccounts(web3) {
      let accounts = await web3.eth.getAccounts();
      console.log(accounts);
      return accounts;
    }

    async getNetworkProvider(web3) {
      // Check if connected
      let providerConnected = web3.providers.connected;
      console.log( providerConnected);
/*

      
      if (provider) {
        const chainId = await provider.request({
            method: 'eth_chainId'
          });
    
          // If the current blockchain is not the desired network, show the button to switch
          const containerElement = document.querySelector('#switch-network');
          const buttonElement = document.querySelector('#switch-network-button');
          let env = NETWORK[ENV];            // dev or prod
          let env_name = NETWORK.NAME[env];  // goerli or matic
          if (chainId != NETWORK.CHAIN_ID[NETWORK[ENV]]) {
            if (containerElement.classList.contains("hidden")) {
              containerElement.classList.remove("hidden");
            }
            buttonElement.innerHTML = "Wrong Network!  Click to connect to " + env_name + "";
          } else {
            if (!containerElement.classList.contains("hidden")) {
              containerElement.classList.add("hidden");
            }
          }
          
      }
      return provider;
      */
    }
    

    render() {
      return (
        <Web3Context.Provider value={this.state}>
          <Component {...this.props} />
        </Web3Context.Provider>
      );
    }
  }

  //return withFirebase(WithWeb3);
  return WithWeb3;
};

export default withWeb3;
