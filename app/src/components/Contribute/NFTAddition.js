import React from "react";
import "./contribute.css";

class NFTAddition extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        metaDataUrl : "",
        password: ""
      };
  }

  handleChange(event) {
    this.setState({[event.target.name]: event.target.value});
  }

  mintNFT() {
    console.log('mint nft');
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
