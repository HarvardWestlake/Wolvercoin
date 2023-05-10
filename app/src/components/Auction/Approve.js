import React from "react";
import { Web3Context } from "../Contexts/Web3Provider";
import { ethers } from "ethers";
import "./auction.css";

const Approve = ({connectedWolvercoin, connectedDutchAuction, needsApproval}) => {
	const web3Context = React.useContext(Web3Context);

    const [approval, setApproval] = React.useState("none");
    const [approvalAmount, setApprovalAmount] = React.useState(0);
    const [wolvercoinBalance, setWolvercoinBalance] = React.useState(0);

    
    const updateApproval = async () => {
        const provider = web3Context.provider;
        const signer = provider.getSigner();
        const signerAddress = await signer.getAddress();
        const totalWolvercoin = await connectedWolvercoin.getBalanceOf(signerAddress);
        setWolvercoinBalance(totalWolvercoin);
        const approvalAmount = await connectedWolvercoin.getApprovedAmountOf(signerAddress, connectedDutchAuction.address);
        const tokenUnits = await connectedWolvercoin.decimals();
        let balance = ethers.utils.formatUnits(approvalAmount, tokenUnits);
        const parsed = parseFloat(balance);
        if(isNaN(parsed)) {
            return;
        }
        setApprovalAmount(Math.round(parsed.toFixed(tokenUnits)*100)/100);
        if (approvalAmount > 0) {
            setApproval(true);
        } else {
            setApproval(false);
        }
        
    }   

    const approve = async () => {
        const provider = web3Context.provider;
        const signer = provider.getSigner();
        const signerAddress = await signer.getAddress();
        const totalWolvercoin = await connectedWolvercoin.getBalanceOf(signerAddress);
        const approve = await connectedWolvercoin.approve(connectedDutchAuction.address, totalWolvercoin);
        setApproval(approve);
        updateApproval();
    }

    if (needsApproval === true && approval === "none") {
        updateApproval();
        return <div>Checking approval for dutch auctions...</div>
    } else if (needsApproval === false || approval === true || (approvalAmount > 0 && approvalAmount === wolvercoinBalance)) {
        return <div className="approved-to-spend">Approved {approvalAmount} WVC on Dutch Auctions</div>
    } else if (approvalAmount > 0) {
        return (
        <div className="setApproval">
            <div>Already approved {approvalAmount} WVC to spend on Dutch Auctions</div>
            <span className="">
                <span>Please approve the rest of your Wolvercoin for Dutch Auctions: </span>
            <button className="button-approve-spending" onClick={approve}>Approve</button>
            </span>
        </div>
        )
    } else {
    return (
        <div className="setApproval">
            { approvalAmount ?  <div>Already approved {approvalAmount} WVC to spend on Dutch Auctions</div> : <div></div> }
            <span className="alert-to-approve-spending">
                <span>Please approve ALL Wolvercoin for Dutch Auctions: </span>
            <button className="button-approve-spending" onClick={approve}>Approve</button>
            </span>
            
        </div>         
        )
    }
}

export default Approve;
