import React from "react";
import { create } from 'ipfs-http-client'
import "./main.css";
import ImageUpload from "../Utils/ImageUpload.js"


const POSSIBLE_NFT_UPLOAD_STATES = {
    SPLASH : "SPLASH",
    READY_TO_UPLAD_TO_IPFS : "READY_TO_UPLOAD_TO_IPFS",
    UPLOADING_TO_IPFS : "UPLOADING_TO_IPFS",
    UPLOADED_TO_IPFS : "UPLOADED_TO_IPFS"
};

const NFT_IMAGE_PREVIEW = {
    height: 400,
    width: 300
}

class NFTAddition extends React.Component {
  state = {
    nftProgress : POSSIBLE_NFT_UPLOAD_STATES.SPLASH,
    imagePreview : null,
    imageBase64 : null,
    ipfsImageUrl : null
  };

  constructor(props) {
    super(props);
    this.updateImage = this.updateImage.bind(this);
    this.onUpdateDetails = this.onUpdateDetails.bind(this);
  }

  componentDidMount() {
    //const contract = drizzle.contracts.Reimbursement;
    const dataKey = null;
    // get and save the key for the variable we are interested in
    //const dataKey = contract.methods["storedData"].cacheCall();
    this.setState({ dataKey });
  }

  uploadToIPFS() {
    const requestOptions = {
        method: 'POST',
        headers: { 
            'Content-Type': 'application/json',
            'Authorization': 'Bearer my-token',
            'My-Custom-Header': this.state.password
        },
        body: JSON.stringify({ title: 'React POST Request Example' })
    };
    fetch('http://ipfs.wolvercoin.com/ipfs', requestOptions)
        .then(response => response.json())
        .then(data => this.setState({ postId: data.id }));
  }

  generateImagePreview() {
    const imagePreivew = this.state.imagePreview ? "" : this.state.imagePreview;
    const height = NFT_IMAGE_PREVIEW.height;
    const width = NFT_IMAGE_PREVIEW.width;
    return (<img src="{imagePreview}" alt="" width="{width}" height="{height}" />)
  }

  async onUpdateDetails(event) {
    var state = this.state;
    state[event.target.name] = event.target.value;
    await this.setState(state);
  }

  updateImage(imageBase64, file) {
    this.setState({imageBase64});
  }

  render() {
    const { count } = this.state;
    const imagePreview = this.generateImagePreview();
    const uploadToIPFSDisabled = (this.state.imageBase64 && this.state.password) ? null : "disabled";
    //const { SimpleStorage } = this.props.drizzleState.contracts;
    //const storedData = SimpleStorage.storedData[this.state.dataKey];
    //return <DisplayValue value={storedData && storedData.value} />;
    return (
      <div className="readableContent">
        <div className="nftAddition">
            <h1>Add an NFT for the class to auction!</h1>
            <h3>This is a two step process</h3>
            <h4>1. Upload the NFT image to IPFS</h4>
            <h4>2. Mint an NFT for auction using <br />the image you uploaded to IPFS</h4>
        </div>
            <div className="imagePreview">
                {imagePreview}
            </div>
            <label htmlFor="password">IPFS Password:</label>
            <input name="password" value={this.state.password} onChange={this.onUpdateDetails}  type="text"></input>
            <br />
            <ImageUpload onUpdate={this.updateImage} image={this.state.imageBase64} />
            <br />
            <button disabled={uploadToIPFSDisabled} onClick={this.uploadToIPFS}>Upload To IPFS</button>
            <br />
            <br />
            <br />

            <h1>Add NFT</h1>
            <div className="ipfsImageUrl">
                {this.state.ipfsImageUrl}
            </div>
            <label htmlFor="NFTCollection">Choose an NFT Collection:</label>
            <select>
                <option val="0">Latest Test</option>
            </select>
            <br />
            <input name="creation" onChange={this.onUpdateDetails} value={this.state.creation} type="date"></input><br />

      </div>
    );
  }
}

export default NFTAddition;
