import React from "react";
import "./nft.css"; 

class NFTs extends React.Component {
    render() {
      return (<div className="nfts">
        <a className="view-nft-collection" target="_blank" height="500" width="500" href="https://testnets.opensea.io/collection/not-so-fungible-wolvies-v2-1">View Collection On Opensea</a>
      </div>)
    }
};

export default NFTs;