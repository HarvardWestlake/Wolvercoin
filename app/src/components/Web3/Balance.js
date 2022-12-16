import React from "react";
import { ethers } from "ethers";

class Balance extends React.Component {
  constructor(props) {
    super(props);
    this.init();
    this.state = {
      balance : "...",
      tokenName : "Total"
     };
  }

  componentDidUpdate(prevProps) {
    if (prevProps.web3Context !== this.props.web3Context) {
      this.init();
    }
  }

  async init() {
    if (this.props.web3Context.wolvercoinContract) {
    let wolvercoinContract = this.props.web3Context.wolvercoinContract;
      const tokenName = await wolvercoinContract.name();
      const tokenBalance = await wolvercoinContract.balanceOf(this.props.web3Context.connectedAccount);
      const tokenUnits = await wolvercoinContract.decimals();
      let balance = ethers.utils.formatUnits(tokenBalance, tokenUnits);
      
      this.setState({balance});
      this.setState({tokenName});
    }
  }

  render() {
    return (          
    <div className="header-row">
      <div className="header-item">
        <p className="title">{this.state.tokenName} Balance</p>
        <p className="figure">{this.state.balance}</p>
      </div>
      <div className="header-item">
        <p className="title">Total Deposits</p>
        <p className="figure">0</p>
      </div>
    </div>
    )
  }
};

export default Balance;