import React from "react";
// https://dev.to/edge-and-node/uploading-files-to-ipfs-from-a-web-application-50a
import { create } from 'ipfs-http-client'
import { Buffer } from 'buffer'
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

    /* configure Infura auth settings */
    const projectId = "2IaWJsOC0dbYxtM2VeX8c1XF3tA"
    const projectSecret = "806e26c84978a921972a9789d344f0d9"
    const auth = 'Basic ' + Buffer.from(projectId + ':' + projectSecret).toString('base64')

    /* Create an instance of the client */
    const client = create({
            //host: 'ipfs.infura.io',
            host: 'ipfs.wolvercoin.com',
            port: 80,
            protocol: 'http',
            headers: {
                authorization: auth,
            }
        });

    /* upload the file */
    const added = await client.add(this.state.file)
  }

  handleChange(event) {
    this.setState({[event.target.name]: event.target.value});
  }

  async updateImage(imageBase64, file) {
    await this.setState({
        imageBase64 : imageBase64,
        file: file
    });
  }

  render() {
    const { count } = this.state;
    const uploadToIPFSDisabled = (this.state.imageBase64 && this.state.password) ? null : "disabled";
    //const { SimpleStorage } = this.props.drizzleState.contracts;
    //const storedData = SimpleStorage.storedData[this.state.dataKey];
    //return <DisplayValue value={storedData && storedData.value} />;
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
