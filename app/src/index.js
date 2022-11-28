import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { Web3ContextProvider } from "./components/Web3/Web3Context.js";

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
    <Web3ContextProvider>
      <App />
    </Web3ContextProvider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
