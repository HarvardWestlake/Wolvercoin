import "./admin.css";
import React from "react";
import ActiveUserForm from "./ActiveUserForm";
import AddPublicGoodForm from "./AddPublicGoodForm";
import AddAuctionItemForm from "./AddAuctionItemForm";

const Admin = (props) => {
    return (
        <div className="admin">
            <div id="active-users">
                <h1>Active Users</h1>
                <ActiveUserForm />
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
