import React from "react";

class Balance extends React.Component {
  constructor(props) {
    super(props);
    this.state = {    };
  }
  
  getBalance() {
    if (!this.props.web3Context.connectedAccount) {
      return 0;
    } else {
      return this.props.web3Context.wolvercoinBalance;
    }
  }
  
  render() {
    const balance = this.getBalance();
    return (          
    <div className="header-row">
      <div className="header-item">
        <p className="title">Total Balance</p>
        <p className="figure">{balance}</p>
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