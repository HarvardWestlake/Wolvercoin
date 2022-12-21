import React from "react";
import "./contribute.css";
import { ethers } from "ethers";

import * as Contracts from "../Contexts/config"

class NFTAddition extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        metaDataUrl : "",
        password: ""
      };
      this.mintNFT = this.mintNFT.bind(this);
  }

  componentDidUpdate(prevProps) {
    if (prevProps.metaDataUrl !== this.props.metaDataUrl) {
      this.setState({metaDataUrl : this.props.metaDataUrl});
    }
  }

  handleChange(event) {
    this.setState({[event.target.name]: event.target.value});
  }

  async mintNFT() {
    let provider = this.props.web3Context.provider;

    const signer = provider.getSigner();

    let nftContract = new ethers.Contract(
      Contracts.ACTIVE_CONTRACTS.nft.address, 
      Contracts.ACTIVE_CONTRACTS.nft.ABI.abi,
      signer
    );
    const connectedNft = nftContract.connect(signer);
    let mintTxn = await connectedNft.mintAsUser(this.state.metaDataUrl, 238497239879);
    
    //let result = await this.props.web3Context.nftContract.mint(this.props.web3Context.connectedAccount, "NFT URI", signer);
    console.log('mint nft', mintTxn); 
  }

  render() {
    let url = <div></div>
    if (this.state.metaDataUrl) {
      url = (<div><a target="_blank" rel="noreferrer"  href={"https://ipfs.wolvercoin.com/ipfs/" + this.state.metaDataUrl} >MetaData on IPFS</a><p>{this.state.metaDataUrl}</p></div>)
    }
    const disabledButton = this.state.metaDataUrl ? "" : "disabled";
    return (
      <div className="readableContent">
        <div>{url}</div>
         <button disabled={disabledButton} onClick={this.mintNFT}>Mint NFT</button>
      </div>
    );
  }
}

export default NFTAddition;
