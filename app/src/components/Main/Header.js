import React from "react";
import MetaMask from "../Web3/MetaMask";
import * as Constants from "./consts"
import Nav from "./Nav"

class Header extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <div className="container">
        <div className="content">
        <div className="menu-container">
          <div className="logo-container"><a className="logo-link" href="/#">Wolvercoin</a></div>
          <Nav updateHashLocation={this.props.onChangeLocation} location={this.props.location}></Nav>
          <MetaMask />
         </div>   
      </div>
        </div>
      </div>
      )
  }
};



export default Header;
