import React from "react";
import LoadingImage from "../../resources/loading.gif";
import { Web3Context } from "../Contexts/Web3Provider";

export default function AddPublicGoodForm() {
    const [goal, setGoal] = React.useState(69);
    const [name, setName] = React.useState("");
    const [nftTokenId, setNftTokenId] = React.useState(null);
    const [nftTokenURI, setNftTokenURI] = React.useState(null);
    const [resultText, setResultText] = React.useState("");

    const web3Context = React.useContext(Web3Context);
    const provider = web3Context?.provider;
    const signer = provider?.getSigner();
    const connectedNft = web3Context?.nftContract.connect(signer);
    const connectedPublicGoods = web3Context?.publicGoodsContract.connect(signer);

    const changeNftId = async (e) => {
        const val = e.target.value;
        setNftTokenId(val);
        if(val.length === 0) return;
        setNftTokenURI(await connectedNft.tokenURI(val));
    }

    const submit = async () => {
        if(!nftTokenId) return;
        if(goal <= 0) return;
        if(!name) return;
        await connectedPublicGoods.createGood(goal, nftTokenId, name);
    }

    return (
        <div>
            <h2>Create a Public Good</h2>
            Name: <input placeholder="Name" value={name} onChange={e => setName(e.target.value)} /><br />
            Donation goal: <input placeholder="Goal" type="number" value={goal} onChange={e => setGoal(e.target.value)} /><br />
            NFT Token ID: <input placeholder="NFT Token ID" type="number" value={nftTokenId} onChange={changeNftId} /><br />
            <button onClick={submit}>Add to Public Goods listing</button><br />
            <img className="preview-image" src={nftTokenURI || LoadingImage} alt="NFT Token" /><br />
            <p className="result">{resultText}</p>
        </div>
    );
}