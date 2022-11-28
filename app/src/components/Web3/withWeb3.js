import React, { createContext, useContext, useEffect, useState } from "react"
import Network from "./Network.js"
import Config from "./config.json"
import Reimbursement from "../../contracts/Reimbursement.json"
import Web3Context from "./context";

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

 const withWeb3 = Component => {
  class WithWeb3 extends React.Component {
    constructor(props) {
      super(props);

      this.state = {
          user : {
            admin: false,
            connected : false
        }
      };
    }

    componentWillMount() {
    }

    render() {
      return (
          <Web3Context.Provider value={this.state.user}>
            <Component {...this.props} />
          </Web3Context.Provider>
        );
      }
    }

    //return withFirebase(WithWeb3);
    return WithWeb3;
};
  
export default withWeb3;