import React, { useState, useEffect } from "react";
import { ethers } from "ethers";

// Make sure the shape of the default value passed to
// createContext matches the shape that the consumers expect!
export const Web3Context = React.createContext();

export const Web3Provider = (props) => {
  const [provider, setProvider] = React.useState(props.provider);
  const [connectedAccount, setConnectedAccount] = React.useState(null);
  const [accounts, setAccounts] = React.useState([]);
  const [chainId, setChainId] = React.useState(0);

  const setAppContext = (p) => {
    console.log(p, props, provider);
  }
  // passing-multiple-value-and-setter-pairs-to-context-provider-in-react
  //const updateContextState = useCallback((value: updateContextType) => {         setContextState((prevState) => ({ ...prevState, ...value }))     }, [])
  // To get around this in a functional component, you can use useMemo to memoise
  //  the value and refresh only when one of these values change.
  const providerValueContext = React.useMemo(() => ({
    connectedAccount, setConnectedAccount, chainId, setChainId, provider, setProvider, accounts, setAccounts
  }), [connectedAccount, chainId, provider, accounts]);
  return (
    <Web3Context.Provider value={providerValueContext}>
      {props.children}
    </Web3Context.Provider>
  );
}
export default Web3Provider;