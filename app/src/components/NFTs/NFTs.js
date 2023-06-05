import "./nfts.css";
import React from "react";
import { ACTIVE_CONTRACTS } from "../Contexts/config";

class NFTs extends React.Component {
	render() {
		return (
			<div className="nfts">
				<p>
					<a target="_blank" rel="noopener noreferrer" href={`https://testnets.opensea.io/assets/goerli/${ACTIVE_CONTRACTS.nft.address}`}>
						View our collection of NFTs here!
					</a>
				</p>
			</div>
		);
	}
};

export default NFTs;
