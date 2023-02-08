import React from "react";
import LoadingImage from "../../resources/loading.gif";
import { Web3Context } from "../Contexts/Web3Provider";

export default function AddAuctionItemForm() {
    const [startPrice, setStartPrice] = React.useState(100);
    const [endPrice, setEndPrice] = React.useState(10);
    const [startDate, setStartDate] = React.useState("");
    const [endDate, setEndDate] = React.useState("");
    const [nftTokenId, setNftTokenId] = React.useState(null);
    const [name, setName] = React.useState("");
    const [nftTokenURI, setNftTokenURI] = React.useState(null);
    const [resultText, setResultText] = React.useState("");

    const web3Context = React.useContext(Web3Context);
    const provider = web3Context.provider;
    const signer = provider.getSigner();
    const connectedNft = web3Context.nftContract.connect(signer);
    const connectedDutchAuction = web3Context.dutchAuctionContract.connect(signer);

    const changeNftId = async (e) => {
        const val = e.target.value;
        setNftTokenId(val);
        if(val.length === 0) return;
        setNftTokenURI(await connectedNft.tokenURI(val));
    }

    const submit = async () => {
        const start = new Date(startDate);
        const end = new Date(endDate);
        if(start < new Date()) return;
        if(end < start) return;
        if(startPrice < 0) return;
        if(endPrice > startPrice || endPrice < 0) return;
        if(!nftTokenId) return;
        if(!name) return;

        await connectedDutchAuction.createAuctionItem(startPrice, endPrice, start.getTime() / 1000, end.getTime() / 1000, nftTokenId, name);
    }

    return (
        <div>
            <h2>Create an Auction Item</h2>
            Name: <input placeholder="Name" value={name} onChange={e => setName(e.target.value)} /><br />
            Start price: <input placeholder="Start price" type="number" value={startPrice} onChange={e => setStartPrice(e.target.value)} /><br />
            End price: <input placeholder="End price" type="number" value={endPrice} onChange={e => setEndPrice(e.target.value)} /><br />
            Start date: <input placeholder="Start date" type="datetime-local" value={startDate} onChange={e => setStartDate(e.target.value)} /><br />
            End date: <input placeholder="End date" type="datetime-local" value={endDate} onChange={e => setEndDate(e.target.value)} /><br />
            NFT Token ID: <input placeholder="NFT Token ID" type="number" value={nftTokenId} onChange={changeNftId} /><br />
            <button onClick={submit}>Add to Dutch Auction listing</button><br />
            <img className="preview-image" src={nftTokenURI || LoadingImage} alt="NFT Token" /><br />
            <p className="result">{resultText}</p>
        </div>
    );
}