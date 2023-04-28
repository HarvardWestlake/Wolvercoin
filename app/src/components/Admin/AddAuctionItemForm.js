import React from "react";
import LoadingImage from "../../resources/loading.gif";
import { Web3Context } from "../Contexts/Web3Provider";
import { ACTIVE_CONTRACTS } from "../Contexts/config";

export default function AddAuctionItemForm() {
    const [startPrice, setStartPrice] = React.useState(100);
    const [endPrice, setEndPrice] = React.useState(10);
    const [startDate, setStartDate] = React.useState("");
    const [endDate, setEndDate] = React.useState("");
    const [nftTokenId, setNftTokenId] = React.useState("");
    const [name, setName] = React.useState("");
    const [nftTokenURI, setNftTokenURI] = React.useState("");
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
        const tokenUri = await connectedNft.tokenURI(val);
        const fullUri = ACTIVE_CONTRACTS.nft.uriBase + tokenUri;

        // The full URI is a JSON object with a bunch of metadata.  We need to grab the image out of it to view it.
        const response = await fetch(fullUri);
        const json = await response.json();
        setNftTokenURI( json.image);
    }

    const submit = async () => {
        const start = new Date(startDate);
        const end = new Date(endDate);
        let yesterday = new Date();
        yesterday.setDate(yesterday.getDate() - 1);
        if(start < yesterday) return; // We should allow it to already be started...
        if(end < start) return;
        if(Number(startPrice) < 0) return;
        if(Number(endPrice) > Number(startPrice) || Number(endPrice) < 0) return;
        if(!nftTokenId) return;
        if(!name) return;

        await connectedDutchAuction.createAuctionItem(startPrice, endPrice, start.getTime() / 1000, end.getTime() / 1000, nftTokenId, name);
    }

    return (
        <div id="add-auction-item-form">
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
