import logo from './logo.svg';
import './App.css';
import React, { Suspense, lazy } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { UserAuthContextProvider } from "./components/Firebase/UserAuthContext.js";
import Firestore from "./components/Firebase/Firestore.js";
import { Web3Context, withWeb3 } from "./components/Web3"
import Header from "./components/Common/Header/main"
import Footer from "./components/Common/Footer"


const Main = lazy(() => import("./routes/Main.js"));

const Home = lazy(() => import("./routes/Home.js"));
const AboutRoute = lazy(() => import("./routes/About.js"));
const MemberRoute = lazy(() => import("./routes/Member.js"));
const NFTRoute = lazy(() => import("./routes/NFT.js"));
const ContributeRoute = lazy(() => import("./routes/Contribute.js"));


const App = () => (
    <Web3Context.Consumer>
      {web3ContextState =>  
      <Main firestore={Firestore} web3Context={web3ContextState}/>}
      }
      </Web3Context.Consumer>
  );

  export default withWeb3(App);