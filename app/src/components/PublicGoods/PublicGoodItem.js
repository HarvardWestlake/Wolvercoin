import React from "react";
import { ACTIVE_CONTRACTS } from "../Contexts/config";

export default function PublicGoodItem({goodNumber, good, connectedPublicGoods, connectedWolvercoin, refresh}) {
    const [donationAmount, setDonationAmount] = React.useState(0);
    const [loading, setLoading] = React.useState(false);

    const donateToGood = async () => {
        if(loading) return;
        setLoading(true);
        await connectedWolvercoin.approve(ACTIVE_CONTRACTS.publicGoods.address, donationAmount);
        await connectedPublicGoods.contribute(goodNumber, donationAmount);
        await refresh();
        setLoading(false);
        setDonationAmount(0);
    }

    const changeDonationAmount = (e) => {
        if(e.target.value < 0) setDonationAmount(0);
        else setDonationAmount(e.target.value);
    }

    return (
        <div className="good" style={{backgroundImage: `url(${good.nftUrl})`}}>
            <h3>{good.name}</h3>
            <p><pre>Token ID #{goodNumber}</pre></p>
            <h2>GOAL:</h2>
            <h1>{good.total} out of {good.goal}</h1>
            <input type="number" value={donationAmount} onChange={changeDonationAmount} /><br />
            <button disabled={loading} onClick={donateToGood}>{loading ? "HANG TIGHT..." : "DONATE"}</button>
        </div>
    );
}