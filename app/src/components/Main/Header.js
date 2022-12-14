import React from "react";
import MetaMask from "../Web3/MetaMask";
import * as Constants from "./consts"
import Nav from "./Nav"
import {Web3Context} from "../Contexts/Web3Provider"

class Header extends React.Component {
  
  constructor(props) {
    super(props);
  }

  render() {
    // The MetaMask Componenet receives not only the connectedAccount
    // but also a onConnect function from the context
    // Wrapping the Context inside a {value => <>} subscribes the component to any changes 
    return (
      <div>
        <div className="container">
        <div className="content">
        <div className="menu-container">
          <div className="logo-container"><a className="logo-link" href="/#">Wolvercoin</a></div>
          <Nav updateHashLocation={this.props.onChangeLocation} location={this.props.location}></Nav>
          <Web3Context.Consumer>
            {providerValueContext => { 
              return <MetaMask web3Context={providerValueContext}/>
            }}
          </Web3Context.Consumer>
         </div>   
      </div>
        </div>
      </div>
      )
  }
};



export default Header;
