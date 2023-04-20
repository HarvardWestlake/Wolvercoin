import React, { useEffect } from "react";
import { Web3Context } from "../Contexts/Web3Provider";
import { ethers } from "ethers";

export default function ActiveUserForm() {
    const [adminAddress, setAdminAddress] = React.useState("");
    const [gradYear, setGradYear] = React.useState("");
    const [bulkAdminAddress, setBulkAdminAddress] = React.useState("");
    const [yearResultText, setYearResultText] = React.useState("");
    const [bulkResultText, setBulkResultText] = React.useState("");
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

    const checkGradYear = async () => {
        if(!adminAddress) return;
        const data = await connectedActiveUsers.getUserGradYear(adminAddress);
        setYearResultText(String(data));
    }
    
    const checkIfAdmin = async () => {
        if(!adminAddress) return;
        const data = await connectedActiveUsers.getIsAdmin(adminAddress);
        setResultText(data === true ? "User is an admin" : "User is not an admin");
    }

    const getGradYear = async () => {
        const data = await connectedActiveUsers.getCurrentGradYear();
        setYearResultText(String(data));
    }

    const setCurrentGradYear = async () => {
        console.log("gradYear: " + gradYear);
        await connectedActiveUsers.setCurrentGradYear(gradYear);
        setYearResultText("Grad Year Set, please get grad year to confirm");
    }

    const bulkAddUsers = async () => {
        const data = await connectedActiveUsers.addBulkUsers(bulkAdminAddress);
        setBulkResultText(String(data.hash));
    }
    
    return (
        <div id="add-admin-form">
            <h2>Admin management:</h2>
            <input placeholder="User address" value={adminAddress} onChange={(e) => {
                setAdminAddress(e.target.value);
            }} /><br />
            <button onClick={checkActiveUser} disabled={!adminAddress}>Check if user is active user</button><br />
            <button onClick={addActiveUser} disabled={!adminAddress}>Add user as active user</button><br /><br />
            <button onClick={checkGradYear} disabled={!adminAddress}>Check user grad year</button><br />
            <button onClick={checkIfAdmin} disabled={!adminAddress}>Check if user is admin</button><br />
            <button onClick={addAdmin} disabled={!adminAddress}>Add user as admin</button><br />
            <button onClick={removeAdmin} disabled={!adminAddress}>Revoke admin from user</button><br />
            <p className="result">{resultText}</p>


            <br /><br />
            <h2>Bulk Admin management:</h2>
            <textarea placeholder="User addresses" value={bulkAdminAddress} onChange={(e) => {
                setBulkAdminAddress(e.target.value.split(','));
            }} /><br />
            <button onClick={bulkAddUsers} disabled={!bulkAdminAddress}>Add users as active users</button><br /><br />
            <p className="result">{bulkResultText}</p>

            <h2>Grad Year management:</h2>
            <button onClick={setCurrentGradYear}>Set Grad Year</button><br />
            <input placeholder="Set Grad Year Here" value={gradYear} onChange={(e) => {
                setGradYear(e.target.value);
            }} /><br />            
            <button onClick={getGradYear}>Get Grad Year</button><br />
            <p className="result">{yearResultText}</p>


        </div>
    );
}
