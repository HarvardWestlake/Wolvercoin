import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { Drizzle, generateStore } from "@drizzle/store";
import { DrizzleContext } from "@drizzle/react-plugin";
// import SimpleStorage from "./contracts/SimpleStorage.json";


// 2. Setup the drizzle instance.
//const options = { contracts: [SimpleStorage] };
const options = { contracts: [] };
const drizzleStore = generateStore(options);
const drizzle = new Drizzle(options, drizzleStore);

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyB13Rzp7Ey2IFI3RTY9cD1VHFq9p8_uF4U",
  authDomain: "wolvercoin-hw.firebaseapp.com",
  projectId: "wolvercoin-hw",
  storageBucket: "wolvercoin-hw.appspot.com",
  messagingSenderId: "101117958130",
  appId: "1:101117958130:web:49ad8f0613ef4eb66d3d6b",
  measurementId: "G-PC4QR208EF"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <DrizzleContext.Provider drizzle={drizzle}>
      <App />
    </DrizzleContext.Provider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
