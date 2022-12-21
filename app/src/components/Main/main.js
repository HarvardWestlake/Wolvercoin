import React from "react";
import Header from "./Header"
import * as Constants from "./consts"
import Contribute from "../Contribute/Contribute.js";
import NFTs from "../NFTs/NFTs.js";
import Auction from "../Auction/Auction.js";
import Footer from "./Footer"


class Main extends React.Component {
    constructor(props) {
        super(props);
        this.renderPage = this.renderPage.bind(this);
        this.setLocation = this.setLocation.bind(this);
        this.state = {
            location: null,
            provider: null
        };
    }

    // Here we update items whether or not the provider 
    componentDidUpdate(prevProps) {
      if (!prevProps.provider != this.props.provider && this.props.provider != null && !prevProps.provider && !this.state.provider) {
        console.log('seeting app context once in Web3Provider.js');
          this.props.web3Context.setAppContext(this.props.provider);
      }
    }

  componentDidMount() {
  }
  
  renderPage() {
    let page = <div></div>
    switch (this.state.location) {
        case Constants.NAV_OPTIONS.AUCTION:
            page = <Auction></Auction>
            break;
        case Constants.NAV_OPTIONS.NFTS:
            page = <NFTs></NFTs>
            break;
        case Constants.NAV_OPTIONS.CONTRIBUTE:
            page = <Contribute></Contribute>
            break;
        default:
            page = <Auction></Auction>
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
        <Footer></Footer>
    </div>
    );
  }
};


export default Main;
