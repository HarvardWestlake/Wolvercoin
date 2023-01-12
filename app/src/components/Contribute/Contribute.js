import React from "react";
import MetaDataAddition from "./MetaDataAddition"
import IPFSAddition from "./IPFSAddition"
import NFTAddition from "./NFTAddition"
import {Web3Context} from "../Contexts/Web3Provider"

class Contribute extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        ipfsImgUrl : "", //"QmQiYLRqSwfyQcH9go2yyLbqCKidZCtjr4suh6RiXYaii3", 
        metaDataUrl : "", // "QmT5NL1PNvyDAc9muxKVNphBPtTns59UxGo6m8ppeZVoH4",
        password : "IPFS Password"
      }
      this.uploadedIPFSFile = this.uploadedIPFSFile.bind(this);
      this.uploadedMetaDataFile = this.uploadedMetaDataFile.bind(this);
      this.updatePassword = this.updatePassword.bind(this);
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
    updateNFT(nft) {
      this.setState({nft});
    }
    render() {
      return (
      <div className="contribute">
        <IPFSAddition onUpdate={this.uploadedIPFSFile} onUpdatePassword={this.updatePassword}></IPFSAddition>
        <MetaDataAddition password={this.state.password} ipfsImgUrl={this.state.ipfsImgUrl} onUpdateMetaDataUrl={this.uploadedMetaDataFile}></MetaDataAddition>

        <Web3Context.Consumer>
            {providerValueContext => { 
              return <NFTAddition  onUpdateNFT={this.updateNFT} web3Context={providerValueContext} metaDataUrl={this.state.metaDataUrl}></NFTAddition>
            }}
          </Web3Context.Consumer>
      </div>)
    }
};

export default Contribute;