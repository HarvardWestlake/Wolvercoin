import "./admin.css";
import React from "react";
import WhitelistContractForm from "./AddAdminForm";

const Admin = () => {
    return (
        <div class="admin">
            <div id="active-users">
                <h1>Active Users</h1>
                <WhitelistContractForm />
            </div>
        </div>
    );
}

export default Admin;