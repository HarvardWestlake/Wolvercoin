import React from "react";
import { ACTIVE_CONTRACTS } from "../Contexts/config";
import "./contribute.css";

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

  overrideUrl = (event) => {
    this.setState({metaDataUrl : event.target.value});
  }

  async mintNFT() {
    let provider = this.props.web3Context?.provider;
    const signer = provider?.getSigner();
    const connectedNft = this.props.web3Context?.nftContract.connect(signer);
    let mintTxn = await connectedNft.mint(ACTIVE_CONTRACTS.nft.address, this.state.metaDataUrl);
    //let mintTxn = await connectedNft.safeMintToThisContractWithApprovalToExternalContractUsingPassword(ACTIVE_CONTRACTS.nft.address, this.state.metaDataUrl, "54321");
    //let result = await this.props.web3Context.nftContract.mint(this.props.web3Context.connectedAccount, "NFT URI", signer);
    console.log('mint nft', mintTxn);
  }

  render() {
    let url = <div></div>
    if (this.state.metaDataUrl) {
      url = (<div><a target="_blank" href={this.state.metaDataUrl}>MetaData on IPFS</a><p>{this.state.metaDataUrl}</p></div>)
    }
    return (
      <div className="readableContent">
        <div>{url}</div>
        {
          window.location.search.includes("debug") && (
            <>
              <input placeholder="URL of NFT image" value={this.state.metaDataUrl} onChange={this.overrideUrl} /><br />
            </>
          )
        }
        <button onClick={this.mintNFT}>Mint NFT</button>
      </div>
    );
  }
}

export default NFTAddition;
