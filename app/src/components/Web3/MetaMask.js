import React from "react";
import { ethers } from "ethers";
import * as Contracts from "../Contexts/config.js"
import "./web3.css"

// Linked to built contracts 
// andrewtheiss@andrews-mbp-3 contracts % ln -s /Users/andrewtheiss/Documents/GitHub/Wolvercoin/build/contracts/ /Users/andrewtheiss/Documents/GitHub/Wolvercoin/app/src/components/Web3/contracts 

// Taken from https://programmablewealth.com/ethersjs-react-tutorial/

class MetaMask extends React.Component {
  constructor(props) {
    super(props);
    this.state = {    };
  }

  getScanAddress(network) {
    network = 1;
    let scanAddress = "https://etherscan.io/address/";
    switch (network) {
      case 1:
        scanAddress = "https://etherscan.io/address/"
        break;
        default:
          break;
    }
    return scanAddress;
  }

  async update() {

    const provider = new ethers.providers.Web3Provider(window.ethereum)
    const accounts = await provider.send("eth_requestAccounts", []);
    const wolvercoinContract = new ethers.Contract(
      Contracts.ACTIVE_CONTRACTS.wolvercoin.address, 
      Contracts.ACTIVE_CONTRACTS.wolvercoin.ABI.abi, 
      provider
    );
    const chosenAccount = this.props.web3Context.connectedAccount;
    const tokenName = await wolvercoinContract.name();
    const tokenBalance = await wolvercoinContract.balanceOf(chosenAccount);
    const tokenUnits = await wolvercoinContract.decimals();
    const tokenBalanceInEther = ethers.utils.formatUnits(tokenBalance, tokenUnits);
    const abreviatedWallet = chosenAccount.substring(0,6) + "..." + chosenAccount.substring(chosenAccount.length-4);
    const scanAddress = this.getScanAddress(1) + chosenAccount;
    this.setState({ selectedAddress: chosenAccount, tokenName, tokenBalanceInEther, abreviatedWallet, scanAddress })
 
  }

  async disconnectFromMetamask() {

  }

  async connectToMetamask() {
    const provider = new ethers.providers.Web3Provider(window.ethereum)
    const accounts = await provider.send("eth_requestAccounts", []);
    await this.props.web3Context.setConnectedAccount(accounts[0]);
    this.props.web3Context.connectedAccount = accounts[0];
    this.setState({accounts : accounts[0]});
  }

  async addToken() {
    const provider = new ethers.providers.Web3Provider(window.ethereum)
    //const accounts = await provider.send("eth_requestAccounts", []);
    // Add token to ethereum wallet in metamask

    const params = {
      type: 'ERC20',
      options: {
        address: Contracts.ACTIVE_CONTRACTS.wolvercoin.address,
        symbol: 'WOLV',
        decimals: 18,
        image: 'https://wolvercoin.com/logo192.png'
      }
    };
   // const assets = await ethers.providers.Web3Provider.request({ method: "wallet_watchAsset",params});
   const asset = window.ethereum.request({ method: 'wallet_watchAsset', params }).then((result) => {
    if (result) {
      console.log('Thanks for your interest!');
    } else {
      console.log('Your loss!');
    }
  }).catch((error) => {
    console.log(error);
  });
    console.log(asset);
  }

  renderMetamask() {
    if (!this.props.web3Context.connectedAccount) {
      return (
        <div className="gas-station-container">
        <span>
          <button className="wallet-connect-button" onClick={() => this.connectToMetamask()}>Connect</button>
        </span>
        </div>
      )
    } else {
      return (
        <div>
        <span>
          <svg className="MuiSvgIcon-root icon" focusable="false" viewBox="0 0 24 24" aria-hidden="true">
          <path d="M19.77 7.23l.01-.01-3.72-3.72L15 4.56l2.11 2.11c-.94.36-1.61 1.26-1.61 2.33 0 1.38 1.12 2.5 2.5 2.5.36 0 .69-.08 1-.21v7.21c0 .55-.45 1-1 1s-1-.45-1-1V14c0-1.1-.9-2-2-2h-1V5c0-1.1-.9-2-2-2H6c-1.1 0-2 .9-2 2v16h10v-7.5h1.5v5c0 1.38 1.12 2.5 2.5 2.5s2.5-1.12 2.5-2.5V9c0-.69-.28-1.32-.73-1.77zM12 10H6V5h6v5zm6 0c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1z"></path>
          </svg>
          <span className="price">62</span>
        </span>
            <span id="addCoinToMetamask" onClick={() => this.addToken()} className="crypto-icon"></span>
            <span>
              <span className="connected-indicator"></span>
              <span className="address">
                <a href={this.state.scanAddress} id="link-to-etherscan" className="link-to-etherscan" target="_blank" rel="noopener noreferrer">{this.state.abreviatedWallet}</a>
              </span>
              <span className="">
                <button className="disconnect-button" tabIndex="-1" type="button">
                  <span className="MuiButton-label"  onClick={() => this.disconnectFromMetamask()} >Disconnect</span>
                </button>
              </span>
            </span>
        </div>
      );
    }
  }
    render() {
      return (
          <div className="wallet-info ">
            {this.renderMetamask()}
          </div>
        )
    }
};

export default MetaMask;
