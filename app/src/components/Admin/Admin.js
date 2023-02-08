import "./admin.css";
import React from "react";
import WhitelistContractForm from "./AddAdminForm";
import AddPublicGoodForm from "./AddPublicGoodForm";
import AddAuctionItemForm from "./AddAuctionItemForm";

const Admin = () => {
    return (
        <div className="admin">
            <div id="active-users">
                <h1>Active Users</h1>
                <WhitelistContractForm />
            </div>
            <div id="public-goods-management">
                <h1>Public Goods</h1>
                <AddPublicGoodForm />
            </div>
            <div id="auction-management">
                <h1>Auction Items</h1>
                <AddAuctionItemForm />
            </div>
        </div>
    );
}

export default Admin;