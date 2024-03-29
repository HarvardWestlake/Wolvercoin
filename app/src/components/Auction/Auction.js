import React from "react";
import { Web3Context } from "../Contexts/Web3Provider";
import AuctionItem from "./AuctionItem";
import "./auction.css";
import { ACTIVE_CONTRACTS } from "../Contexts/config";
import Approve from "./Approve";
import { ethers } from "ethers";

const Auction = () => {
	const web3Context = React.useContext(Web3Context);
    
	const [auctionItems, setAuctionItems] = React.useState({});
    const [connectedDutchAuction, setConnectedDutchAuction] = React.useState(null);
    const [connectedNft, setConnectedNft] = React.useState(null);
    const [connectedWolvercoin, setConnectedWolvercoin] = React.useState(null);
    const [needsApproval, setNeedsApproval] = React.useState(null);

    React.useEffect(() => {
        const provider = web3Context.provider;
        const signer = provider.getSigner();
        setConnectedDutchAuction(web3Context.dutchAuctionContract.connect(signer));
        setConnectedNft(web3Context.nftContract.connect(signer));
        setConnectedWolvercoin(web3Context.wolvercoinContract.connect(signer));
    }, [web3Context]);


    const fetchData = React.useCallback(async () => {
        if(!connectedDutchAuction) return;
        let activeItems = await connectedDutchAuction.getActiveAuctionItems();
        const newAuctionItems = {};
        const provider = web3Context.provider;
        const signerAddress = await provider.getSigner().getAddress();
        const totalWolvercoin = await connectedWolvercoin.getBalanceOf(signerAddress);
        const approvalAmount = await connectedWolvercoin.getAllowanceOf(connectedDutchAuction.address);
        setNeedsApproval(totalWolvercoin > approvalAmount);
        await Promise.all(activeItems.map(async itemNumber => {
			const seller = await connectedDutchAuction.getSeller(itemNumber);
			const startDate = await connectedDutchAuction.getStartDate(itemNumber);
			const endDate = await connectedDutchAuction.getEndDate(itemNumber);
			const startPrice = await connectedDutchAuction.getStartPrice(itemNumber);
			const endPrice = await connectedDutchAuction.getEndPrice(itemNumber);
			const name = await connectedDutchAuction.getName(itemNumber);
            const nftJsonUri = await connectedNft.tokenURI(itemNumber);
            const fullUri = ACTIVE_CONTRACTS.nft.uriBase + nftJsonUri;
            const response = await fetch(fullUri);
            const json = await response.json();
            const readableStartPrice = ethers.utils.formatUnits(startPrice, 18);
            const readableEndPrice = ethers.utils.formatUnits(endPrice, 18);
            newAuctionItems[itemNumber] = {
                seller,
				startDate: new Date(startDate.toNumber() * 1000),
				endDate: new Date(endDate.toNumber() * 1000),
				startPrice: readableStartPrice,
				endPrice: readableEndPrice,
				name,
                nftUrl: json.image,
                approvalAmount : approvalAmount.toNumber()
            };
        }));
        setAuctionItems(newAuctionItems);
    }, [connectedDutchAuction, connectedNft]);

    React.useEffect(() => {
        fetchData();
    }, [connectedNft, connectedDutchAuction, fetchData]);
    
    return (
        <div className="auction">
            {needsApproval && <Approve 
                connectedWolvercoin={connectedWolvercoin}  
                connectedDutchAuction={connectedDutchAuction} 
                needsApproval={needsApproval}
                />
            }
            <h1>Dutch Auction</h1>
            <ul>
                <li>Buy private goods, e.g. a grade boost or a smoke sesh with Top T!</li>
                <li>The price of each good goes down as time goes on, so if you wait, you'll get a better deal.</li>
                <li>But, if you wait too long, someone else might buy the item before you, so better hurry!</li>
            </ul>
            <div id="items_list">
                {
                    Object.keys(auctionItems).map(itemNumber => {
                        const item = auctionItems[itemNumber];
                        return (
                            <AuctionItem
                                key={itemNumber}
                                itemNumber={itemNumber}
                                item={item}
                                connectedDutchAuction={connectedDutchAuction}
                                connectedWolvercoin={connectedWolvercoin}
                                refresh={fetchData}
                            />
                        )
                    })
                }
            </div>
        </div>
    )
}

export default Auction;
