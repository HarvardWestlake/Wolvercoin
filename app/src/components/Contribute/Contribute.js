import React from "react";
import MetaDataAddition from "./MetaDataAddition"
import IPFSAddition from "./IPFSAddition"
import NFTAddition from "./NFTAddition"

class Contribute extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        ipfsImgUrl : "QmdhvcpkeeUvA85RAiLCgYAq5QSeeWmTmyvF2U6zj88cbX",
        metaDataUrl : "",
        password : "IPFS Password"
      }
    }
    uploadedIPFSFile(ipfsImgUrl) {
      this.setState({ipfsImgUrl});
    }
    uploadedMetaDataFile(metaDataUrl) {
      this.setState({metaDataUrl});
    }
    updatePassword(password) {
      this.setState({password});
    }
    render() {
      return (
      <div className="contribute">
        <IPFSAddition onUpdate={this.uploadedIPFSFile} onUpdatePassword={this.updatePassword}></IPFSAddition>
        <MetaDataAddition password={this.state.password} ipfsImgUrl={this.state.ipfsImgUrl}></MetaDataAddition>
        <NFTAddition ipfsMetaDataUrl={this.state.metaDataUrl}></NFTAddition>
      </div>)
    }
};

export default Contribute;