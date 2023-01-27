import React from "react";
import moment from "moment";
import { ACTIVE_CONTRACTS } from "../Contexts/config";

export default function AuctionItem({itemNumber, item, connectedDutchAuction, connectedWolvercoin, refresh}) {
    const [price, setPrice] = React.useState(0);
    const [loading, setLoading] = React.useState(false);

    const buyItem = async () => {
        if(loading) return;
        setLoading(true);

        await connectedWolvercoin.approve(ACTIVE_CONTRACTS.dutchAuction.address, item.startPrice);
        await connectedDutchAuction.buy(itemNumber);
        await refresh();
        setLoading(false);
    }

    React.useEffect(() => {
        setInterval(() => {
            let newPrice;
            if((new Date()) > item.endDate) {
                newPrice = item.endPrice;
            } else {
                const timeSinceStart = Date.now() - item.startDate.getTime();
                const totalDuration = item.endDate.getTime() - item.startDate.getTime();
                const priceRange = item.startPrice - item.endPrice;
                const progress = timeSinceStart / totalDuration;
                newPrice = item.startPrice - (priceRange * progress);
            }
            setPrice(newPrice);
        }, 1000);
    }, []);

    return (
        <div className="item" style={{backgroundImage: `url(${item.nftUrl})`}}>
            <h3>{item.name}</h3>
            <p><pre>Token ID #{itemNumber}</pre></p>
            <p>Price range: {item.endPrice} to {item.startPrice}</p>
            <p>
                Auction starts {moment(item.startDate).format("ddd, MMM Do, h:mm A")}<br />
                Auction ends {moment(item.endDate).format("ddd, MMM Do, h:mm A")}
            </p>
            {
                item.startDate.getTime() > Date.now() ? (
                    <p>Auction hasn't started yet!</p>
                ) : (
                    <>
                        <h2>PRICE:</h2>
                        <h1>{price.toFixed(2)} WVC</h1>
                        <button disabled={loading} onClick={buyItem}>{loading ? "HANG TIGHT..." : "BUY NOW!"}</button>
                    </>
                )
            }
        </div>
    );
}
