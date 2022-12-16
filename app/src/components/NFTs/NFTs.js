import React from "react";
import "./nft.css"; 

class NFTs extends React.Component {
    render() {
      return (<div className="nfts">
        <a className="view-nft-collection" target="_blank" rel="noreferrer" height="500" width="500" href="https://testnets.opensea.io/collection/not-so-fungible-wolverines">View Collection On Opensea</a>
      </div>)
    }
};

export default NFTs;