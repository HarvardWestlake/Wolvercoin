import React from "react";

class Header extends React.Component {
  componentDidMount() {
    console.log(this.props);
  }
  render() {
    return (
      <div>
        <div className="container">
        <div className="content">
        <div className="menu-container">
          <div className="logo-container"><a className="logo-link" href="/">Wolvercoin</a></div>
          <div className="menu-items">
            <a id="menu_home" className="menu-item" href="/#">Balances</a>
            <a id="menu_nfts" className="menu-item active" href="/#nfts">NFTs</a>
            <a id="menu_announcements" className="menu-item " href="/#announcements">Announcements</a>
            <a id="menu_docs" className="menu-item " href="/#docs">Docs</a>
          </div>
          <div className="wallet-info">
            <div id="wallet-connected" className="wallet-connected-container">
              <div className="wallet-info ">
                <div className="gas-station-container hidden">
                  <svg className="MuiSvgIcon-root icon" focusable="false" viewBox="0 0 24 24" aria-hidden="true">
                    <path d="M19.77 7.23l.01-.01-3.72-3.72L15 4.56l2.11 2.11c-.94.36-1.61 1.26-1.61 2.33 0 1.38 1.12 2.5 2.5 2.5.36 0 .69-.08 1-.21v7.21c0 .55-.45 1-1 1s-1-.45-1-1V14c0-1.1-.9-2-2-2h-1V5c0-1.1-.9-2-2-2H6c-1.1 0-2 .9-2 2v16h10v-7.5h1.5v5c0 1.38 1.12 2.5 2.5 2.5s2.5-1.12 2.5-2.5V9c0-.69-.28-1.32-.73-1.77zM12 10H6V5h6v5zm6 0c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1z">
                    </path>
                  </svg><span className="price">62</span>
                </div>
                <span id="addCoinToMetamask" className="crypto-icon"></span>
                <span className="connected-indicator"></span>
                <span className="address">
                  <a href="https://etherscan.io/address/0x3afb0b4ca9ab60165e207cb14067b07a04114413" id="link-to-etherscan" className="link-to-etherscan" target="_blank" rel="noopener noreferrer">0x3af...4413</a>
                </span>
                <span className="">
                  <button className="disconnect-button" tabIndex="-1" type="button" disabled="">
                    <span className="MuiButton-label">Disconnect</span>
                  </button>
                </span>
              </div>
            </div>
            <button id="wallet-connect-button" className="wallet-connect-button hidden" tabIndex="0" type="button" aria-controls="wallet-info-dropdown" aria-haspopup="true">
              <span className="MuiButton-label">Connect Wallet</span>
            </button>
          </div>
        </div>
      </div>
        </div>
      </div>)
  }
};



export default Header;
