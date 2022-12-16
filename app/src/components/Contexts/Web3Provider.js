import React, { useEffect } from "react";
import { ethers } from "ethers";
import * as Contracts from "./config.js"

// Make sure the shape of the default value passed to
// createContext matches the shape that the consumers expect!
export const Web3Context = React.createContext();

export const Web3Provider = (props) => {
  const [provider, setProvider] = React.useState(props.provider);
  const [connectedAccount, setConnectedAccount] = React.useState("");
  const [chainId, setChainId] = React.useState(0);
  const [wolvercoinBalance, setWolvercoinBalance] = React.useState(0);
  const [nftContract, setNftContract] = React.useState();
  const [wolvercoinContract, setWolvercoinContract] = React.useState();
  
  const setInitialWolvercoinContract = async(provider) => {
    setWolvercoinContract(new ethers.Contract(
      Contracts.ACTIVE_CONTRACTS.wolvercoin.address, 
      Contracts.ACTIVE_CONTRACTS.wolvercoin.ABI.abi, 
      provider.getSigner()
    ))
  }  
  const setInitialNftContract = async(provider) => {
    setNftContract(new ethers.Contract(
      Contracts.ACTIVE_CONTRACTS.nft.address, 
      Contracts.ACTIVE_CONTRACTS.nft.ABI.abi,
      provider.getSigner()
    ))
  }
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
  }), [connectedAccount, chainId, wolvercoinBalance, provider, nftContract, wolvercoinContract]);

  // Set contexts
  useEffect(() => { setInitialChainId(provider); }, [provider]);
  useEffect(() => { setInitialAccount(provider); }, [provider]);
  useEffect(() => { setInitialWolvercoinContract(provider); }, [provider]);
  useEffect(() => { setInitialNftContract(provider); }, [provider]);

  return (
    <Web3Context.Provider value={providerValueContext}>
      {props.children}
    </Web3Context.Provider>
  );
}
export default Web3Provider;