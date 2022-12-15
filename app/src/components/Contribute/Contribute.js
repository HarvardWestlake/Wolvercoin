import React from "react";
import MetaDataAddition from "./MetaDataAddition"
import IPFSAddition from "./IPFSAddition"
import NFTAddition from "./NFTAddition"
import {Web3Context} from "../Contexts/Web3Provider"

class Contribute extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        ipfsImgUrl : "QmdhvcpkeeUvA85RAiLCgYAq5QSeeWmTmyvF2U6zj88cbX",
        metaDataUrl : "QmTp2edhAiUMXtaRqQiUvd3paXTDTspBytncBPehwN41S6",
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

        <Web3Context.Consumer>
            {providerValueContext => { 
              return <NFTAddition  web3Context={providerValueContext} ipfsMetaDataUrl={this.state.metaDataUrl}></NFTAddition>
            }}
          </Web3Context.Consumer>
      </div>)
    }
};

export default Contribute;