import React, { useState, useEffect } from "react";
import { ethers } from "ethers";
import * as Contracts from "./config.js"

// Make sure the shape of the default value passed to
// createContext matches the shape that the consumers expect!
export const Web3Context = React.createContext();

export const Web3Provider = (props) => {
  const [connectedAccount, setConnectedAccount] = React.useState("");
  const [chainId, setChainId] = React.useState(1);
  const [wolvercoinBalance, setWolvercoinBalance] = React.useState(0);

  // Set app context once
  const setAppContext = async () => {
    const provider = new ethers.providers.Web3Provider(window.ethereum);
    const accounts = await provider.listAccounts();
    const connectedAccount = accounts[0];

    const network = await provider.getNetwork();
    console.log(network, network.chainId);

    // See if account is already connected
    if (accounts.length > 0) {
      const balance = await provider.getBalance(connectedAccount);
      setConnectedAccount(connectedAccount);

      const wolvercoinContract = new ethers.Contract(
        Contracts.ACTIVE_CONTRACTS.wolvercoin.address, 
        Contracts.ACTIVE_CONTRACTS.wolvercoin.ABI.abi, 
        provider
      );

      const tokenName = await wolvercoinContract.name();
      const tokenBalance = await wolvercoinContract.balanceOf(connectedAccount);
      const tokenUnits = await wolvercoinContract.decimals();
      const tokenBalanceInEther = ethers.utils.formatUnits(tokenBalance, tokenUnits);
      setWolvercoinBalance(tokenBalanceInEther);
    }
  };

  // passing-multiple-value-and-setter-pairs-to-context-provider-in-react
  //const updateContextState = useCallback((value: updateContextType) => {         setContextState((prevState) => ({ ...prevState, ...value }))     }, [])
  // To get around this in a functional component, you can use useMemo to memoise
  //  the value and refresh only when one of these values change.
  const providerValueContext = React.useMemo(() => ({
    connectedAccount, setConnectedAccount, chainId, setChainId, wolvercoinBalance, setWolvercoinBalance
  }), [connectedAccount, chainId, wolvercoinBalance]);
  useEffect(() => { setAppContext(); }, []);
  return (
    <Web3Context.Provider value={providerValueContext}>
      {props.children}
    </Web3Context.Provider>
  );
}
export default Web3Provider;