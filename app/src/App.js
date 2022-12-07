import logo from './logo.svg';
import './App.css';
import React, { Suspense, lazy } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { UserAuthContextProvider } from "./components/Firebase/UserAuthContext.js";
import Firestore from "./components/Firebase/Firestore.js";
import { Web3Context, withWeb3 } from "./components/Web3"
import Header from "./components/Common/Header/main"
import Footer from "./components/Common/Footer"


const Home = lazy(() => import("./routes/Home.js"));
const AboutRoute = lazy(() => import("./routes/About.js"));
const MemberRoute = lazy(() => import("./routes/Member.js"));
const NFTRoute = lazy(() => import("./routes/NFT.js"));
const ContributeRoute = lazy(() => import("./routes/Contribute.js"));


const App = () => (
    <Router>
    <Web3Context.Consumer>
      {web3ContextState =>  
      <Suspense fallback={<Home />}>
        <Header val={web3ContextState.user}/> 
        <Routes>
          <Route exact path="/" element={<Home />} />
          <Route exact path="/nft/:nftCollectionId/:nftId" element={<NFTRoute firestore={Firestore} />} />
          <Route exact path="/membership" element={<MemberRoute firestore={Firestore} />} />
          <Route exact path="/member/:memberId" element={<MemberRoute firestore={Firestore} />} />
          <Route exact path="/contribute" element={<ContributeRoute firestore={Firestore} />} />
        </Routes>
        <Footer />
      </Suspense> } 
      </Web3Context.Consumer>
    </Router>
  );

  export default withWeb3(App);