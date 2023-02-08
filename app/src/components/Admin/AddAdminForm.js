import React, { useEffect } from "react";
import { Web3Context } from "../Contexts/Web3Provider";

export default function AddAdminForm() {
    const [adminAddress, setAdminAddress] = React.useState("");
    const [resultText, setResultText] = React.useState("");

    
    const web3Context = React.useContext(Web3Context);
    const provider = web3Context?.provider;
    const signer = provider?.getSigner();
    const connectedActiveUsers = web3Context?.activeUserContract.connect(signer);
    
    const checkActiveUser = async () => {
        if(!adminAddress) return;
        const data = await connectedActiveUsers.getIsActiveUser(adminAddress);
        setResultText(data === true ? "User is an active user" : "User is not an active user");
    }

    const addActiveUser = async () => {
        if(!adminAddress) return;
        await connectedActiveUsers.addUser(adminAddress);
        setResultText("Active user added (may take a while for block to be mined)");
    }

    const addAdmin = async () => {
        if(!adminAddress) return;
        await connectedActiveUsers.addAdmin(adminAddress);
        setResultText("Admin added (may take a while for block to be mined)");
    }
    
    const removeAdmin = async () => {
        if(!adminAddress) return;
        await connectedActiveUsers.removeAdmin(adminAddress);
        setResultText("Admin removed (may take a while for block to be mined)");
    }
    
    const checkIfAdmin = async () => {
        if(!adminAddress) return;
        const data = await connectedActiveUsers.getIsAdmin(adminAddress);
        setResultText(data === true ? "User is an admin" : "User is not an admin");
    }
    
    return (
        <div id="add-admin-form">
            <h2>Admin management:</h2>
            <input placeholder="User address" value={adminAddress} onChange={(e) => {
                setAdminAddress(e.target.value);
            }} /><br />
            <button onClick={checkActiveUser} disabled={!adminAddress}>Check if user is active user</button><br />
            <button onClick={addActiveUser} disabled={!adminAddress}>Add user as active user</button><br /><br />
            <button onClick={checkIfAdmin} disabled={!adminAddress}>Check if user is admin</button><br />
            <button onClick={addAdmin} disabled={!adminAddress}>Add user as admin</button><br />
            <button onClick={removeAdmin} disabled={!adminAddress}>Revoke admin from user</button><br />
            <p className="result">{resultText}</p>
        </div>
    );
}