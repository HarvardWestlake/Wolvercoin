import logo from './logo.svg';
import './App.css';
import React, { Suspense, lazy } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { UserAuthContextProvider } from "./components/Firebase/UserAuthContext.js";
import Firestore from "./components/Firebase/Firestore.js";

const Home = lazy(() => import("./routes/Home.js"));
const AboutRoute = lazy(() => import("./routes/About.js"));
const MemberRoute = lazy(() => import("./routes/Member.js"));
const NFTRoute = lazy(() => import("./routes/NFT.js"));

function App() {
  return  (
    <UserAuthContextProvider>
      <Router>
        <Suspense fallback={<Home />}>
          <Routes>
            <Route exact path="/" element={<Home />} />
            <Route exact path="/nft/:nftCollectionId/:nftId" element={<NFTRoute firestore={Firestore} />} />
            <Route exact path="/membership" element={<MemberRoute firestore={Firestore} />} />
            <Route exact path="/member/:memberId" element={<MemberRoute firestore={Firestore} />} />
          </Routes>
        </Suspense>
      </Router>
    </UserAuthContextProvider>
  );
  
}

export default App;