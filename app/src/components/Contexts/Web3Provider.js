import React, { useState, useEffect } from "react";
import { ethers } from "ethers";
import * as Contracts from "./config.js"

// Make sure the shape of the default value passed to
// createContext matches the shape that the consumers expect!
export const Web3Context = React.createContext();

const getProvider = () => {
  return new ethers.providers.Web3Provider(window.ethereum, 'any');
}

export const Web3Provider = (props) => {
  const [provider, setProvider] = React.useState(getProvider());
  const [connectedAccount, setConnectedAccount] = React.useState("");
  const [chainId, setChainId] = React.useState(0);
  const [wolvercoinBalance, setWolvercoinBalance] = React.useState(0);
  const [nftContract, setNftContract] = React.useState(new ethers.Contract(
    Contracts.ACTIVE_CONTRACTS.nft.address, 
    Contracts.ACTIVE_CONTRACTS.nft.ABI.abi,
    provider.getSigner()
  ))
  const [wolvercoinContract, setWolvercoinContract] = React.useState(new ethers.Contract(
    Contracts.ACTIVE_CONTRACTS.wolvercoin.address, 
    Contracts.ACTIVE_CONTRACTS.wolvercoin.ABI.abi, 
    provider.getSigner()
  ))
  
  const setInitialAccount = async(provider) => {
    const accounts = await provider.listAccounts();
    setConnectedAccount(accounts[0]);
  }

  const setInitialChainId = async(provider) => {
    const network = await provider.getNetwork();
    setChainId(network.chainId);
  };
  // passing-multiple-value-and-setter-pairs-to-context-provider-in-react
  //const updateContextState = useCallback((value: updateContextType) => {         setContextState((prevState) => ({ ...prevState, ...value }))     }, [])
  // To get around this in a functional component, you can use useMemo to memoise
  //  the value and refresh only when one of these values change.
  const providerValueContext = React.useMemo(() => ({
    connectedAccount, setConnectedAccount, 
    chainId, setChainId, 
    wolvercoinBalance, setWolvercoinBalance, 
    provider, setProvider,
    nftContract, setNftContract,
    wolvercoinContract, setWolvercoinContract
  }), [connectedAccount, chainId, wolvercoinBalance, provider]);

  // Set contexts
  useEffect(() => { setInitialChainId(provider); }, []);
  useEffect(() => { setInitialAccount(provider); }, []);

  return (
    <Web3Context.Provider value={providerValueContext}>
      {props.children}
    </Web3Context.Provider>
  );
}
export default Web3Provider;