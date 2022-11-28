import logo from './logo.svg';
import './App.css';
import React, { Suspense, lazy } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { UserAuthContextProvider } from "./components/Firebase/UserAuthContext.js";
import Firestore from "./components/Firebase/Firestore.js";
import { Web3Context, withWeb3 } from "./components/Web3"
import Header from "./components/Common/Header"
import Footer from "./components/Common/Footer"


const Home = lazy(() => import("./routes/Home.js"));
const AboutRoute = lazy(() => import("./routes/About.js"));
const MemberRoute = lazy(() => import("./routes/Member.js"));
const NFTRoute = lazy(() => import("./routes/NFT.js"));


const App = () => (
    <Router>
      <Suspense fallback={<Home />}>
      <Web3Context.Consumer>
        {user => user['auth'] ? <Header val={1}/> : <Header val={0} />
        }
      </Web3Context.Consumer>
        <Routes>
          <Route exact path="/" element={<Home />} />
          <Route exact path="/nft/:nftCollectionId/:nftId" element={<NFTRoute firestore={Firestore} />} />
          <Route exact path="/membership" element={<MemberRoute firestore={Firestore} />} />
          <Route exact path="/member/:memberId" element={<MemberRoute firestore={Firestore} />} />
        </Routes>
        <Footer />
      </Suspense>
    </Router>
  );

  export default withWeb3(App);