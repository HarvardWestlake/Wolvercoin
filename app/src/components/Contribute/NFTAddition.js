import React from "react";
import "./contribute.css";

class NFTAddition extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        metaDataUrl : "QmTp2edhAiUMXtaRqQiUvd3paXTDTspBytncBPehwN41S6",
        password: ""
      };
      this.mintNFT = this.mintNFT.bind(this);
  }

  onComponentUpdate() {

  }

  handleChange(event) {
    this.setState({[event.target.name]: event.target.value});
  }

  async mintNFT() {
    let provider = this.props.web3Context.provider;

    const signer = provider.getSigner();

    const connectedNft = this.props.web3Context.nftContract.connect(signer);
    let mintTxn = await connectedNft.mint(this.props.web3Context.connectedAccount, this.state.metaDataUrl);
  
    //let result = await this.props.web3Context.nftContract.mint(this.props.web3Context.connectedAccount, "NFT URI", signer);
    console.log('mint nft', mintTxn);
  }

  render() {
    return (
      <div className="readableContent">
        <div>{this.state.metaDataUrl}</div>
         <button onClick={this.mintNFT}>Mint NFT</button>
      </div>
    );
  }
}

export default NFTAddition;
