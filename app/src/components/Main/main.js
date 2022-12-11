import React, {lazy } from "react";
import Header from "./Header"
import * as Constants from "./consts"
import Contribute from "../Contribute/Contribute.js";
import NFTs from "../NFTs/NFTs.js";
import Balance from "../Balance/Balance.js";


class Main extends React.Component {
    constructor(props) {
        super(props);
        this.renderPage = this.renderPage.bind(this);
        this.setLocation = this.setLocation.bind(this);
        this.state = {
            location: null
        };
    }

  componentDidMount() {
  }
  
  renderPage() {
    let page = <div></div>
    switch (this.state.location) {
        case Constants.NAV_OPTIONS.BALANCE:
            page = <Balance></Balance>
            break;
        case Constants.NAV_OPTIONS.NFTS:
            page = <NFTs></NFTs>
            break;
        case Constants.NAV_OPTIONS.CONTRIBUTE:
            page = <Contribute></Contribute>
            break;
        default:
            page = <Balance></Balance>
            break;
    }
    return page;
  }

  setLocation(location) {
    this.setState({location});
  }


  render() {
    const pageToRender = this.renderPage();
    return (
    <div>
        <Header onChangeLocation={this.setLocation} location={this.state.location}></Header>
        {pageToRender}
    </div>
    );
  }
};


export default Main;
