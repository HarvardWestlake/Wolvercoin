import React, { lazy } from "react";
import Header from "./Header"
import * as Constants from "./consts"
import Contribute from "../Contribute/Contribute.js";
import NFTs from "../NFTs/NFTs.js";
import Auction from "../Auction/Auction.js";
import PublicGoods from "../PublicGoods/PublicGoods.js";
import Footer from "./Footer"
import Admin from "../Admin/Admin";


class Main extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            location: null
        };
    }

    renderPage = () => {
        let page = <div></div>
        switch (this.state.location) {
            case Constants.NAV_OPTIONS["Admin"]:
                page = <Admin />
                break;
            case Constants.NAV_OPTIONS["Auction"]:
                page = <Auction />
                break;
            case Constants.NAV_OPTIONS["Public Goods"]:
                page = <PublicGoods />
                break;
            case Constants.NAV_OPTIONS["NFTs"]:
                page = <NFTs />
                break;
            case Constants.NAV_OPTIONS["Contribute"]:
                page = <Contribute />
                break;
            default:
                page = <Auction />
                break;
        }
        return page;
    }

    setLocation = (location) => {
        this.setState({ location });
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
