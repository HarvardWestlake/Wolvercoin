import React from "react";
import { Web3Context } from "../Contexts/Web3Provider";
import AuctionItem from "./AuctionItem";
import "./auction.css";

const Auction = () => {
	const web3Context = React.useContext(Web3Context);
    const provider = web3Context.provider;
    const signer = provider.getSigner();
    const connectedDutchAuction = web3Context.dutchAuctionContract.connect(signer);
    const connectedNft = web3Context.nftContract.connect(signer);
    const connectedWolvercoin = web3Context.wolvercoinContract.connect(signer);
	const [auctionItems, setAuctionItems] = React.useState({});

    async function fetchData() {
        let activeItems = await connectedDutchAuction.getActiveAuctionItems();
        await Promise.all(activeItems.map(async itemNumber => {
			const seller = await connectedDutchAuction.getSeller(itemNumber);
			const startDate = await connectedDutchAuction.getStartDate(itemNumber);
			const endDate = await connectedDutchAuction.getEndDate(itemNumber);
			const startPrice = await connectedDutchAuction.getStartPrice(itemNumber);
			const endPrice = await connectedDutchAuction.getEndPrice(itemNumber);
			const name = await connectedDutchAuction.getName(itemNumber);

			const newAuctionItems = {...auctionItems};
            newAuctionItems[itemNumber] = {
                seller,
				startDate: new Date(startDate.toNumber() * 1000),
				endDate: new Date(endDate.toNumber() * 1000),
				startPrice: startPrice.toNumber(),
				endPrice: endPrice.toNumber(),
				name,
                nftUrl: await connectedNft.tokenURI(itemNumber)
            };
            setAuctionItems(newAuctionItems);
        }));
    }

    React.useEffect(() => {
        fetchData();
    }, [connectedDutchAuction]);
    
    return (
        <div className="auction">
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