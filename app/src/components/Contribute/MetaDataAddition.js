import React from "react";
// https://dev.to/edge-and-node/uploading-files-to-ipfs-from-a-web-application-50a
import { create } from 'ipfs-http-client'
import {sha256} from 'crypto-hash';
import "./contribute.css";

const NFT_IMAGE_PREVIEW = {
    height: 400,
    width: 300
}

class MetaDataAddition extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        ipfsImgUrl : this.props.ipfsImgUrl,
        password: this.props.password,
        name : "",
        metaDataUrl : ""
      };
      this.handleChange = this.handleChange.bind(this);
      this.uploadMetaDataToIPFS = this.uploadMetaDataToIPFS.bind(this);
      this.generateBasicMetaDataForUpload = this.generateBasicMetaDataForUpload.bind(this);
  }

  componentDidUpdate(prevProps) {
    if (prevProps.ipfsImgUrl !== this.props.ipfsImgUrl) {
      this.setState({ipfsImgUrl : this.props.ipfsImgUrl});
    }
    
  }

  generateBasicMetaDataForUpload() {
    // https://ikzttp.mypinata.cloud/ipfs/QmQFkLSQysj94s5GvTHPyzTxrawwtjgiiYS2TBLgrvw8CW/6190
    let basicMetaData = {
        name : this.state.name,
        image : "http://ipfs.wolvercoin.com/ipfs/" + this.state.ipfsImgUrl,
        attributes : [
            {
                "trait_type": "Year",
                "value": 2023
            }
        ]
    };
    return basicMetaData;
  }

  async uploadMetaDataToIPFS() {
    const auth = await(sha256(this.state.password));
    const client = create({
            host: 'ipfs.wolvercoin.com',
            port: 80,
            protocol: 'http',
            headers: {
                Authorization: auth
            }
        });

    /* upload the metadata */
    console.log('need to check filesize');
    const fileData = JSON.stringify(this.generateBasicMetaDataForUpload());
    const blob = new Blob([fileData], {type: "text/json"});
    const added = await client.add(blob);
    let metaDataUrl = added.path;
    await this.setState({metaDataUrl});
    this.props.onUpdateMetaDataUrl(metaDataUrl);
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
    const uploadToIPFSDisabled = (this.state.metaDataUrl == "" && this.state.ipfsImgUrl != "") ? null : "disabled";
    
    let url = <div></div>
    if (this.state.ipfsImgUrl) {
      url = (<div><a target="_blank" href={"http://ipfs.wolvercoin.com/ipfs/" + this.state.ipfsImgUrl} >MetaData on IPFS</a><p>{this.state.ipfsImgUrl}</p></div>)
    }
    return (
      <div className="readableContent">
            <h4>2. Upload MetaData</h4>
            <div className="ipfsImageUrl">
                {url}
            </div>
            <label htmlFor="name">Name:</label>
            <input name="name" onChange={this.handleChange} value={this.state.name} type="text"></input><br />
            <button disabled={uploadToIPFSDisabled} onClick={this.uploadMetaDataToIPFS}>Upload MetaData</button>
            <div>{this.state.metaDataUrl}</div>
      </div>
    );
  }
}

export default MetaDataAddition;
