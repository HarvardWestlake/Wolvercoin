import React from "react";
// https://dev.to/edge-and-node/uploading-files-to-ipfs-from-a-web-application-50a
import { create } from 'ipfs-http-client'
import {sha256} from 'crypto-hash';
import "./contribute.css";
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

class IPFSAddition extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        nftProgress : POSSIBLE_NFT_UPLOAD_STATES.SPLASH,
        password: "",
        imagePreview : null,
        imageBase64 : null,
        ipfsImgUrl : null
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
    let ipfsImgUrl = added.path;
    await this.setState({ipfsImgUrl});
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
    const passwordDisabled = (this.state.ipfsImgUrl) ? null : "disabled";
    const uploadToIPFSDisabled = (this.state.imageBase64 && this.state.password && !this.state.ipfsImgUrl) ? null : "disabled";
    const ipfsUrl = this.state.ipfsImgUrl ? "" : <div>{this.state.ipfsImgUrl}<img src={this.state.ipfsImgUrl} /></div>;
    return (
      <div className="readableContent">
        <div className="nftAddition">
            <h3>Add an NFT for the class to auction!</h3>
            <p>1. Upload the image to IPFS</p>
        </div>
            <label htmlFor="password">IPFS Password:</label>
            <input type="password" name="password" disabled={passwordDisabled} value={this.state.password} onChange={this.handleChange} />
            <ImageUpload onUpdate={this.updateImage} image={this.state.imageBase64} />
            <button disabled={uploadToIPFSDisabled} onClick={this.uploadToIPFS}>Upload To IPFS</button>
      </div>
    );
  }
}

export default IPFSAddition;
