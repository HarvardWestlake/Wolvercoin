import React from "react";
import { ethers } from "ethers";

class Balance extends React.Component {
  constructor(props) {
    super(props);
    this.init();
    this.state = {
      balance : "..."
     };
  }

  async init() {

    let wolvercoinContract = this.props.web3Context.wolvercoinContract;
      const tokenName = await wolvercoinContract.name();
      console.log('Change this to getBalanceOf view after update');
      const tokenBalance = await wolvercoinContract.balanceOf(this.props.web3Context.connectedAccount);
      const tokenUnits = await wolvercoinContract.decimals();
      let balance = ethers.utils.formatUnits(tokenBalance, tokenUnits);
      
      this.setState({balance});
      
  }

  render() {
    return (          
    <div className="header-row">
      <div className="header-item">
        <p className="title">Total Balance</p>
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