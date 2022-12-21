import React from "react";
import "./web3.css"
import * as Constants from "../Contexts/config"

class SwitchNetwork extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
    this.switchNetwork = this.switchNetwork.bind(this);
  }
  
  async switchNetwork() {
    let network = Constants.ACTIVE_CONTRACTS.chainId;
    switch (network) {
        case 5:
          let chainId = await this.props.web3Context.provider.send("wallet_switchEthereumChain",[{chainId: "0x5"}]);
          window.location.reload();
          break;
        default:
          this.props.web3Context.provider.send("wallet_addEthereumChain",[{
                chainId: "0x5",
                rpcUrls: ["https://goerli.optimism.io/"],
                chainName: "Goerli",
                nativeCurrency: {
                    name: "GoerliEth",
                    symbol: "Eth",
                    decimals: 18
                },
                blockExplorerUrls: ["https://goerli.etherscan.io/"]
            }]);
        break;
    }
  }
  
  render() {
    // If we have not yet gotten the chain ID from the network
    if (Number(this.props.web3Context.chainId) === 0) {
      return (<div></div>)
    }

    const visible = (Number(this.props.web3Context.chainId) === 5) ? "hidden" : "switch-to-goerli";
    return (  
      <div className="switch-network-container">        
    <button className={visible} onClick={this.switchNetwork}>Switch to Correct EVM Network</button>
    </div>
    )
  }
};

export default SwitchNetwork;