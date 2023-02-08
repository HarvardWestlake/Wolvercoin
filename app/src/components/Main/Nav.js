import React from "react";
import { Web3Context } from "../Contexts/Web3Provider";
import { ADMIN_ROUTES, NAV_DEFAULT_LOCATION, NAV_OPTIONS } from "./consts";

const Nav = ({location, updateHashLocation}) => {
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

  const onNavClick = (e) => {
    if (!e || !e.target || !e.target.name) {
      e = {target:{name:""}};
    }
    window.location.hash = e.target.name;
    updateHashLocation(e.target.name);
  }

  const renderNavLinks = () => {
    let navigationOptions = <div className="menu-items"></div>;
    let loc = location ? location : NAV_DEFAULT_LOCATION;
    if (Object.keys(NAV_OPTIONS).length > 0) {
        navigationOptions = Object.keys(NAV_OPTIONS).map((key) => (
          (isAdmin || !ADMIN_ROUTES.includes(key)) && (
            // eslint-disable-next-line jsx-a11y/anchor-is-valid
            <a
              key={key}
              id={NAV_OPTIONS[key]}
              className={loc === NAV_OPTIONS[key] ? "menu-item active" : "menu-item"}
              name={NAV_OPTIONS[key]}
              onClick={onNavClick}
            >{key}</a>
          )
      ));
    }
    return navigationOptions;
  }

  React.useEffect(() => {
    if (window.location.hash) {
      const hash = window.location.hash.substring(1);
      updateHashLocation(hash);
    }
  }, [updateHashLocation]);

  let navOptions = renderNavLinks();
  return (
    <div className="menu-items">
      {navOptions}
    </div>
  )
}

export default Nav;
