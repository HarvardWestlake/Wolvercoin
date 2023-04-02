import React from "react";
import { ACTIVE_CONTRACTS } from "../Contexts/config";
import { Web3Context } from "../Contexts/Web3Provider";

export default function PublicGoodItem({goodNumber, good, connectedPublicGoods, connectedWolvercoin, refresh}) {
    const [donationAmount, setDonationAmount] = React.useState(0);
    const [loading, setLoading] = React.useState(false);
    const [isAdmin, setIsAdmin] = React.useState(false);

    const web3Context = React.useContext(Web3Context);
    const provider = web3Context?.provider;
    const signer = provider?.getSigner();
    const connectedActiveUsers = web3Context?.activeUserContract.connect(signer);

    React.useEffect(() => {
        (async () => {
            const isAdmin = await connectedActiveUsers.getIsAdmin(web3Context.connectedAccount);
            setIsAdmin(isAdmin);
        })();
    }, [connectedActiveUsers, web3Context.connectedAccount]);

    const donateToGood = async () => {
        if(loading) return;
        setLoading(true);
        await connectedWolvercoin.approve(ACTIVE_CONTRACTS.publicGoods.address, donationAmount);
        await connectedPublicGoods.contribute(goodNumber, donationAmount);
        await refresh();
        setLoading(false);
        setDonationAmount(0);
    }

    const completeGood = async () => {
        if(loading) return;
        // eslint-disable-next-line no-restricted-globals
        if(!confirm(
            good.total >= good.goal ?
                "Complete the public good? Only do this once the good has been given to the class." :
                "Cancel the public good? The listing will no longer show up, and all donators will be refunded."
        )) return;

        setLoading(true);
        await connectedPublicGoods.complete(goodNumber);
        await refresh();
        setLoading(false);
    }

    const changeDonationAmount = (e) => {
        if(e.target.value < 0) setDonationAmount(0);
        else setDonationAmount(e.target.value);
    }

    return (
        <div className="good" style={{backgroundImage: `url(${good.nftUrl})`}}>
            <h3>{good.name}</h3>
            <p>Token ID #{goodNumber}</p>
            <h2>GOAL:</h2>
            <h1>{good.total} out of {good.goal}</h1>
            <input type="number" value={donationAmount} onChange={changeDonationAmount} /><br />
            <button disabled={loading} onClick={donateToGood}>{loading ? "HANG TIGHT..." : "DONATE"}</button><br />
            {
                isAdmin && (
                    <button className={good.total >= good.goal ? "" : "negative"} onClick={completeGood}>{good.total >= good.goal ? "COMPLETE GOOD" : "CANCEL GOOD"}</button>
                )
            }
        </div>
    );
}