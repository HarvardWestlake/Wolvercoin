import React from "react";
// https://dev.to/edge-and-node/uploading-files-to-ipfs-from-a-web-application-50a
import { create } from 'ipfs-http-client'
import {sha256} from 'crypto-hash';
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
  constructor(props) {
    super(props);
    this.state = {
        nftProgress : POSSIBLE_NFT_UPLOAD_STATES.SPLASH,
        password: "",
        imagePreview : null,
        imageBase64 : null,
        ipfsImageUrl : null
      };
    this.updateImage = this.updateImage.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.uploadToIPFS = this.uploadToIPFS.bind(this);
  }

  componentDidMount() {
    //const contract = drizzle.contracts.Reimbursement;
    const dataKey = null;
    // get and save the key for the variable we are interested in
    //const dataKey = contract.methods["storedData"].cacheCall();
    this.setState({ dataKey });
  }

  async uploadToIPFS() {
    const auth = await(sha256(this.state.password));

    /* Create an instance of the client */
    const client = create({
            host: 'ipfs.wolvercoin.com',
            port: 80,
            protocol: 'http',
            headers: {
                Authorization: auth,
            }
        });

    /* upload the file */
    const added = await client.add(this.state.imageBase64)
    //const added = {path: 'QmbTBUqX9VfJ1apHevCTz2Uh43xAwDjDSV9LnoVvHdrWUv', cid: [], size: NaN};
    console.log(added);
    let ipfsImageUrl = added.path;
    await this.setState({ipfsImageUrl});
  }

  handleChange(event) {
    this.setState({[event.target.name]: event.target.value});
  }

    updateImage(imageBase64, file) {
    this.setState({
        imageBase64 : imageBase64,
        file: file
    });
  }

  render() {
    const { count } = this.state;
    const uploadToIPFSDisabled = (this.state.imageBase64 && this.state.password) ? null : "disabled";
    const ipfsUrl = this.state.ipfsImageUrl ? "" : <div>{this.state.ipfsImageUrl}<img src={this.state.ipfsImageUrl} /></div>;
    return (
      <div className="readableContent">
        <div className="nftAddition">
            <h1>Add an NFT for the class to auction!</h1>
            <h3>This is a two step process</h3>
            <h4>1. Upload the image to IPFS</h4>
            <h4>2. Mint an NFT for auction using <br />the image uploaded to IPFS</h4>
        </div>
            <label htmlFor="password">IPFS Password:</label>

            <input type="password" name="password" value={this.state.password} onChange={this.handleChange} />
            <br />
            <ImageUpload onUpdate={this.updateImage} image={this.state.imageBase64} />
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
